from flask import Flask, render_template, flash, request, send_file
from content_management import Content
from werkzeug import secure_filename
import os
import awscompute as aws
import dataStorage

TOPIC_DICT  = Content()
# the folder static is for the files for css, img, js files
# the templates folder is for html files 
# keep all python files in same directoory as the flaskbackend.
# To start, run flaskbackend

app = Flask(__name__)

#Added this
app.config['UPLOAD_FOLDER'] = "./Uploads"


@app.errorhandler(404)
def page_not_found(e):
    return "error 404"

@app.errorhandler(405)
def method_not_found(e):
    return "error 405"

@app.route('/', methods = ["GET", "POST"])
def main_page():
    return render_template("base.html")

@app.route('/handle_data', methods =['POST']) 
def handle_data():
    productName = request.form['pname']
    priceAmount = request.form['price']
    uploadFile = request.form['uploadedFile']
    categoryType = request.form['category']
    description = request.form['descrip']
    return request.form['pname']

    #return '{} {}'.format(productName,description)
    #request.form['pname'] request.form['uploadedFile'],request.form['category'],request.form['descrip']

#added
@app.route('/')
def upload_f():
   return render_template('upload.html')

#added
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      

      da = aws.analyze(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))

      category = (da['cat'])
      confidence = (da['conf'])
      productName = request.form['pname']
      image = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename))
      description = request.form['descrip']
      priceAmount = request.form['price']

      output = showResults(category, round(confidence, 2), productName, image, description, priceAmount)
      return render_template('successful.html', output = output)

@app.route('/successful')
def showResults(category,confidence, productName , image , description, priceAmount):
    output2 = str(category) + "," + str(confidence) + "," + str(productName) + "," + str(image) + "," + str(description) + "," + str(priceAmount).replace(',', '~')
    dataStorage.writeData(output2)
    return category, confidence



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) #host='0.0.0.0', port=80
