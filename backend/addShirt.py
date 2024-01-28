import cv2
import cvzone
import os

# def addShirt(frame, landmarks, imgIndex, rightCounter, leftCounter, shirtList, shirtDir, ratio, shirtRatio, speed, rightButtonImg, leftButtonImg):
def addShirt(frame, lmList, imageNumber, counterRight, counterLeft, listShirts, shirtFolderPath, fixedRatio, shirtRatioHeightWidth, selectionSpeed, imgButtonRight, imgButtonLeft):
    # center = bboxInfo["center"]
    lm11 = lmList[11][1:3]
    lm12 = lmList[12][1:3]
    imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

    widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
    print(widthOfShirt)

    imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))

    currentScale = (lm11[0] - lm12[0]) / 190
    offset = int(44 * currentScale), int(48 * currentScale)

    try:
        frame = cvzone.overlayPNG(frame, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
    except:
        pass

    # img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
    # img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

    if lmList[16][1] < 300:
        counterRight += 1
        cv2.ellipse(frame, (139, 360), (66, 66), 0, 0,
                    counterRight * selectionSpeed, (0, 255, 0), 20)
        if counterRight * selectionSpeed > 360:
            counterRight = 0
            if imageNumber < len(listShirts) - 1:
                imageNumber += 1
    elif lmList[15][1] > 900:
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