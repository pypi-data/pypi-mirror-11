import django
if django.VERSION >= (1, 7):
    from django.core import checks
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist
from django.db.models.manager import Manager
from django.db.models.signals import post_save, class_prepared
from django.utils.translation import get_language
from hvad.descriptors import LanguageCodeAttribute, TranslatedAttribute
from hvad.manager import TranslationManager, TranslationsModelManager
from hvad.utils import (get_cached_translation, set_cached_translation,
                        SmartGetFieldByName, SmartGetField, settings_updater)
from hvad.compat import MethodType
from itertools import chain
import sys
import warnings

#===============================================================================

# Global settings, wrapped so they react to SettingsOverride
@settings_updater
def update_settings(*args, **kwargs):
    global FALLBACK_LANGUAGES, TABLE_NAME_SEPARATOR
    FALLBACK_LANGUAGES = tuple( code for code, name in settings.LANGUAGES )
    TABLE_NAME_SEPARATOR = getattr(settings, 'HVAD_TABLE_NAME_SEPARATOR', '_')

#===============================================================================

def _split_together(constraints, fields, meta, name):
    sconst, tconst = [], []
    if name in meta:
        # raise in 1.4, remove in 1.6
        warnings.warn('Passing \'%s\' to TranslatedFields is deprecated. Please use '
                      'Please Meta.%s instead.' % (name, name), DeprecationWarning)
        tconst.extend(meta[name])

    for constraint in constraints:
        if all(item in fields for item in constraint):
            tconst.append(constraint)
        elif not any(item in fields for item in constraint):
            sconst.append(constraint)
        else:
            raise ImproperlyConfigured(
                'Constraints in Meta.%s cannot mix translated and '
                'untranslated fields, such as %r.' % (name, constraint))
    return sconst, tconst

def create_translations_model(model, related_name, meta, **fields):
    """
    Create the translations model for the shared model 'model'.
    'related_name' is the related name for the reverse FK from the translations
    model.
    'meta' is a (optional) dictionary of attributes for the translations model's
    inner Meta class.
    'fields' is a dictionary of fields to put on the translations model.
    
    Two fields are enforced on the translations model:
    
        language_code: A 15 char, db indexed field.
        master: A ForeignKey back to the shared model.
        
    Those two fields are unique together, this get's enforced in the inner Meta
    class of the translations table
    """

    # Build a list of translation models from base classes. Depth-first scan.
    abstract = model._meta.abstract
    translation_bases = []
    translation_base_fields = set()
    scan_bases = list(reversed(model.__bases__)) # backwards so we can use pop/extend
    while scan_bases:
        base = scan_bases.pop()
        if not issubclass(base, TranslatableModel) or base is TranslatableModel:
            continue
        if not base._meta.abstract:
            raise TypeError(
                'Multi-table inheritance of translatable models is not supported. '
                'Concrete model %s is not a valid base model for %s.' % (
                    base._meta.model_name if django.VERSION >= (1, 6) else base._meta.module_name,
                    model._meta.model_name if django.VERSION >= (1, 6) else model._meta.module_name))
        try:
            # The base may have translations model, then just inherit that
            translation_bases.append(base._meta.translations_model)
            translation_base_fields.update(field.name for field in base._meta.translations_model._meta.fields)
        except AttributeError:
            # But it may not, and simply inherit other abstract bases, scan them
            scan_bases.extend(reversed(base.__bases__))
    translation_bases.append(BaseTranslationModel)

    # Create translation model Meta
    meta = meta or {}
    meta['abstract'] = abstract
    meta['db_tablespace'] = model._meta.db_tablespace
    meta['managed'] = model._meta.managed
    if model._meta.order_with_respect_to in fields:
        raise ValueError(
            'Using a translated fields in %s.Meta.order_with_respect_to is ambiguous '
            'and hvad does not support it.' %
            model._meta.model_name if django.VERSION >= (1, 6) else model._meta.module_name)

    sconst, tconst = _split_together(
        model._meta.unique_together,
        translation_base_fields.union(fields).union(('language_code',)),
        meta,
        'unique_together'
    )
    model._meta.unique_together = tuple(sconst)
    meta['unique_together'] = tuple(tconst)
    if django.VERSION >= (1, 5):
        sconst, tconst = _split_together(
            model._meta.index_together,
            translation_base_fields.union(fields).union(('language_code',)),
            meta,
            'index_together'
        )
        model._meta.index_together = tuple(sconst)
        meta['index_together'] = tuple(tconst)

    if not abstract:
        unique = [('language_code', 'master')]
        meta['unique_together'] = list(meta.get('unique_together', [])) + unique
    Meta = type('Meta', (object,), meta)

    if not hasattr(Meta, 'db_table'):
        Meta.db_table = model._meta.db_table + '%stranslation' % TABLE_NAME_SEPARATOR
    Meta.app_label = model._meta.app_label
    name = '%sTranslation' % model.__name__

    # Create translation model
    attrs = {}
    attrs.update(fields)
    attrs['Meta'] = Meta
    attrs['__module__'] = model.__module__

    if not abstract:
        # If this class is abstract, we must not contribute management fields
        attrs['objects'] = TranslationsModelManager()
        attrs['language_code'] = models.CharField(max_length=15, db_index=True)
        # null=True is so we can prevent cascade deletion
        attrs['master'] = models.ForeignKey(model, related_name=related_name,
                                            editable=False, null=True)
    # Create and return the new model
    translations_model = ModelBase(name, tuple(translation_bases), attrs)
    if not abstract:
        # Abstract models do not have a DNE class
        bases = (model.DoesNotExist, translations_model.DoesNotExist,)
        DNE = type('DoesNotExist', bases, {})
        translations_model.DoesNotExist = DNE
    opts = translations_model._meta
    opts.shared_model = model

    # We need to set it here so it is available when we scan subclasses
    model._meta.translations_model = translations_model

    # Register it as a global in the shared model's module.
    # This is needed so that Translation model instances, and objects which
    # refer to them, can be properly pickled and unpickled. The Django session
    # and caching frameworks, in particular, depend on this behaviour.
    mod = sys.modules[model.__module__]
    setattr(mod, name, translations_model)

    return translations_model


