#uninstallPySide2.py

"""To uninstall PySide2 from Unreal.
"""

from subprocess import call
from site import getsitepackages

unrealSitePackage = getsitepackages()[0]
call(['pip','uninstall','--target',unrealSitePackage])

print('PySide2 uninstalled. alembicImportUI.py will no longer function.','Unless you have PySide2 sourcing via another method, such as sys.path or added it to UE_PYTHONPATH.',sep='\n')