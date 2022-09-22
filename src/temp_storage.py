import os
from pathlib import Path


def get_temp_storage_path():

    path = os.path.join(str(Path.home()), "AaronsKit_PDF_Downloads")

    return path


def rename_file(old_name, new_name):

    os.rename(old_name, new_name)


# def count_files(directory):

#     countfiles = len(os.listdir(directory))

#     return countfiles


# def delete_temp_storage(directory):

#     os.rmdir(directory)
