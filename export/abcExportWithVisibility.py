#temp name

"""
FIRST AND FOREMOST -- Test out visibility w Alembics in UE urself
Theory:
The reason it doesn't work, is bc transform data is like a blendshape in Unreal.
It's not ACTUALLY keyed, because then we'd see keys in the sequencer.
So why would visibility act any different? Although I wish it did.

Idea for exporting alembic files AND visibility:
After the alembic export, we query and export a JSON of all the visibility-keyed objects.

The problem:
The typical process in Unreal is to import the alembic, then put it in any sequence when ready.
Unless we make a new sequence for each alembic file, we can't key the visibility of the object.
There needs to be some way to tell Unreal to add the keyed visibility when the Alembic is brought into a sequence
Perhaps this could be done with blueprints.


AUG 2023 UPDATE
To truly key the visibility, each character (or animated geo) must be exported as its OWN FILE.
Meaning that an alembic file featuring 6 characters, all with their own visibilities animated, cannot have individual animated visibility in Unreal
HOWEVER, I have created an alembic importer for unreal that easily allows for multi alembic importing. This could aid in the ease of use of exporting/importing abc files.
ALSO I know for fact that the abc export function in maya accepts multiple agruments, I believe, to create separate files.
"""