from flask import Flask

app = Flask(__name__) # Flask Class의 인스턴스 생성

@app.route('/') # Flask에게 어떤 URL이 작성한 함수를 실행시킬지 알려줌
def hello_world(): # 브라우저에 보여줄 메시지를 리턴하는 함수
    return 'Hello Flask!' # 리턴 메세지

@app.route('/user/<name>') # <name>에 임의 value를 통해서 URL을 접근하면
def user_profile(name): # parameter로 value 삽입
    return 'User %s' % name # 삽입된 value를 %s에 넣고 함께 return

@app.route('/post/<int:user_id>') # 위의 route와 달리 value의 자료형이 int일때만 접근가능
def user_id(user_id):
    return 'ID %s' % user_id

if __name__ == "__main__":
    app.run() # 로컬서버로 실행, app.run(host='0.0.0.0')으로 모든 OS에게 접근가능하도록 설정