from werkzeug.utils import secure_filename
from flask import Flask,render_template,request
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import os
app = Flask(__name__)

# Loading our trained model
model = load_model('/home/dikshant/Desktop/pybox/Tomato-Fungal-Disease/tomato.h5')

picfolder = os.path.join('static','upload')
app.config['UPLOAD_FOLDER'] = picfolder
path = "/home/dikshant/Desktop/pybox/Tomato-Fungal-Disease/static/upload"

def model_predict(img_path, model):
	img_pred = image.load_img(img_path,target_size = (150,150))
	img_pred = image.img_to_array(img_pred)
	img_pred = np.expand_dims(img_pred,axis = 0)
	result = model.predict(img_pred)
	if result[0][0] == 1:
		return "Healthy Tomato"
	else:
		return "early blight Tomato"

@app.route("/")
def hello():
	return render_template('index.html')

@app.route("/",  methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file1']
        file1_path = os.path.join(path,secure_filename(f.filename))
        f.save(file1_path)
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename))

        # Make Prediction
        result = model_predict(file1_path, model)
        return render_template('index.html', image12=pic1, final_output=result)
        

if __name__ == '__main__':
    app.run(debug=True)