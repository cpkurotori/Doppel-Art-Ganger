from flask import Flask, request
import os#, logging
# import cloudstorage as gcs
# from google.appengine.api import app_identity
from mongo import *
from db import DB_NAME, DB_URI
from flask import render_template
from mongo import *

app = Flask(__name__)

# DB_URI is in the db.py file
app.config['MONGOALCHEMY_DATABASE'] = DB_NAME
app.config['MONGOALCHEMY_CONNECTION_STRING'] = DB_URI

# initialize the database
db.init_app(app)

# upload specs
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# secret key
app.secret_key = 'XqRByek'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get(self):
#   bucket_name = os.environ.get('BUCKET_NAME',
#                                app_identity.get_default_gcs_bucket_name())

#   self.response.headers['Content-Type'] = 'text/plain'
#   self.response.write('Demo GCS Application running from Version: '
#                       + os.environ['CURRENT_VERSION_ID'] + '\n')
#   self.response.write('Using bucket name: ' + bucket_name + '\n\n')

# def create_file(self, filename):
#   """Create a file.

#   The retry_params specified in the open call will override the default
#   retry params for this particular file handle.

#   Args:
#     filename: filename.
#   """
#   self.response.write('Creating file %s\n' % filename)

#   write_retry_params = gcs.RetryParams(backoff_factor=1.1)
#   gcs_file = gcs.open(filename,
#                       'w',
#                       content_type='text/plain',
#                       options={'x-goog-meta-foo': 'foo',
#                                'x-goog-meta-bar': 'bar'},
#                       retry_params=write_retry_params)
#   gcs_file.write('abcde\n')
#   gcs_file.write('f'*1024*4 + '\n')
#   gcs_file.close()
#   self.tmp_filenames_to_clean_up.append(filename)

#   def read_file(self, filename):
#   self.response.write('Abbreviated file content (first line and last 1K):\n')

#   gcs_file = gcs.open(filename)
#   self.response.write(gcs_file.readline())
#   gcs_file.seek(-1024, os.SEEK_END)
#   self.response.write(gcs_file.read())
#   gcs_file.close()