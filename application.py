from config import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_artwork', methods=['GET', 'POST'])
def upload_artwork():
    if request.method == 'POST':
        print(request.files)
        if 'photo-file' not in request.files:
            print('No file part')
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['photo-file']
        if file.filename == '':
            print('No file selected')
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            artwork = Art()
            with open('temp/'+filename, 'rb') as f:
                artwork.init(file_name=filename, file_data=f.read(), file_date=datetime.now())
                return 'Artwork Uploaded'

@app.route('/test')
def test():
    test = Art()
    test.init("NAME", "DATA", datetime.now())
    return 'Test Complete'

PORT = os.getenv('PORT', 8080)
IP = os.getenv('IP', '0.0.0.0')

app.debug = True

app.run(host=IP, port=int(PORT))