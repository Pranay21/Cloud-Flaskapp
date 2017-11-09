import os,time
from flask import Flask, jsonify, request, render_template, make_response, redirect,url_for
import boto3
import json

ACCESS_KEY = 'AKIAJYEYMPPOL7MQPI6A'
SECRET_KEY = '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'

s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
bucket=s3.Bucket('sxa0453')
app = Flask(__name__)

@app.route('/')
def Welcome():
    return render_template('login.html')

@app.route('/login/',methods=['POST','GET'])
def login():
     u_name = request.form['u_name']
     print u_name

     u_pass = request.form['u_pass']
     print u_pass
     content_object = s3.Object('sxa0453', 'users.json')
     file_content = content_object.get()['Body'].read()
     json_content = json.loads(file_content)
     for users in json_content['users']:
        if u_name==users['username'] and u_pass==users['password']:
            return redirect(url_for('index'))

     return render_template('login.html',msg="Invalid user")



@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST','GET'])
def upload():


    if request.method=='POST':
     file = request.files['myFile']
     file_name = file.filename
     print file
     print file_name

     data = file.read()
     bucket.put_object(Key=file_name, Body=data)
     return render_template('result.html', result="File uploaded successfully!!")

@app.route('/view/' ,methods=['GET'])
def view():
	return render_template('view.html', bucket = bucket)

@app.route('/download/', methods=['POST','GET'])
def download():
    temp=0
    filename = request.form['f_name']
    print filename
    for key in bucket.objects.all():
        print key.key
        if key.key==filename:
            body = key.get()['Body'].read()
            response = make_response(body)
            response.headers["Content-Disposition"] = "attachment; filename="+filename
            return response

    return render_template('result.html', result="File doesnt Exists.")


@app.route('/delete/' ,methods=['POST','GET'])
def delete():
    filename = request.form['f_name']
    for key in bucket.objects.all():
        if key.key == filename:
              key.delete()
              return redirect(url_for('view'))

    return render_template('result.html', result="File doesnt Exists.")





port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))