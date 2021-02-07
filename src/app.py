import numpy as np
import cv2
import datetime

from os import listdir, makedirs
from os.path import isdir, isfile, join

# 사진을 200x200 사이즈로 crop 후에 회색 바탕으로 바꿔서 저장
face_dirs = 'static/faces/'
# 회원과 외부인을 가리지 않고 방문한 사람을 모두 촬영해서 웹으로 전송
img_dirs = 'static/img/'

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Jetson Nano에서 Pi Cam을 사용하기 위해서 필요한 메소드(건들지 말것)
def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# 각각의 모델을 트레이닝하는 메소드
def train_model(name):
    path = face_dirs+name+'/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    training_data, labels = [], []
    for i, files in enumerate(onlyfiles):
        img = path + onlyfiles[i]
        gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            continue    
        training_data.append(np.asarray(gray, dtype=np.uint8))
        labels.append(i)
    if len(labels) == 0:
        print("There is no data to train.")
        exit()

    labels = np.asarray(labels, dtype=np.int32)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(training_data), np.asarray(labels))
    print("Model: '"+name+"' Training Complete!!!")
    return model

# 트레이닝을 위한 모든 모델을 불러오는 메소드
def train_models():
    path = face_dirs
    model_dirs = [f for f in listdir(path) if isdir(join(path, f))]

    models = {}
    for model in model_dirs:
        result = train_model(model)
        if result is None:
            continue
        models[model] = result
    return models

# 얼굴을 인식했는지 판단하는 메소드
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    faces = face_cascade.detectMultiScale(blur, 1.3, 5)

    # 얼굴을 인식하지 못하면 None 리턴(안 써주면 오류 발생)
    if faces is ():
        return None
        
    # current = datetime.datetime.now()
    # current_datetime = current.strftime('%Y-%m-%d %H:%M:%S')
    # cv2.imwrite(img_dirs+current_datetime+'.jpg', img) # 얼굴을 인식하면 jpg 파일로 저장

    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
        #roi_gray = gray[y : y+h, x : x+w]
        roi_color = img[y:y+h, x:x+w]
    print('Face Detected')
    return roi_color

# 얼굴을 인식하면 사진촬영해서 저장하고 사용자인지 외부인인지 판별하는 메소드
def face_identification(models):
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow("Face Identification", cv2.WINDOW_AUTOSIZE)

        while cv2.getWindowProperty("Face Identification", 0) >= 0:
            ret, img = cap.read()
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # blur = cv2.GaussianBlur(gray, (5,5), 0)
            # faces = face_cascade.detectMultiScale(blur, 1.3, 5)

            # for(x, y, w, h) in faces:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #     #roi_gray = gray[y : y+h, x : x+w]
            #     roi_color = img[y : y+h, x : x+w]

            # 카메라를 통해서 읽어온 이미지를 얼굴로 인식할 경우
            if face_detector(img) is not None:
                face = cv2.resize(face_detector(img), (200, 200)) # 얼굴 사이즈에 맞게 200x200 사이즈로 이미지 crop
                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) # crop한 이미지를 회색 배경으로 바꿔서 저장

                # 학습한 모델로 예측 시도
                min_score = 999
                min_score_name = ""
                for key, model in models.items():
                    result = model.predict(gray)
                    if min_score > result[1]:
                        min_score = result[1]
                        min_score_name = key

                # result[1]는 신뢰도를 뜻하며, 0에 가까울수록 본인과 일치한다는 의미
                if min_score < 500:
                    confidence = int(100*(1-(result[1])/300))
                    display_string = str(confidence)+'% Confidence it is '+min_score_name
                cv2.putText(img, display_string, (100,120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

                # confidence에 따라서 등록된 사용자인지 외부인인지 판별하여 이미지를 저장
                current = datetime.datetime.now()
                current_datetime = current.strftime('%Y-%m-%d_%H:%M:%S_')
                if confidence >= 80:
                    cv2.putText(img, 'User:'+min_score_name, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imwrite(img_dirs+current_datetime+'User:'+min_score_name+'.jpg', img) # 등록된 사용자로 인식될 경우에 대한 이미지 파일 저장
                    print("User:"+min_score_name)
                else:
                    cv2.putText(img, 'Unknown', (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imwrite(img_dirs+current_datetime+'Unknown.jpg', img) # 외부인으로 인식될 경우에 대한 이미지 파일 저장
                    print("Unknown")

            cv2.imshow("Face Identification", img)
            keyCode = cv2.waitKey(1) & 0xFF
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == "__main__":
    models = train_models()
    face_identification(models)