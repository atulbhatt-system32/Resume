#!"c:\users\system32\desktop\projects\resume reader\env\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'tika==1.24','console_scripts','tika-python'
__requires__ = 'tika==1.24'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('tika==1.24', 'console_scripts', 'tika-python')()
    )
