import os
from pathlib import Path


def get_temp_storage_path():

    path = os.path.join(str(Path.home()), "AaronsKit_PDF_Downloads")

    return path


def get_storage_path():

    src_directory = os.path.dirname(__file__)

    return src_directory


def misc_path():

    src_directory = get_storage_path()

    misc_directory = os.path.normpath(src_directory + os.sep + os.pardir)

    return misc_directory


def rename_file(old_name, new_name):

    os.rename(old_name, new_name)


def delete_files(new_name):

    os.remove(new_name)


def delete_temp_storage(directory):

    os.rmdir(directory)
