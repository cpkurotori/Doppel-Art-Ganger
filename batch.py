import os
from config import *
from time import sleep

path = 'static/assets/images/paintings/'
UPLOAD_FOLDER = path


for x in os.listdir(path):
    artwork = Art()
    try:
        with open(path+x) as f:
            import pdb; pdb.set_trace()
            UPLOAD_FOLDER = path
            artwork.init(file_name=x, file=f, file_date=datetime.now())
    except Exception as e:
        print("No work with "+x)
        print(e)
    sleep(4)
