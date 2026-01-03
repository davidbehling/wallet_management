from i18n import pt_BR

LOCALES = {
  "pt_BR": pt_BR.TRANSLATIONS
}

_current_locale = "pt_BR"

def set_locale(locale):
  global _current_locale
  if locale in LOCALES:
    _current_locale = locale

def t(key):
  return LOCALES[_current_locale].get(key, key)
