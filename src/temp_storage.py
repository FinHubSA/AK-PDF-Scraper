import os
from pathlib import Path


def get_temp_storage_path():

    path = os.path.join(str(Path.home()), "AaronsKit_PDF_Downloads")

    return path


def rename_file(old_name, new_name):

    os.rename(old_name, new_name)


def delete_files(new_name):

    os.remove(new_name)


def delete_temp_storage(directory):

    os.rmdir(directory)
