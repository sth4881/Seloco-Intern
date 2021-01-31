import cv2

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

cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

if cap.isOpened():
    cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Video', frame)
            keyCode = cv2.waitKey(1) & 0xFF
            if keyCode==27:
                break
        else:
            print("Can't Read Frame")

cap.release()
cv2.destroyAllWindows()