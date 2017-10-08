from flask import flash, redirect, url_for
from flask_mongoalchemy import MongoAlchemy
from datetime import timedelta, datetime
from db import *
import cognitive_face as CF
import os, gridfs
from werkzeug.utils import secure_filename
from pymongo import database, MongoClient

mongo = database.Database(MongoClient(host=DB_URI), name=DB_NAME)
db = MongoAlchemy()

class Art(db.Document):
    file_name = db.StringField()
    file_data_id = db.ObjectIdField()
    file_date = db.DateTimeField()
    file_face_id = db.StringField()
    def init(self, file_name, file_data, file_date):
        self.file_name = file_name
        self.file_date = file_date
        try:
            self.file_face_id = self.upload_face(file_name)
            self.file_data_id = gridfs.GridFS(mongo).put(file_data)
            self.save()
        except:
            raise 

    def upload_face(self, filename):
        CF.Key.set(SUBSCRIPTION_KEY)
        # try:
        #     result = CF.face.detect('temp/'+filename)
        #     print(result)
        #     print(type(result))
        # except:
        #     print("Bad request creating face")
        #     flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")
        #     return url_for('index')
        # if len(result) != 1:
        #     flash("Make sure the photo only has 1 subject in frame.")
        #     return url_for('index')
        # else:
        #     width, top, height, left = str(result[0]['faceRectangle']['width']), str(result[0]['faceRectangle']['top']), str(result[0]['faceRectangle']['height']), str(result[0]['faceRectangle']['left'])
        #try:
        try:
            return CF.face_list.add_face('temp/'+filename, 'artwork')['persistedFaceId']
        except CF.CognitiveFaceException:
            print("Bad request adding face to list")
            flash("Make sure the photo only has 1 subject in frame.")
        except Exception as e:
            print(e)
            flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")
        raise