class TranslatedFields(object):
    """
    Wrapper class to define translated fields on a model.
    """
    def __init__(self, meta=None, **fields):
        self.fields = fields
        self.meta = meta

    def contribute_to_class(self, cls, name):
        """
        Called from django.db.models.base.ModelBase.__new__
        """
        create_translations_model(cls, name, self.meta, **self.fields)


class BaseTranslationModel(models.Model):
    """
    Needed for detection of translation models. Due to the way dynamic classes
    are created, we cannot put the 'language_code' field on here.
    """
    def _get_unique_checks(self, exclude=None):
        # Due to the way translations are handled, checking for unicity of
        # the ('language_code', 'master') constraint is useless. We filter it out
        # here so as to avoid a useless query
        unique_checks, date_checks = super(BaseTranslationModel, self)._get_unique_checks(exclude=exclude)
        unique_checks = [check for check in unique_checks
                         if check != (self.__class__, ('language_code', 'master'))]
        return unique_checks, date_checks

    class Meta:
        abstract = True


class NoTranslation(object):
    pass


class TranslatableModel(models.Model):
    """
    Base model for all models supporting translated fields (via TranslatedFields).
    """
    # change the default manager to the translation manager
    objects = TranslationManager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # Split arguments into shared/translatd
        veto_names = ('pk', 'master', 'master_id', self._meta.translations_model._meta.pk.name)
        skwargs, tkwargs = {}, {}
        for key, value in kwargs.items():
            if key in self._translated_field_names and not key in veto_names:
                tkwargs[key] = value
            else:
                skwargs[key] = value

        super(TranslatableModel, self).__init__(*args, **skwargs)

        # Create a translation if there are translated fields
        if tkwargs:
            tkwargs['language_code'] = tkwargs.get('language_code') or get_language()
            set_cached_translation(self, self._meta.translations_model(**tkwargs))

    @classmethod
    def save_translations(cls, instance, **kwargs):
        'Signal handler for post_save'
        translation = get_cached_translation(instance)
        if translation is not None:
            translation.master = instance
            translation.save()

    def translate(self, language_code):
        ''' Create a new translation for current instance.
            Does NOT check if the translation already exists!
        '''
        set_cached_translation(
            self,
            self._meta.translations_model(language_code=language_code)
        )
        return self

    def safe_translation_getter(self, name, default=None):
        cache = get_cached_translation(self)
        if cache is None:
            return default
        return getattr(cache, name, default)

    def lazy_translation_getter(self, name, default=None):
        """
        Lazy translation getter that fetches translations from DB in case the instance is currently untranslated and
        saves the translation instance in the translation cache
        """
        stuff = self.safe_translation_getter(name, NoTranslation)
        if stuff is not NoTranslation:
            return stuff

        # get all translations
        translations = getattr(self, self._meta.translations_accessor).all()

        # if no translation exists, bail out now
        if len(translations) == 0:
            return default

        # organize translations into a nice dict
        translation_dict = dict((t.language_code, t) for t in translations)

        # see if we have the right language, or any language in fallbacks
        for code in (get_language(), settings.LANGUAGE_CODE) + FALLBACK_LANGUAGES:
            try:
                translation = translation_dict[code]
            except KeyError:
                continue
            break
        else:
            # none of the fallbacks was found, pick an arbitrary translation
            translation = translation_dict.popitem()[1]

        set_cached_translation(self, translation)
        return getattr(translation, name, default)

    def get_available_languages(self):
        """ Get a list of all available language_code in db. """
        qs = getattr(self, self._meta.translations_accessor).all()
        if qs._result_cache is not None:
            return [obj.language_code for obj in qs]
        return qs.values_list('language_code', flat=True)

    #===========================================================================
    # Validation
    #===========================================================================

    def clean_fields(self, exclude=None):
        super(TranslatableModel, self).clean_fields(exclude=exclude)
        translation = get_cached_translation(self)
        if translation is not None:
            translation.clean_fields(exclude=exclude + ['id', 'master', 'master_id', 'language_code'])

    def validate_unique(self, exclude=None):
        super(TranslatableModel, self).validate_unique(exclude=exclude)
        translation = get_cached_translation(self)
        if translation is not None:
            translation.validate_unique(exclude=exclude)

    #===========================================================================
    # Checks - require Django 1.7 or newer
    #===========================================================================

    if django.VERSION >= (1, 7):
        @classmethod
        def check(cls, **kwargs):
            errors = super(TranslatableModel, cls).check(**kwargs)
            errors.extend(cls._check_shared_translated_clash())
            return errors

        @classmethod
        def _check_shared_translated_clash(cls):
            fields = set(chain.from_iterable(
                (f.name, f.attname)
                for f in cls._meta.fields
            ))
            tfields = set(chain.from_iterable(
                (f.name, f.attname)
                for f in cls._meta.translations_model._meta.fields
                if f.name not in ('id', 'master')
            ))
            return [checks.Error("translated field '%s' clashes with untranslated field." % field,
                                hint=None, obj=cls, id='hvad.models.E01')
                    for field in tfields.intersection(fields)]

        @classmethod
        def _check_local_fields(cls, fields, option):
            """ Remove fields we recognize as translated fields from tests """
            to_check = []
            for field in fields:
                try:
                    cls._meta.translations_model._meta.get_field(field)
                except FieldDoesNotExist:
                    to_check.append(field)
            return super(TranslatableModel, cls)._check_local_fields(to_check, option)

        @classmethod
        def _check_ordering(cls):
            if not cls._meta.ordering:
                return []

            if not isinstance(cls._meta.ordering, (list, tuple)):
                return [checks.Error("'ordering' must be a tuple or list.",
                                    hint=None, obj=cls, id='models.E014')]

            fields = [f for f in cls._meta.ordering if f != '?']
            fields = [f[1:] if f.startswith('-') else f for f in fields]
            fields = set(f for f in fields if f not in ('_order', 'pk') and '__' not in f)

            valid_fields = set(chain.from_iterable(
                (f.name, f.attname)
                for f in cls._meta.fields
            ))
            valid_tfields = set(chain.from_iterable(
                (f.name, f.attname)
                for f in cls._meta.translations_model._meta.fields
                if f.name not in ('master', 'language_code')
            ))

            return [checks.Error("'ordering' refers to the non-existent field '%s' --hvad." % field,
                                hint=None, obj=cls, id='models.E015')
                    for field in fields - valid_fields - valid_tfields]

    #===========================================================================
    # Internals
    #===========================================================================
    
    @property
    def _translated_field_names(self):
        if getattr(self, '_translated_field_names_cache', None) is None:
            opts = self._meta.translations_model._meta
            result = set()

            if django.VERSION >= (1, 8):
                for field in opts.get_fields():
                    result.add(field.name)
                    if hasattr(field, 'attname'):
                        result.add(field.attname)
            else:
                result = set(opts.get_all_field_names())
                for name in tuple(result):
                    try:
                        attname = opts.get_field(name).get_attname()
                    except (FieldDoesNotExist, AttributeError):
                        continue
                    if attname:
                        result.add(attname)

            self._translated_field_names_cache = tuple(result)
        return self._translated_field_names_cache

