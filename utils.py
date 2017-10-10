from config import CF, bucket, datetime, time, Art, db
import os, sys
from flask_mongoalchemy import session

def update():
    try:
        FL = CF.face_list.get('artwork')
        print("Current Face List length == {}".format(len(FL['persistedFaces'])))
    except CF.util.CognitiveFaceException as e:
        # BREAKING ABSTRACTION -- COULDN'T FIND METHOD TO RETRIEVE ERROR CODE
        error = str(e)
        code_start = error.find('\tcode') + 7
        code_end = error.find('\n', code_start)
        if error[code_start:code_end] == 'FaceListNotFound':
            CF.face_list.create('artwork')

    for page in bucket.list_blobs().pages:
        for blob in page:
            if not Art.query.filter(Art.file_name == blob.name).count():
                artwork = Art()
                try:
                    artwork.init(file_name=blob.name, file=blob, file_date=datetime.now())
                    time.sleep(4) # wait 4 seconds so the API isn't accessed too many times (20/minute is the limit)
                except Exception as e:
                    print(e)
                    print("Failed to upload {}".format(blob.name))

order = {'mf':True, 'mb':True, 'gs':True}

def rm(order=order):
    assert os.path.isfile('remove.py'), "Need the remove.py containing a variable REMOVE which contains a list of filenames that need to be removed from MongoDB, Microsoft Face List, and Google Storage"
    from remove import REMOVE as remove
    for filename in remove:
        try:
            db_query = Art.query.filter(Art.file_name == filename)
            if order['mf']:
                print("Removing from Microsoft Face List")
                CF.face_list.delete_face('artwork', db_query.first().file_face_id)
                print("Removed")
            try:
                if order['mb']:
                    print("Removing from MongoDB")
                    session.RemoveQuery(Art, db.session).filter(Art.file_name == filename).execute()
                    print("Removed")
                try:
                    if order['gs']:
                        print("Deleting from Google Storage")
                        bucket.get_blob(filename).delete()
                        print("Deleted")
                except Exception as gserror:
                    print(gserror)
                    print("Failed to delete from Google Storage")
            except Exception as mdberror:
                print(mdberror)
                print("Failed to remove from MongoDB")
                print("Was not removed from Google Storage")
        except Exception as mflerror:
                print(mflerror)
                print("Failed to remove from Microsoft Face List")
                print("Was not removed from MongoDB")
                print("Was not deleted from Google Storage")

assert len(sys.argv) >= 2, "Need a command"
if sys.argv[1] == 'update':
    update()
elif sys.argv[1] == 'remove':
    rm()
else:
    print("No valid command matching given argument: {}".format(sys.argv[1]))