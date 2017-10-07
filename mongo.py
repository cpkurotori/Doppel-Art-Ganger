from flask import flash, redirect, url_for
from flask_mongoalchemy import MongoAlchemy
from datetime import timedelta, datetime
from db import SUBSCRIPTION_KEY
import cognitive_face as CF
import os

db = MongoAlchemy()

class Art(db.Document):
    file_name = db.StringField()
    file_data = db.StringField()
    file_date = db.DateTimeField()
    def init(self, file_name, file_data, file_date):
        self.file_name = file_name
        self.file_data = file_data
        self.file_date = file_date
        self.face_id = upload_face(self, file_name, file_data)
        self.save()

    def upload_face(self, filename, data):
        with open('temp/'+filename, 'wb') as f:
            f.write(data)
            f.close()
        CF.Key.set(SUBSCRIPTION_KEY)
        try:
            result = CF.face.detect('temp'+filename)
        except:
            print("Bad request.")
            flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")
            return url_for('index')
        if len(result != 1):
            flash("Make sure the photo only has 1 subject in frame.")
            return url_for('index')
        else:
            width, top, height, left = str(result[0]['width']), str(result[0]['top']), str(result[0]['height']), str(result[0]['left'])
            try:
                return CF.face.face_list.add_face(faceListId='artwork', targetFace=left+','+top+','+width+','+height)['persistedFaceId']
            except:
                print("Bad request.")
                flash("Upload failed. Please try again. If you keep receiving this error, please try another photo.")
                return url_for('index')






