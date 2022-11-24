import os, time
from dask import dataframe as df1
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from script import process, results
import threading


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

@app.route('/index', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
                save_location = os.path.join('input', new_filename)
                file.save(save_location)
                output_file_name = f'processed_{str(datetime.now())}.csv'
                file.save(os.path.join('processing', output_file_name))
                x = threading.Thread(target=process, args=(save_location, output_file_name))
                x.start()
                return render_template('uploadsuccess.html', fileid=output_file_name) 

        return render_template('upload.html')

@app.route('/download')
def download():
    return render_template('download.html', files=os.listdir('output'))
    

@app.route('/request', methods=['POST'])
def handle_data():
    requestedfile = request.form['filename']
    under_processing = os.listdir('processing')
    files = os.listdir('output')
    return results(requestedfile, files, under_processing)
     
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)   

