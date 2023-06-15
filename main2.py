import cv2
from pymodbus.client import ModbusTcpClient
from pyModbusTCP.client import ModbusClient

# Robot
c = ModbusClient(host="192.168.1.101", port=502, unit_id=1, auto_open=True)

# Rumah
# c = ModbusClient(host="127.0.0.1", port=502, unit_id=1, auto_open=True)

# c.read_holding_registers(ADDRESS, JUMLAH)
regs_l = c.read_holding_registers(138, 10)
# print(regs_l[0])

var = 0


#----------------------------- < pymodbus ERROR GABISA READ > -----------------------------------#
# # Connect to the Modbus server
# client = ModbusTcpClient('127.0.0.1', port=502)
# client.connect()
#
# # Read the sensor value from the Modbus server
# result = client.read_holding_registers(address=200, count=2, unit=1)
# sensor_value = result
# print (result)

#MODBUS MASUK
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)


    pixel_center = hsv_frame[cy, cx]
    print(pixel_center)

    hue_value = pixel_center[0]



    if hue_value < 5:
        color= "RED"
        # var = 1
    elif hue_value < 22:
        color = "ORANGE"
        # var = 2
    if hue_value < 33:
        color = "YELLOW"
        var = 1
    elif hue_value < 90:
        color = "GREEN"
        # var = 4
    elif hue_value <167:
        color = "BLUE"
        var = 2
    # elif hue_value < 167:
    #     color = "VIOLET"
    #     var = 7
    else:
        color = "UNRECOGNIZE"

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    cv2.putText(frame, color, (10, 70), 5, 3, (b, g, r), 3)
    # cv2.circle(frame, (800,400), 50, (25, 25, 25), 20)
    cv2.rectangle(frame, (700, 630), (1030, 270), (b, g, r), 5)

    #!!ERROR!!
    #client.write_registers(address=200, values=[num_red_pixels], unit=1)
    #client.write_registers(address=200, values=10, unit=1)
    #client.write_registers(200, VALUE)

    c.write_single_register(138, var)


    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cap.destroyAllWindows()
c.close()