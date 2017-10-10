from google.cloud import storage
import os

def init(bucket_name):
    storage_client = storage.Client()
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except google.cloud.exceptions.NotFound as e:
        print(e)
        bucket = storage_client.create_bucket(bucket_name)
        print('Bucket {} created'.format(bucket.name))

    return storage_client, bucket
