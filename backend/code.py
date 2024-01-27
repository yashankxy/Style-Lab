# Import necessary libraries
import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

# Initialize video capture and pose detector
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set the width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set the height
detector = PoseDetector()

# Get the list of shirt images in the folder
shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

# Define some constants and variables related to the size and aspect ratio of the shirt imagesx
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0

# Load images for left and right buttons
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

# Initialize counters for left and right button presses
counterRight = 0
counterLeft = 0

# Define the speed of selection (how fast the progress indicator grows)
selectionSpeed = 5

# Main loop
while True:
    # Read a frame from the video
    success, img = cap.read()
    # Detect poses in the frame
    img = detector.findPose(img)
    
    # Find the positions of landmarks in the frame
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=True, draw=True)
    if lmList:
        # Get the positions of landmarks 11 and 12
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        # Load the current shirt image
        imgShirt = cv2.imread(os.path.join(
            shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        # Calculate the width of the shirt image based on the distance between landmarks 11 and 12
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        # Resize the shirt image
        if widthOfShirt > 0 and shirtRatioHeightWidth > 0:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(
                widthOfShirt * shirtRatioHeightWidth)))

        # Calculate the current scale and offset
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        # Try to overlay the shirt image onto the frame
        try:
            img = cvzone.overlayPNG(
                img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        # Overlay the left and right button images onto the frame
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Check if the user is pointing to the right button
        if lmList[16][1] < 300:
            # Increment the right counter and draw a progress indicator
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            # If the progress indicator completes a full circle, change the current shirt image
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        # Check if the user is pointing to the left button
        elif lmList[15][1] > 900:
            # Increment the left counter and draw a progress indicator
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            # If the progress indicator completes a full circle, change the current shirt image
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            # If the user is not pointing to any button, reset the counters
            counterRight = 0
            counterLeft = 0

# Initialize variables for gesture recognition
prev_x = None

# Inside your main loop
if lmList:
    # Get x-coordinate of the wrist (or any other landmark)
    wrist_x = lmList[0][1]  # adjust the index based on the landmark you choose

    # Check if the previous x-coordinate is not None
    if prev_x is not None:
        # Check if there's significant horizontal movement
        if abs(wrist_x - prev_x) > gesture_threshold:
            # Determine the direction
            if wrist_x > prev_x:
                # Swipe Right
                print("Swipe Right")
            else:
                # Swipe Left
                print("Swipe Left")

    # Update the previous x-coordinate
    prev_x = wrist_x

    # Display the processed frame
    cv2.imshow("Image", img)
    # Wait for a short delay before processing the next frame
    cv2.waitKey(1)
