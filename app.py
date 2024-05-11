from flask import Flask, render_template, request
import os
import time
from text_extraction import *
from address_detection import *

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads_folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        start_time = time.time()
        # Extract text from the uploaded file
        text = text_from_any_documents(file_path)
        subtexts = split_text(text, words_per_subtext=350, word_overlap=20)

        # Extract addresses using BERT
        # addresses, scores = extract_address_using_bert(subtexts)

        addresses, scores = process_subtexts(subtexts)
        # print(addresses)

        end_time = time.time()  # Enregistrez le temps de fin
        processing_time = end_time - start_time 
        # print(processing_time)


        result_data = zip(addresses, scores)

# Render the result on the web page
        return render_template('result.html', filename=file.filename, result_data=result_data, processing_time=processing_time)


if __name__ == '__main__':
    app.run(port=8080, debug=True)

