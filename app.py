import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
# import our OCR function
from ocr_main import ocr

# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # call the OCR function on it
            imagename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
            img_src = UPLOAD_FOLDER + imagename
            details, message  = ocr(img_src)
            print(str(message))

            if type(details) is dict:
                return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=str(message),
                                   img_src=UPLOAD_FOLDER + imagename,
                                   pname=str(details['Name']), fname = str(details['Father Name']),
                                   dob=str(details['Date of Birth']), panid= str(details['PAN']))
            # extract the text and display it
            else:
                return render_template('upload.html',
                                       msg='Successfully processed',
                                       extracted_text=str(details)+'\n'+str(message),
                                       img_src=UPLOAD_FOLDER + imagename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()