from config import *

def retrieve_photo(request):
    if 'photo-file' not in request.files:
        print('No file part')
        flash('No file part')
        raise
    file = request.files['photo-file']
    if file.filename == '':
        print('No file selected')
        flash('No selected file')
        raise
    if file and allowed_file(file.filename):
        return file



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_artwork', methods=['GET', 'POST'])
def upload_artwork():
    if request.method == 'POST':
        try:
            file = retrieve_photo(request)
        except:
            print("Could not retrieve photo")
            return redirect(url_for('index'))
        artwork = Art()
        try:
            artwork.init(file_name=secure_filename(file.filename), file=file, file_date=datetime.now())
            flash("Artwork added...")
        except:
            print("Could not upload to database")
            return 'ERROR! STOP AND TELL CAMERON'  
    return redirect(url_for('index'))


@app.route('/find_doppelartganger', methods=['GET', 'POST'])
def find_dopple():
    if request.method == 'POST':
        try:
            file = retrieve_photo(request)
        except:
            return redirect(url_for('index'))
        try:
            image_name = Art.query.filter(Art.file_face_id == find_similar(file)).first().file_name
            image = gridfs.GridFS(mongo).get_last_version(image_name)
            

        except:
            flash('Bad request.')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)