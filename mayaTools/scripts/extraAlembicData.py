#extraAlembicData.py

"""
For various extra data needed by Unreal when exporting from Maya.

For now, only the start frame of the animation is stored. 
However there is potential for more data to be saved.

The data is saved at the end of the exported alembic file.
"""

from maya import cmds

def writeStartFrame(file):
    """Writes the start frame number to the alembic file.

    Args:
        file : The alembic file.
    """
    startFrame = cmds.playbackOptions(q=1, minTime=1)
    
    with open(file, 'a') as f:
        f.write(f'\nframe_start={startFrame}')