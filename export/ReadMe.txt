"""
To run each tool you must:
1) Copy this folder, called export, into the Maya scripts folder.
2) Open Maya
3) Paste the code given below into the command line or script editor.

Optional:
Highlight the code in the command line and middle-mouse drag it to your preferred shelf.
"""

###


alembicSelectionSet.py
_______________________________
This allsow you to make the needed selection sets that the exporter used to indentify what needs to be exported.

CODE:
from export import alembicSelectionSet; alembicSelectionSet.run()


###

alembicExportUI.py
_____________________
This UI (though currently ugly) allows you to export an alembic cache with the proper settings needed by Unreal.

You can either export a single alembic file of the entire scene (provided the "EXPORT_SET" selection sets are in place. Or, you can export everything individually, based on the respective "EXPORT_SET" selection sets.

CODE:
from export import alembicExportUI; alembicExportUI.AlembicExportUI().showWindow()

