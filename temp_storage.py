import os
from pathlib import Path

class storage:

    def createTempStorage():
        path = os.path.join(str(Path.home()),'TempStorage')
        return(path)
        # if already exists try another name perhaps

    def renameFile(old_name,new_name):
        os.rename(old_name,new_name)   

    def countFiles(directory):
        countfiles=len(os.listdir(directory))
        return(countfiles)

    def deleteTempStorage(directory):
        os.rmdir(directory)
