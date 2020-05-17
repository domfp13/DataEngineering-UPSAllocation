# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes

from __future__ import annotations
import os
import itertools
from google.cloud import storage
from google.cloud import pubsub_v1
from sqlalchemy.sql import text
from ast import literal_eval
from typing import Optional

def binary_to_dict(the_binary):
    """This method thansform a binary object to a dictionary"""
    dictionary = literal_eval(str(the_binary))
    return dictionary

def sub(project_id, subscription_name) -> list:
    """Receives messages from a Pub/Sub subscription."""

    # Initialize a Subscriber client
    subscriber = pubsub_v1.SubscriberClient()

    # Create a fully qualified identifier in the form of
    # `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name
    )

    NUM_MESSAGES = 50

    # The subscriber pulls a specific number of messages.
    response = subscriber.pull(subscription_path, max_messages=NUM_MESSAGES)

    ack_ids = []
    files_to_process = []
    for received_message in response.received_messages:

        blob_name = binary_to_dict(received_message.message.attributes).get('objectId')

        if os.path.dirname(blob_name) == 'global/UPS_ALLOCATION':
            files_to_process.append(blob_name)
            ack_ids.append(received_message.ack_id)

    # Acknowledges the received messages so they will not be sent again.
    if len(ack_ids)!=0:
        subscriber.acknowledge(subscription_path, ack_ids)

    subscriber.close()

    return files_to_process

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

def to_gcs_bucket(file_name: str, file_final_path: str) -> None:
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

def download_blob(source_blob_name, destination_file_name) -> None:
    """Downloads a blob from the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.get_bucket('appusma206_apps')
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

def delete_processed_file(file_final_path) -> None:
    os.remove(file_final_path)
    print("File Deleted")
