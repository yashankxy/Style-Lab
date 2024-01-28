import cv2
import cvzone
import os

# def addShirt(frame, landmarks, imgIndex, rightCounter, leftCounter, shirtList, shirtDir, ratio, shirtRatio, speed, rightButtonImg, leftButtonImg):
def addShirt(frame, lm_List, imageNumber, counterRight, counterLeft, listShirts, shirtFolderPath, fixedRatio, shirtRatioHeightWidth, selectionSpeed, imgButtonRight, imgButtonLeft):
    # center = bboxInfo["center"]
    landmark11 = lm_List[11][1:3]
    landmark12 = lm_List[12][1:3]
    img_Shirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

    width_of_Shirt = int((landmark11[0] - landmark12[0]) * fixedRatio)
    print(width_of_Shirt)

    img_Shirt = cv2.resize(img_Shirt, (width_of_Shirt, int(width_of_Shirt * shirtRatioHeightWidth)))

    current_Scale = (landmark11[0] - landmark12[0]) / 190
    offset = int(44 * current_Scale), int(48 * current_Scale)

    try:
        frame = cvzone.overlayPNG(frame, img_Shirt, (landmark12[0] - offset[0], landmark12[1] - offset[1]))
    except:
        pass

    # img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
    # img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

    if lm_List[16][1] < 300:
        counterRight += 1
        cv2.ellipse(frame, (139, 360), (66, 66), 0, 0,
                    counterRight * selectionSpeed, (0, 255, 0), 20)
        if counterRight * selectionSpeed > 360:
            counterRight = 0
            if imageNumber < len(listShirts) - 1:
                imageNumber += 1
    elif lm_List[15][1] > 900:
        counterLeft += 1
        cv2.ellipse(frame, (1138, 360), (66, 66), 0, 0,
                    counterLeft * selectionSpeed, (0, 255, 0), 20)
        if counterLeft * selectionSpeed > 360:
            counterLeft = 0
            if imageNumber > 0:
                imageNumber -= 1

    else:
        counterRight = 0

    return frame, imageNumber, counterRight, counterLeft