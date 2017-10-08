from config import *

def retrieve_photo(request):
    if 'photo-file' not in request.files:
        print('No file part')
        flash('No file part')
        raise
    file = request.files['photo-file']
    if file.filename == '':
        print('No file selected')
        raise
    if file and allowed_file(file.filename):
        # import pdb; pdb.set_trace()
        # return FS.create_file_from_stream(ACCOUNT_SHARE, None, secure_filename(file.filename), file.stream, content_settings=ContentSettings(content_type=file.content_type))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_artwork', methods=['GET', 'POST'])
def upload_artwork():
    if request.method == 'POST':
        try:
            filename = retrieve_photo(request)
        except:
            print("Could not retrieve photo")
            return redirect(url_for('index'))
        artwork = Art()
        try:
            with open(app.config['UPLOAD_FOLDER']+filename) as f:
                artwork.init(file_name=filename, file=f, file_date=datetime.now())
            flash("Artwork added...")
            os.remove(app.config['UPLOAD_FOLDER']+filename)
        except:
            print("Could not upload to database")
            return 'ERROR! STOP AND TELL CAMERON'  
    return redirect(url_for('index'))




@app.route('/find_doppelartganger', methods=['GET', 'POST'])
def find_doppel():
    if request.method == 'POST':
        try:
            filename = retrieve_photo(request)
            img_file_name = Art.query.filter(Art.file_face_id == find_similar(filename)).first().file_name
            print("finding image")
            image = gridfs.GridFS(mongo).get(Art.query.filter(Art.file_name == img_file_name).first().file_data_id)
            with open(app.config['UPLOAD_FOLDER']+img_file_name, 'wb') as f:
                f.write(image.read())
        except:
            flash('Bad request.')
            return redirect(url_for('index'))
        return render_template('results.html', user_img=filename, result_img=img_file_name)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)