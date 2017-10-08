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
        print(file)
        if file.filename == '':
            print('No file selected')
            flash('No selected file')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.create_file(filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            artwork = Art()
            # with open(app.config['UPLOAD_FOLDER']+filename, 'rb') as f:

            artwork.init(file_name=filename, file=file, file_date=datetime.now())
            #except: 
            #    return 'ERROR! STOP AND TELL CAMERON'
            # os.remove(app.config['UPLOAD_FOLDER']+filename)    
            return redirect(url_for('index'))

@app.route('/test')
def test():
    test = Art()
    test.init("NAME", "DATA", datetime.now())
    return 'Test Complete'

app.debug = True