import os, sys

from flask import Flask, request, redirect, render_template, send_file

app = Flask(__name__) # Flask Class의 인스턴스 생성

@app.route('/') # Flask에게 어떤 URL이 작성한 함수를 실행시킬지 알려줌
@app.route('/index')
def index(): # 브라우저에 보여줄 메시지를 리턴하는 함수
    return render_template('index.html') # 단순히 메세지를 리턴하지 않고 template(html)로 이동시킴

@app.route('/test/', methods=['GET', 'POST']) # POST 형식으로 선언
def test():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        value = request.form['aaa'] # test.html에서 input name이 aaa인 정보를 받아옴
        return value # 받아온 정보는 value에 담기게 되고 그것을 최종적으로 반환

@app.route('/monitor/', methods=['GET', 'POST'])
def monitor():
    if request.method == 'GET':
        path = 'static/pictured/'
        files = os.listdir(path)
        files.sort() # 파일을 오름차순으로 정렬
        files.reverse() # 파일을 내림차순으로 정렬
        return render_template('monitor.html', path='../'+path, files=files)
    elif request.method == 'POST':
        img = request.form
        return "pictured/2021-02-02_11:58:11_User:Jinho.jpg"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True) # 로컬서버로 실행, app.run(host='0.0.0.0')으로 모든 OS에게 접근가능하도록 설정