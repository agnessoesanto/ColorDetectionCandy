import cv2
import numpy as np


#Koneksi Modbus (PyModbus)
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="127.0.0.1", port=502, unit_id=1, auto_open=True)
# 192.168.1.101
# 127.0.0.1

# WebCamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 10)
# cap.set(cv2.CAP_PROP_CONTRAST, 50)
# cap.set(cv2.CAP_PROP_SATURATION, 50)
cap.set(cv2.CAP_PROP_EXPOSURE, -5.0)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)


# lampu putih
hLower_GlacierFreshMint = 98
hUpper_GlacierFreshMint = 118
sLower_GlacierFreshMint = 6
sUpper_GlacierFreshMint = 119
vLower_GlacierFreshMint = 148
vUpper_GlacierFreshMint = 255

#Ricola Lemon Mint (Yellow)
hLower_LemonMint = 16
hUpper_LemonMint = 36
sLower_LemonMint = 58
sUpper_LemonMint = 254
vLower_LemonMint = 111
vUpper_LemonMint = 255


listItem = []


detectGlacierFreshMint = 0
detectLemonMint = 0

glacierMint = 0
lemonMint = 0

dummyGlacierFreshMint = 0
dummyLemonMint = 0


dummyReadReg = 0




def getContours(img, hsv, upperHSV, lowerHSV):
    mask = cv2.inRange(hsv, lowerHSV, upperHSV)
    andbit = cv2.bitwise_and(img, img, mask=mask)

    imgBlur = cv2.GaussianBlur(andbit, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(imgGray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours

while True:
    # Setting Gambar / Camera

    _, img = cap.read()
    _, imgSet = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # untuk memasukkan data kedaam list array
    # Ricola Glacier Fresh Mint
    LowerHSV_GlacierFreshMint = np.array([hLower_GlacierFreshMint, sLower_GlacierFreshMint, vLower_GlacierFreshMint])
    UpperHSV_GlacierFreshMint = np.array([hUpper_GlacierFreshMint, sUpper_GlacierFreshMint, vUpper_GlacierFreshMint])

    # Ricola Lemon Mint
    LowerHSV_LemonMint = np.array([hLower_LemonMint, sLower_LemonMint, vLower_LemonMint])
    UpperHSV_LemonMint = np.array([hUpper_LemonMint, sUpper_LemonMint, vUpper_LemonMint])


    contours_GlacierFreshMint = getContours(img, hsv, UpperHSV_GlacierFreshMint, LowerHSV_GlacierFreshMint)
    contours_LemonMint = getContours(img, hsv, UpperHSV_LemonMint, LowerHSV_LemonMint)



    # Ricola Glacier Fresh Mint
    for cnt in contours_GlacierFreshMint:
        area = cv2.contourArea(cnt) #deteksi warna dominan
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        x, y, w, h = cv2.boundingRect(cnt)
        #print(area)

        if area > 30000:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
            img = cv2.putText(img, "GlacierFreshMint", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
            cv2.imshow('Image Box', img)
            glacierMint += 1

    if(glacierMint > 0):
        glacierMint = 0
        detectGlacierFreshMint = 1
    else:
        detectGlacierFreshMint = 0

    # Ricola Lemon Mint
    for cnt in contours_LemonMint:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # print(area)

        x, y, w, h = cv2.boundingRect(approx)

#22500
        if area > 30000:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
            img = cv2.putText(img, "LemonMint", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
            cv2.imshow('Image Box', img)
            lemonMint += 1

    if(lemonMint > 0):
        lemonMint = 0
        detectLemonMint = 1
    else :
        detectLemonMint = 0

    # if (len(contours_GlacierFreshMint) == 0):
    #     detectGlacierFreshMint = 0
    # if (len(contours_LemonMint) == 0):
    #     detectLemonMint = 0


    if(detectGlacierFreshMint ^ dummyGlacierFreshMint == True) :
        dummyGlacierFreshMint = detectGlacierFreshMint
        if(detectGlacierFreshMint == 1):
            listItem.append(2)

    if (detectLemonMint ^ dummyLemonMint == True):
        dummyLemonMint = detectLemonMint
        if (detectLemonMint == 1):
            listItem.append(1)

    print(listItem)

    c.write_single_register(140, len(listItem))

    pickupObj = c.read_holding_registers(130, 10)[9]
    if (pickupObj ^ dummyReadReg == True):
        dummyReadReg = pickupObj
        if (pickupObj == 1):
            if (len(listItem) < 1) :
                c.write_single_register(138, 0)
            else:
                c.write_single_register(138, listItem[0])
                listItem.pop(0)

    none = c.read_holding_registers(140, 10)[3]
    if none == 1:
        c.write_single_register(138, 0)

    cv2.imshow('Image Box', img)

    if cv2.waitKey(1) & 0XFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()