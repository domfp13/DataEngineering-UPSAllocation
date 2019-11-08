# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

import os
import itertools
from google.cloud import storage
from sqlalchemy.sql import text

def get_files_in_directory(files_directory_path: str) -> list:
    """This method returns a list of the files in a directory"""
    return  os.listdir(files_directory_path)

def check_if_list_Null(list: list) -> bool:
    """This method returns if a list is empty"""
    return len(list) == 0

def clean_string(text: str) -> str:
    if text != 'None':
        return text.strip().upper()
    else:
        return ""
def is_int(text: str) -> bool:
    try:
        return isinstance(text, int)
    except Exception as e:
        return False

def to_gcs_bucket(file_name: str, file_final_path: str):
    """
    Writes a string to a gcs bucket.
    :param output: the string
    :param filename: the name of the file to write
    :return: none
    """

    dictionary = {'bucketName': 'appusma206_apps_output', #gs://appusma206_apps_output
                  'destination_blob_name': f'appusma206_apps/UPS_ALLOCATION/{file_name}',
                  'source_file_name': f'{file_final_path}'}
    storage_client = storage.Client()
    storage_client.get_bucket(dictionary['bucketName']).blob(dictionary['destination_blob_name'])\
        .upload_from_filename(dictionary['source_file_name'])
    print("File uploaded")

def delete_processed_file(file_final_path):
    os.remove(file_final_path)
    print("File Deleted")
