from config import *

def retrieve_photo(request, bucket, tmp=False):
    if 'photo-file' not in request.files:
        print('No file part')
        flash('No file part')
        raise Exception('No file part')
    print("getting file from quest")
    file = request.files['photo-file']
    if file.filename == '':
        print('No file selected')
        raise Exception('No file selected')
    if file and allowed_file(file.filename):
        # import pdb; pdb.set_trace()
        # return FS.create_file_from_stream(ACCOUNT_SHARE, None, secure_filename(file.filename), file.stream, content_settings=ContentSettings(content_type=file.content_type))
        filename = secure_filename(file.filename)
        if not tmp and bucket.get_blob(filename):
            flash("file already exists")
            raise Exception('File already exists')
        else:
            if tmp and bucket.get_blob(filename):
                print("deleting blob")
                bucket.get_blob(filename).delete()
            blob = bucket.blob(filename)
            print("Uploading from file {}".format(filename))
            blob.upload_from_file(file, content_type=request.files['photo-file'].content_type)
            return filename, bucket.get_blob(filename).public_url
            #return filename


@app.route('/')
def index():
    return render_template('new.html')

@app.route('/upload_artwork', methods=['GET', 'POST'])
def upload_artwork():
    # if request.method == 'POST':
    #     try:
    #         filename = retrieve_photo(request)
    #     except:
    #         print("Could not retrieve photo")
    #         return redirect(url_for('index'))
    #     artwork = Art()
    #     try:
    #         with open(app.config['UPLOAD_FOLDER']+filename) as f:
    #             artwork.init(file_name=filename, file=f, file_date=datetime.now())
    #         flash("Artwork added...")
    #         os.remove(app.config['UPLOAD_FOLDER']+filename)
    #     except:
    #         print("Could not upload to database")
    #         return 'ERROR! STOP AND TELL CAMERON'  
    # return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            filename, url = retrieve_photo(request, bucket)
        except Exception as e:
            print(e)
            print("Could not retrieve photo")
            return redirect(url_for('index'))
        artwork = Art()
        try:
            artwork.init(file_name=filename, file=bucket.get_blob(filename), file_date=datetime.now())
            flash("Artwork added")
        except Exception as e:
            print(e)
            print("Could not upload to database")
            return 'ERROR! STOP AND TELL CAMERON'  
    return redirect(url_for('index'))


@app.route('/find_doppelartganger', methods=['GET', 'POST'])
def find_doppel():
    if request.method == 'POST':
        try:
            filename, user_url = retrieve_photo(request, tmp_bucket, tmp = True)
            print("finding image")
            similar = Art.query.filter(Art.file_face_id == find_similar(StringIO.StringIO(tmp_bucket.get_blob(filename).download_as_string())))
            print(similar.first().file_name)
            art_image = bucket.get_blob(similar.first().file_name)
            print (art_image.public_url)
            if not art_image:
                print("Removing face {} from Face List".format(similar.file_face_id))
                CF.face_list.delete_face(similar.file_face_id)
                flash("FAIL")
                return ("FAIL")
            print("image found")
        except Exception as e:
            print(e)
            flash('Bad request.')
            return redirect(url_for('index'))
        return render_template('results.html', user_img=filename, result_img=art_image.name, user_image_url=user_url, result_image_url=art_image.public_url)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
