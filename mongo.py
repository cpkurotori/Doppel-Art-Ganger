from flask import flash, redirect, url_for
from flask_mongoalchemy import MongoAlchemy
from datetime import timedelta, datetime
from db import *
import cognitive_face as CF
import os, gridfs
from werkzeug.utils import secure_filename
from pymongo import database, MongoClient
from azure.storage.file import ContentSettings, FileService

UPLOAD_FOLDER = 'static/tmp/'

mongo = database.Database(MongoClient(host=DB_URI), name=DB_NAME)
db = MongoAlchemy()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])


class Art(db.Document):
    file_name = db.StringField()
    file_data_id = db.ObjectIdField()
    file_date = db.DateTimeField()
    file_face_id = db.StringField()
    def init(self, file_name, file, file_date):
        print(1)
        self.file_name = file_name
        print(2)
        self.file_date = file_date
        # self.file_data_id = gridfs.GridFS(mongo).put(FS.get_file_to_stream(ACCOUNT_SHARE, None, self.file_name).read())
        #self.file_face_id = self.upload_face(file_url, file)
        print(3)
        self.file_face_id = self.upload_face(UPLOAD_FOLDER+file_name)
        print(4)
        self.file_data_id = gridfs.GridFS(mongo).put(file.read())
        #FS.delete_file(ACCOUNT_SHARE, None, self.file_name)
        self.save()

    def upload_face(self, filename):
        CF.Key.set(SUBSCRIPTION_KEY)
        try:
            return CF.face_list.add_face(filename, 'artwork')['persistedFaceId']
        except CF.CognitiveFaceException:
            print("Bad request adding face to list")
            flash("Make sure the photo only has 1 subject in frame.")
        except Exception as e:
            print(e)
            flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")



def find_similar(filename):
    CF.Key.set(SUBSCRIPTION_KEY)
    faces = CF.face.detect(UPLOAD_FOLDER+filename)
    if len(faces) != 1:
        flash('Make sure the photo only has 1 subject in frame.')
        raise
    return CF.face.find_similars(faces[0]['faceId'], face_list_id='artwork', max_candidates_return=1, mode='matchFace')[0]['persistedFaceId']


def get_photo(face_id):
    "This is going to return the photo information of the given face_id"


