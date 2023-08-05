author = 'calvin'

import gettext
from eventdispatcher import Property

# The translation (gettext) function to be used
translator = None


def fake_translation(s):
    """
    A fake translation function to 'french' that can help you verify that you have tagged all text in the program
    """
    return 'Le %s' % s if s != '\n' else '\n'


class StringProperty(Property):
    observers = set()

    def __init__(self, default_value):
        super(StringProperty, self).__init__(default_value)
        self.translatables = set()
        if not isinstance(default_value, basestring):
            raise ValueError('StringProperty can only accepts strings.')

    def register(self, instance, property_name, default_value):
        super(StringProperty, self).register(instance, property_name, default_value)
        if isinstance(default_value, _):
            prop = instance.event_dispatcher_properties[property_name]
            prop.update({'_': default_value, 'obj': instance})
            StringProperty.observers.add(self.translate)
            self.translatables.add(instance)

    def __get__(self, obj, owner):
        value = obj.event_dispatcher_properties[self.name]['value']
        if isinstance(value, _):
            return _.translate(value)
        else:
            return value

    def __set__(self, obj, value):
        prop = obj.event_dispatcher_properties[self.name]
        if isinstance(value, _):
            # If it is tagged as translatable, register this object as an observer
            prop.update({'_': value, 'obj': obj})
            StringProperty.observers.add(self.translate)
            self.translatables.add(obj)
        if value != prop['value']:
            prop['value'] = value
            for callback in prop['callbacks']:
                if callback(obj, value):
                    break

    def translate(self):
        for obj in self.translatables:
            prop = obj.event_dispatcher_properties[self.name]
            prop['value'] = _.translate(prop['_'])
            for callback in prop['callbacks']:
                callback(prop['obj'], prop['value'])

    @staticmethod
    def remove_translation():
        """
        Remove the currently set translation function and return the language back to english (or default)
        """
        StringProperty.set_translation_function(None)

    @staticmethod
    def set_translation_function(func):
        """
        Set the translation function and dispatch all changes
        """
        global translator
        translator = func
        # Dispatch the changes to all the observers
        for callback in StringProperty.observers:
            callback()

    @staticmethod
    def load_fake_translation():
        """
        Load a fake translation function to that can help you verify that you have tagged all text in the program.
        Adds 'Le' to the beginning of every string.
        """
        StringProperty.set_translation_function(fake_translation)

    @staticmethod
    def switch_lang(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=None):
        global translator
        # Create the translation class from gettext
        translation = gettext.translation(domain, localedir, languages, class_, fallback, codeset)
        translator = translation.ugettext

        # Dispatch the changes to all the observers
        for callback in StringProperty.observers:
            callback()


class _(unicode):
    """
    This is a wrapper to the gettext translation function _(). This wrapper allows the eventdispatcher.StringProperty
    to be automatically updated when the language (translation function) changes. In this way, all labels will be
    re-translated automatically.

    """

    def __new__(cls, s, *args, **kwargs):
        if translator:
            trans = translator(s, *args, **kwargs)
            obj = super(_, cls).__new__(cls, trans, *args, **kwargs)
        else:
            obj = super(_, cls).__new__(cls, s, *args, **kwargs)
        obj.untranslated = s
        return obj

    def __eq__(self, other):
        """
        Compare the fully translated string (including the _additionals) if comparing _ objects, otherwise compare
        the english strings
        """
        s = _.translate(self)
        if isinstance(other, _):
            return s == _.translate(other)
        else:
            return s == other

    def __ne__(self, other):
        """
        Compare the fully translated string (including the _additionals) if comparing _ objects, otherwise compare
        the english strings
        """
        s = _.translate(self)
        if isinstance(other, _):
            return s != _.translate(other)
        else:
            return s != other

    def __add__(self, other):
        """
        Rather than creating a new _ instance of the sum of the two strings, keep the added string as a reference so
        that we can translate each individually. In this way we can make sure the following translates correctly:

            eg.

                _('Show Lines') + '\n' + (_('On') if show_lines else _('Off'))

        """
        if not hasattr(self, '_additionals'):
            self._additionals = []

        if isinstance(other, _):
            self._additionals.append(other)
            if hasattr(other, '_additionals'):
                self._additionals.extend(other._additionals)
        else:
            self._additionals.append(other)

        return self

    def __mul__(self, other):
        if type(other) is bool:
            if other:
                return self
            else:
                return ''
        if type(other) is int:
            if not hasattr(self, '_additionals'):
                self._additionals = []
            self._additionals.extend([self] * other)
        else:
            raise TypeError("can't multiply sequence by non-int of type %s" % type(other))

    @staticmethod
    def join_additionals(s):
        if translator is None:
            l = [s.untranslated]
            for a in s._additionals:
                l.append(a.untranslated if isinstance(a, _) else a)
        else:
            l = [translator(s.untranslated)]
            for a in s._additionals:
                l.append(translator(a.untranslated) if isinstance(a, _) else a)
        return ''.join(l)

    @staticmethod
    def translate(s, *args, **kwargs):
        if hasattr(s, '_additionals'):
            return _.join_additionals(s)
        else:
            if translator is None:
                return s.untranslated.format(args, kwargs)
            else:
                return translator(s.untranslated).format(args, kwargs)


if __name__ == '__main__':

    from eventdispatcher import EventDispatcher

    class Trans(EventDispatcher):
        s = StringProperty('testing')

        def on_s(self, inst, s):
            print s

    class Trans2(EventDispatcher):
        s = StringProperty('blah')

    def to_G(s):
        return 'G_' + s

    locale_dir = "/home/calvin/smc/pygame/lib/PygameWidgets/PygameWidgets/resources/translations"
    StringProperty.switch_lang('ssi', locale_dir, languages=['French'])

    t = Trans()
    t.s = _('Color')
    t.s = _("asd")
    StringProperty.set_translation_function(to_G)
    t.s = _('Color')
    StringProperty.switch_lang('ssi', locale_dir, languages=['french'])

    StringProperty.remove_translation()


    # Test adding _'s
    asd = _('asd')
    qwe = _('qwe')

    asdqwe = asd + qwe
    assert isinstance(asdqwe, _)


    sdf=3

