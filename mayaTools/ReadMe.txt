To use the tools in the MtoU_alembicExport/mayaTools folder (this folder),
you must drag and drop the DRAG-N-DROP-IN-MAYA.py file into the Maya viewport window.

You will then see a menu on the top bar of the main window with all the tools. 


If you want to use the tools via a shelf and don't want the menu on the top bar, look below:

Go to the documents/maya/<maya_version>/scripts/MtoU_alembicExport folder.
Rename or delete the userSetup.py file. This is what makes the top bar menu.
Copy the code given below into your script editor, highlight it and middle-click drag it to the desried shelf.


alembicSelectionSet.py
_______________________________
This allows you to make the needed selection sets that the exporter used to indentify what needs to be exported.

CODE:
import alembicSelectionSet; alembicSelectionSet.run()


###

alembicExportUI.py
_____________________
This UI allows you to export an alembic cache with the proper settings needed by Unreal.

You can either export a single alembic file of the entire scene provided the "EXPORT_SET" selection sets are in place. Or, you can export everything individually, based on the respective "EXPORT_SET" selection sets.

CODE:
import alembicExportUI; alembicExportUI.AlembicExportUI().showWindow()