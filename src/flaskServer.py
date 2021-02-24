import os, sys, json

from flask import Flask, request, redirect, render_template, jsonify, make_response
from face_save import gstreamer_pipeline, face_detector, face_save

app = Flask(__name__) # Flask Class의 인스턴스 생성

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/crop/', methods=['GET', 'POST'])
def crop():
    if request.method == 'GET':
        return render_template('crop.html')
    elif request.method == 'POST':
        name = list(request.json.values())[0] # crop.html 페이지에서 POST방식으로 제출한 id='name'을 json 형식으로 받아옴
        face_save(name)
        return json.dumps("SUCCESS") # JSON Parse해서 클라이언트에 응답

@app.route('/monitor/', methods=['GET', 'POST'])
def monitor():
    if request.method == 'GET':
        path = 'static/img/'
        files = os.listdir(path)
        files.sort() # 파일을 오름차순으로 정렬
        files.reverse() # 파일을 내림차순으로 정렬
        return render_template('monitor.html', path='../'+path, files=files)
    elif request.method == 'POST':
        img = list(request.form.keys())[0] # monitor.html 페이지에서 submit의 name이 지칭하는 파일명 가져오기
        return render_template('display.html', img=img)
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) # 로컬서버로 실행, app.run(host='0.0.0.0')으로 모든 OS에게 접근가능하도록 설정