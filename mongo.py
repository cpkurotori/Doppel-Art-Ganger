from flask import flash, redirect, url_for
from flask_mongoalchemy import MongoAlchemy
from datetime import timedelta, datetime
from db import *
import cognitive_face as CF
import os, StringIO#, gridfs
from werkzeug.utils import secure_filename
#from pymongo import database, MongoClient
from azure.storage.file import ContentSettings, FileService

UPLOAD_FOLDER = 'static/tmp/'

# mongo = database.Database(MongoClient(host=DB_URI), name=DB_NAME)
db = MongoAlchemy()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])


class Art(db.Document):
    file_name = db.StringField()
    file_date = db.DateTimeField()
    file_face_id = db.StringField()
    file_url = db.StringField()
    def init(self, file_name, file, file_date):
        # FILE is blob to a google storage file
        try:
            self.file_name = file_name
            self.file_date = file_date
            # self.file_data_id = gridfs.GridFS(mongo).put(FS.get_file_to_stream(ACCOUNT_SHARE, None, self.file_name).read())
            #self.file_face_id = self.upload_face(file_url, file)
            #self.file_face_id = self.upload_face(UPLOAD_FOLDER+file_name)
            self.file_face_id = self.upload_face(StringIO.StringIO(file.download_as_string()))
            print("Face added to face list")
            self.file_url = file.public_url
            # print(4)
            # self.file_data_id = gridfs.GridFS(mongo).put(file.read())
            #FS.delete_file(ACCOUNT_SHARE, None, self.file_name)
            self.save()
            print("Art entry added to DB for file: {}".format(self.file_name))
        except Exception as e:
            print(e)
            print("Did not create Database entry for file: {}".format(file_name))
            print("Removing file from Google Storage file: {}".format(file_name))
            if self.file_face_id:
                try:
                    CF.face_list.delete_face('artwork', self.file_face_id)
                    print("Face {} deleted from Facelist".format(file_name))
                except Exception as e:
                    print("Failed to delete {} from Facelist. persistedFaceId = {}".format(file_name, self.file_face_id))
            try:
                file.delete()
                print("File {} deleted".format(file_name))
            except Exception as e:
                print(e)
                print("Failed to delete {}".format(file_name))



    def upload_face(self, file):
        try:
            return CF.face_list.add_face(file, 'artwork')['persistedFaceId']
        except CF.CognitiveFaceException as e:
            print(e)
            print("Bad request adding face to list")
            flash("Make sure the photo only has 1 subject in frame.")
        except Exception as e:
            print(e)
            flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")



def find_similar(file):
    if not CF.Key.get():
        CF.Key.set(SUBSCRIPTION_KEY)
    faces = CF.face.detect(file)
    if len(faces) != 1:
        flash('Make sure the photo only has 1 subject in frame.')
        raise Exception('Multiple subjects or cannot find face')
    return CF.face.find_similars(faces[0]['faceId'], face_list_id='artwork', max_candidates_return=1, mode='matchFace')[0]['persistedFaceId']


