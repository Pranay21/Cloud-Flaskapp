# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#REFERENCES
#http://stackoverflow.com/questions/27628053/uploading-and-downloading-files-with-flask
#http://code.runnable.com/UiIdhKohv5JQAAB6/how-to-download-a-file-generated-on-the-fly-in-flask-for-python
#http://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
#http://pythoncentral.io/hashing-files-with-python/
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
