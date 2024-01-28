import cv2
import cvzone
import os

def addShirt(frame, lm_List, imgIndex, rightCounter, leftCounter, list_Shirts, shirtDir, fxd_Ratio, shirtRatio_H_W, selectionSpeed, img_switch_Right, img_switch_Left):
    landmark11 = lm_List[11][1:3]
    landmark12 = lm_List[12][1:3]
    img_Shirt = cv2.imread(os.path.join(shirtDir, list_Shirts[imgIndex]), cv2.IMREAD_UNCHANGED)

    width_of_Shirt = int((landmark11[0] - landmark12[0]) * fxd_Ratio)
    print(width_of_Shirt)
    if width_of_Shirt <= 0:
        width_of_Shirt = 1  # or some default value
    img_Shirt = cv2.resize(img_Shirt, (width_of_Shirt, int(width_of_Shirt * shirtRatio_H_W)))

    current_Scale = (landmark11[0] - landmark12[0]) / 190
    offset = int(44 * current_Scale), int(48 * current_Scale)

    try:
        frame = cvzone.overlayPNG(frame, img_Shirt, (landmark12[0] - offset[0], landmark12[1] - offset[1]))
    except:
        pass
    # img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
    # img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))
    if lm_List[16][1] < 300:
        rightCounter += 1
        cv2.ellipse(frame, (139, 360), (66, 66), 0, 0,
                    rightCounter * selectionSpeed, (0, 255, 0), 20)
        if rightCounter * selectionSpeed > 360:
            rightCounter = 0
            if imgIndex < len(list_Shirts) - 1:
                imgIndex += 1
    elif lm_List[15][1] > 900:
        leftCounter += 1
        cv2.ellipse(frame, (1138, 360), (66, 66), 0, 0,
                    leftCounter * selectionSpeed, (0, 255, 0), 20)
        if leftCounter * selectionSpeed > 360:
            leftCounter = 0
            if imgIndex > 0:
                imgIndex -= 1

    else:
        rightCounter = 0

    return frame, imgIndex, rightCounter, leftCounter   