#=============================================================================

def contribute_translations(cls, rel):
    """
    Contribute translations options to the inner Meta class and set the
    descriptors.

    This get's called from prepare_translatable_model
    """
    opts = cls._meta
    opts.translations_accessor = rel.get_accessor_name()
    if django.VERSION >= (1, 8):
        opts.translations_model = rel.field.model
    else:
        opts.translations_model = rel.model
    opts.translations_cache = '%s_cache' % rel.get_accessor_name()
    trans_opts = opts.translations_model._meta

    # Set descriptors
    ignore_fields = ('pk', 'master', 'master_id', opts.translations_model._meta.pk.name)
    for field in trans_opts.fields:
        if field.name in ignore_fields:
            continue
        if field.name == 'language_code':
            attr = LanguageCodeAttribute(opts)
        else:
            attr = TranslatedAttribute(opts, field.name)
            attname = field.get_attname()
            if attname and attname != field.name:
                setattr(cls, attname, TranslatedAttribute(opts, attname))
        setattr(cls, field.name, attr)


def prepare_translatable_model(sender, **kwargs):
    model = sender
    if not issubclass(model, TranslatableModel) or model._meta.abstract:
        return
    if not isinstance(model._default_manager, TranslationManager):
        raise ImproperlyConfigured(
            "The default manager on a TranslatableModel must be a "
            "TranslationManager instance or an instance of a subclass of "
            "TranslationManager, the default manager of %r is not." % model)

    # If this is a proxy model, get the concrete one
    concrete_model = model._meta.concrete_model if model._meta.proxy else model

    # Find the instance of TranslatedFields in the concrete model's dict
    # We cannot use _meta.get_fields here as app registry is not ready yet.
    found = None
    for relation in list(concrete_model.__dict__.keys()):
        try:
            obj = getattr(model, relation)
            if django.VERSION >= (1, 8):
                shared_model = obj.related.field.model._meta.shared_model
            else:
                shared_model = obj.related.model._meta.shared_model
        except AttributeError:
            continue
        if shared_model is concrete_model:
            if found:
                raise ImproperlyConfigured(
                    "A TranslatableModel can only define one set of "
                    "TranslatedFields, %r defines more than one: %r on %r "
                    "and %r on %r and possibly more" % (model, obj,
                    obj.related.model, found, found.related.model))
            # Mark as found but keep looking so we catch duplicates and raise
            found = obj

    if not found:
        raise ImproperlyConfigured(
            "No TranslatedFields found on %r, subclasses of "
            "TranslatableModel must define TranslatedFields." % model
        )

    #### Now we have to work ####

    contribute_translations(model, found.related)

    # Ensure _base_manager cannot be TranslationManager despite use_for_related_fields
    # 1- it is useless unless default_class is overriden
    # 2- in that case, _base_manager is used for saving objects and must not be
    #    translation aware.
    base_mgr = getattr(model, '_base_manager', None)
    if base_mgr is None or isinstance(base_mgr, TranslationManager):
        model.add_to_class('_base_manager', Manager())

    # Replace get_field_by_name with one that warns for common mistakes
    if django.VERSION < (1, 9) and not isinstance(model._meta.get_field_by_name, SmartGetFieldByName):
        model._meta.get_field_by_name = MethodType(
            SmartGetFieldByName(model._meta.get_field_by_name),
            model._meta
        )
    if not isinstance(model._meta.get_field, SmartGetField):
        model._meta.get_field = MethodType(
            SmartGetField(model._meta.get_field),
            model._meta
        )

    # Attach save_translations
    post_save.connect(model.save_translations, sender=model, weak=False)

class_prepared.connect(prepare_translatable_model)
