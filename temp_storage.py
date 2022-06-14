import os
from pathlib import Path

class storage:

    def getTempStoragePath():
        path = os.path.join(str(Path.home()),'AaronsKitTempStorage')
        return(path)
        # if already exists try another name perhaps

    def renameFile(old_name,new_name):
        os.rename(old_name,new_name)   

    def countFiles(directory):
        countfiles=len(os.listdir(directory))
        return(countfiles)

    def deleteTempStorage(directory):
        os.rmdir(directory)
