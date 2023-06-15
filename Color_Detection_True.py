import cv2
import numpy as np

# imgReal = cv2.imread('objek.jpg')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 10)
# cap.set(cv2.CAP_PROP_CONTRAST, 50)
# cap.set(cv2.CAP_PROP_SATURATION, 50)
cap.set(cv2.CAP_PROP_EXPOSURE, -5.0)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

imgNum = []

# Mean H, S, V
hMean = 0
sMean = 0
vMean = 0


# Value Lower and Upper
hLower = 0
hUpper = 0
sLower = 0
sUpper = 0
vLower = 0
vUpper = 0


# Dummy
update = 0
text = ''
color = (0, 0, 0)

def nothing(self):
    pass


# Create Trackbar
cv2.namedWindow("Setting")
cv2.resizeWindow("Setting", 480, 480)

cv2.createTrackbar('Lower Hue', 'Setting', 0, 180, nothing)
cv2.createTrackbar('Upper Hue', 'Setting', 180, 180, nothing)

cv2.createTrackbar('Lower Sat', 'Setting', 0, 255, nothing)
cv2.createTrackbar('Upper Sat', 'Setting', 255, 255, nothing)

cv2.createTrackbar('Lower Val', 'Setting', 0, 255, nothing)
cv2.createTrackbar('Upper Val', 'Setting', 255, 255, nothing)


# Calculate Mean H,S,V size 5x5
def imgCol(x, y, z):
    imgNum.clear()
    a = 0
    c = -3

    # Nilai pixel x,y
    h = int(hsv[y, x, 0])
    s = int(hsv[y, x, 1])
    v = int(hsv[y, x, 2])

    for i in range(5):
        c = c + 1
        e = -3
        if (x + i) < img.shape[1]:
            for j in range(5):
                if (y + j) < img.shape[0]:
                    hx = int(hsv[y + e, x + c, 0])
                    sx = int(hsv[y + e, x + c, 1])
                    vx = int(hsv[y + e, x + c, 2])
                    if (h - 10) <= hx <= (h + 10) or (s - 70) <= sx <= (s + 70) or (v - 100) <= vx <= (v + 100):
                        a = a + 1
                        e = e + 1
                        imgNum.insert(a, hsv[y + e, x + c, z])
    mean = int(np.mean(imgNum))
    return mean


# Mouse Click
def mouseClick(event, x, y, flags, param):
    global hMean, sMean, vMean, update
    if event == cv2.EVENT_LBUTTONDOWN:
        hMean = imgCol(x, y, 0)
        sMean = imgCol(x, y, 1)
        vMean = imgCol(x, y, 2)
        print(hMean, sMean, vMean)
        update = 1


# Color Detect with Hue Range
def colorTxt():
    global text, color
    if (0 <= hMean < 10):
        text = "Merah"
        color = (0, 0, 255)
        if (sMean <= 80):
            text = "Merah Muda"
            color = (100, 100, 255)
    if (10 <= hMean < 20):
        text = "Orange"
        color = (0, 50, 200)
    if (20 <= hMean < 40):
        text = "Kuning"
        color = (0, 255, 255)
    if (40 <= hMean < 70):
        text = "Hijau"
        color = (0, 255, 0)
        if (sMean <= 80):
            text = "Hijau Muda"
            color = (100, 255, 100)
    if (70 <= hMean < 100):
        text = "Aqua"
        color = (255, 255, 0)
    if (100 <= hMean < 130):
        text = "Biru"
        color = (255, 0, 0)
        if (sMean <= 80):
            text = "Biru Muda"
            color = (255, 100, 100)
    if (130 <= hMean < 170):
        text = "Ungu"
        color = (255, 0, 255)
    if (170 <= hMean < 180):
        text = "Merah"
        color = (0, 0, 255)
        if (sMean <= 80):
            text = "Merah Muda"
            color = (100, 100, 255)
    if (vMean <= 50):
        text = "Hitam"
        color = (125, 125, 125)
    if (sMean <= 30 and vMean > 50):
        text = "Abu"
        color = (50, 50, 50)

