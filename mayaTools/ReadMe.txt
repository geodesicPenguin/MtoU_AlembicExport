To use the tools in the MtoU_alembicExport/maya folder (this folder),
you must drag and drop the DRAG-N-DROP-IN-MAYA.py file into the Maya viewport window.

You will then see a menu on the top bar of the main window with all the tools. 


If you want to use the tools via Python, look below:

Copy the mayaTools folder to the scripts folder. Then use the code given for each tool below to run.
With this method, you can make your own shelf button.



alembicSelectionSet.py
_______________________________
This allsow you to make the needed selection sets that the exporter used to indentify what needs to be exported.

CODE:
from mayaTools import alembicSelectionSet; alembicSelectionSet.run()


###

alembicExportUI.py
_____________________
This UI (though currently ugly) allows you to export an alembic cache with the proper settings needed by Unreal.

You can either export a single alembic file of the entire scene provided the "EXPORT_SET" selection sets are in place. Or, you can export everything individually, based on the respective "EXPORT_SET" selection sets.

CODE:
from mayaTools import alembicExportUI; alembicExportUI.AlembicExportUI().showWindow()