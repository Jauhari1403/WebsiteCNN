from flask import Flask, render_template, request # type: ignore
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import PIL
import numpy as np	


app = Flask(__name__)

dic = {0 : 'Sampah Anorganik',  
       1 : 'Sampah Organik',}

model = load_model('Static/Model/Jenis Sampah-Jenis Sampah-100.0.h5', compile=True)

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(224,224))
	i = image.img_to_array(i)/255.0
	i = i.reshape(1, 224,224,3)

	pred = model.predict(i)  # Menggunakan predict()
	p = np.argmax(pred, axis=1)[0]  # Ambil indeks kelas dengan nilai tertinggi
	return dic[p]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("classification.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("classification.html", prediction = p, img_path = img_path)

if __name__ =='__main__':
	#app.debug = True
	app.run(host='0.0.0.0', port=5000)