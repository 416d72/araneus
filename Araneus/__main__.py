from Araneus.preferences import *

print(Preferences().get_option("GENERAL", "LANGUAGE"))
Preferences().set_option("GENERAL", "LANGUAGE", 'en')
print(Preferences().get_option("GENERAL", "LANGUAGE"))
