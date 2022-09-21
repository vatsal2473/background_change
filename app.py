from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import cv2
import base64
import os, glob
import segment, bg_editor
import io
from PIL import Image

app = Flask(__name__, template_folder='frontend', static_folder='frontend')
#CORS(app, support_credentials=True)
    
UPLOAD_FOLDER = 'static/uploads/'
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@app.route("/")
def template_test():
    return render_template('index.html')

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/file-upload', methods=['POST'])
#@cross_origin(supports_credentials=True)
def upload_image():

    dir = 'static/uploads'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
    
    dir = 'input/segmented'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output_bg'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)
    
    #category  = request.form.get('human_model', type=str, default='')
    file=request.form.get('file',type = str, default='')

    new_string = file.split(',')[1]

    my_str_as_bytes = str.encode(new_string)
    with open("static/uploads/image.jpg", "wb") as fh:
        fh.write(base64.decodebytes(my_str_as_bytes))

    # for i in os.listdir('static/uploads/'):
    #     print(i)
    #     im = cv2.imread('static/uploads/'+i)
    #     print(im.shape)
    #     im = cv2.resize(im,(768,1024))
    #     print(im.shape)
    #     cv2.imwrite('static/uploads/'+i.split('.')[0]+'.jpg',im)

    #uncomment below two lines to run models
    #segment.main()
    #gb_editor.add_background()

    names = os.listdir('output_bg')
    output = []
    for i in range(len(names)):
        print(names[i])
        file_path = 'output_bg/' + names[i]
        print(file_path)
        encoded_img = get_response_image(file_path)
        
        output.append(encoded_img)

    response = jsonify({'output': output})
    return (response)
    
if __name__ == "__main__":
    app.run()