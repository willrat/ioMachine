import gettext
import locale

APPLICATION_DOMAIN = 'machine'

def initFinnish():
  locale.setlocale(locale.LC_ALL, "fi_FI.utf8")
  locale.bindtextdomain(APPLICATION_DOMAIN, './locale')
  finnish = gettext.translation(APPLICATION_DOMAIN, localedir='./locale', languages=['fi'], fallback=True)
  finnish.install()

def initEnglish():
  locale.setlocale(locale.LC_ALL, "en_GB.utf8")
  locale.bindtextdomain(APPLICATION_DOMAIN, './locale')
  english = gettext.translation(APPLICATION_DOMAIN, localedir='./locale', languages=['en'], fallback=True)
  english.install()


# initFinnish()
initEnglish()

