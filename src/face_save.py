import numpy as np
import cv2

from os import makedirs
from os.path import isdir

# 사진을 200x200 사이즈로 crop 후에 회색 바탕으로 바꿔서 저장
face_dirs = 'static/faces/'

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

# 얼굴을 인식했는지 판단하는 메소드
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    faces = face_cascade.detectMultiScale(blur, 1.3, 5)

    # 얼굴을 인식하지 못하면 None 리턴(안 써주면 오류 발생)
    if faces is ():
        return None

    for(x, y, w, h) in faces:
        roi = img[y:y+h, x:x+w]
    return roi

# 얼굴을 인식하면 jpg 파일로 저장하는 메소드
def face_save(name):
    user_dirs = face_dirs+name+'/'

    # 해당 디렉토리가 존재하지 않으면 생성
    if not isdir(user_dirs):
        makedirs(user_dirs)

    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow("Face Cropper", cv2.WINDOW_AUTOSIZE)

        count = 1
        while cv2.getWindowProperty("Face Cropper", 0) >= 0:
            ret, img = cap.read()
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # blur = cv2.GaussianBlur(gray, (5,5), 0)
            # faces = face_cascade.detectMultiScale(blur, 1.3, 5)

            # for(x, y, w, h) in faces:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #     roi_gray = gray[y : y+h, x : x+w]
            #     roi_color = img[y : y+h, x : x+w]

            # 카메라를 통해서 읽어온 이미지를 얼굴로 인식할 경우
            face = face_detector(img)
            if face is not None:
                crop = cv2.resize(face, (200, 200)) # 얼굴 사이즈에 맞게 200x200 사이즈로 이미지 축소
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY) # 축소된 이미지를 회색 바탕으로 변경
                cv2.imwrite(user_dirs+str(count)+'.jpg', gray) # 축소되고 회색으로 변경된 이미지를 저장

                cv2.putText(gray, str(count), (25, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2) # 현재 몇번째 이미지를 촬영하고 있는지 좌측 상단에 숫자로 표시
                cv2.imshow("Face Cropper", gray)
                count += 1
            
            keyCode = cv2.waitKey(1) & 0xFF
            if keyCode == 27 or count > 10:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")

if __name__ == "__main__":
    name = input("Name: ")
    face_save(name)