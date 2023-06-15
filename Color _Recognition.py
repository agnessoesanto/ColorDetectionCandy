import cv2
from Modbus import get_limits
from PIL import Image

yellow = [0, 255, 255]
blue = [255, 0, 0]

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, frame = cap.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Warna Kuning
    lowerLimit, upperLimit = get_limits(color=yellow)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    print(mask)
    bboxYellow = mask_.getbbox()
    if bboxYellow is not None:
        x1, y1, x2, y2 = bboxYellow
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, "yellow", (10, 50), 0, 1, (0, 255, 255), 2)

    # Warna Biru
    mask_ = Image.fromarray(mask)
    lowerLimit, upperLimit = get_limits(color=blue)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    bboxBlue = mask_.getbbox()
    if bboxBlue is not None:
        x1, y1, x2, y2 = bboxBlue
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, "blue", (10, 50), 0, 1, (255, 0, 0), 2)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

# # print(img)
# cap.release()
# cv2.destroyAllWindows()