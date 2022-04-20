# Alexander C. Perez, acperez@syr.edu
import cv2
import numpy as np


def nothing(x):
    # any operation
    pass


cap = cv2.VideoCapture(4)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = 0
    l_s = 0
    l_v = 134
    u_h = 180
    u_s = 166
    u_v = 254

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)

    if len(approx) == 3:
        cv2.putText(frame, 'Triangle', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    elif len(approx) == 4:
        cv2.putText(frame, 'Square', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    elif len(approx) == 5:
        # cv2.putText(frame, 'Pentagon', (x, y),
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        pass

    elif len(approx) == 6:
        # cv2.putText(frame, 'Hexagon', (x, y),
        #            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        pass
    else:
        cv2.putText(frame, 'circle', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

#     print('x coord:', x)
#     print('y coord:', y)
#
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
#
# cap.release()
# cv2.destroyAllWindows()