# Main Program
while True:
    # Setting Gambar / Camera
    # r = cv2.getTrackbarPos(switch, 'Setting')
    r = 1
    if r == 0:
        img = cv2.resize(imgReal, (480, 360))
        imgSet = cv2.resize(imgReal, (480, 360))
    else:
        _, img = cap.read()
        _, imgSet = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('Lower Hue', 'Setting')
    s1 = cv2.getTrackbarPos('Lower Sat', 'Setting')
    v1 = cv2.getTrackbarPos('Lower Val', 'Setting')

    h2 = cv2.getTrackbarPos('Upper Hue', 'Setting')
    s2 = cv2.getTrackbarPos('Upper Sat', 'Setting')
    v2 = cv2.getTrackbarPos('Upper Val', 'Setting')

    imgSet = cv2.putText(imgSet, "Click Color to Detect", (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 150, 0), 2)
    cv2.imshow("Setting", imgSet)
    cv2.setMouseCallback("Setting", mouseClick)

    if(update == 1):
        update = 0
        colorTxt()
        if(sMean <= 30 and vMean >= 180):
            h1 = cv2.setTrackbarPos('Lower Hue', 'Setting', 0)
            h2 = cv2.setTrackbarPos('Upper Hue', 'Setting', 179)
            s1 = cv2.setTrackbarPos('Lower Sat', 'Setting', 0)
            s2 = cv2.setTrackbarPos('Upper Sat', 'Setting', 75)
            v1 = cv2.setTrackbarPos('Lower Val', 'Setting', 180)
            v2 = cv2.setTrackbarPos('Upper Val', 'Setting', 255)
            #print('Putih')
            text = "Putih"
            color = (160, 160, 160)

        else:
            # Setting Hue
            hUpper = hMean + 10
            hLower = hMean - 10
            if hUpper >= 179:
                hUpper = 179
            if hLower <= 0:
                hLower = 0
            h1 = cv2.setTrackbarPos('Lower Hue', 'Setting', hLower)
            h2 = cv2.setTrackbarPos('Upper Hue', 'Setting', hUpper)

            # Setting Saturation
            sUpper = sMean + 30
            sLower = sMean - 30
            if sUpper >= 255:
                sUpper = 255
            if sLower <= 0:
                sLower = 0
            s1 = cv2.setTrackbarPos('Lower Sat', 'Setting', sLower)
            s2 = cv2.setTrackbarPos('Upper Sat', 'Setting', sUpper)

            # Setting Value
            vUpper = vMean + 50
            vLower = vMean - 50
            if vUpper >= 255:
                vUpper = 255
            if vLower <= 0:
                vLower = 0
            v1 = cv2.setTrackbarPos('Lower Val', 'Setting', vLower)
            v2 = cv2.setTrackbarPos('Upper Val', 'Setting', vUpper)

    h1 = cv2.getTrackbarPos('Lower Hue', 'Setting')
    h2 = cv2.getTrackbarPos('Upper Hue', 'Setting')

    s1 = cv2.getTrackbarPos('Lower Sat', 'Setting')
    s2 = cv2.getTrackbarPos('Upper Sat', 'Setting')

    v1 = cv2.getTrackbarPos('Lower Val', 'Setting')
    v2 = cv2.getTrackbarPos('Upper Val', 'Setting')

    LowerHSV = np.array([h1, s1, v1])
    UpperHSV = np.array([h2, s2, v2])

    mask = cv2.inRange(hsv, LowerHSV, UpperHSV)

    andbit = cv2.bitwise_and(img, img, mask=mask)
    andbit = cv2.putText(andbit, text, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

    cv2.imshow('Masking Image', mask)
    cv2.imshow('Bitwise AND Image', andbit)

    imgBlur = cv2.GaussianBlur(andbit, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 100, 255);
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    cv2.imshow("img Dilate", imgDil)

    contours, _ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        x, y, w, h = cv2.boundingRect(approx)

        if area > 2000:
            # c = cv2.drawContours(img, cnt, -1, (255,0,255), 7)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
            cv2.imshow('Image Box', img)

    if cv2.waitKey(1) & 0XFF == ord('x'):
        break
cap.release()
cv2.destroyAllWindows()