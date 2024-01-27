import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

# Setup video capture and pose detection
# videoCap = cv2.VideoCapture('Resources/Videos/1.mp4')
videoCap = cv2.VideoCapture(0)
videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
poseDetect = PoseDetector()

# Get list of images in the directory
shirtDir = "Resources/Shirts"
shirtList = os.listdir(shirtDir)

# Constants and variables for image size and aspect ratio
ratio = 262 / 190
shirtRatio = 581 / 440
imgIndex = 0

# Load button images
rightButtonImg = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
leftButtonImg = cv2.flip(rightButtonImg, 1)

# Initialize button press counters
rightCounter = 0
leftCounter = 0

# Selection speed
speed = 5

while True:
    # Capture a frame from the video
    success, frame = videoCap.read()
    # Detect poses in the frame
    frame = poseDetect.findPose(frame)
    
    # Find landmark positions in the frame
    landmarks, bbox = poseDetect.findPosition(frame, bboxWithHands=True, draw=True)
    
    if landmarks:
        # Get positions of landmarks 11 and 12
        landmark11 = landmarks[11][1:3]
        landmark12 = landmarks[12][1:3]
        # Load the current shirt image
        shirtImg = cv2.imread(os.path.join(shirtDir, shirtList[imgIndex]), cv2.IMREAD_UNCHANGED)




        # Calculate the shirt image width based on the distance between landmarks 11 and 12
        shirtWidth = int((landmark11[0] - landmark12[0]) * ratio)
        
        
        # Resize the shirt image
        if shirtWidth < 0 and shirtRatio < 0:
            shirtWidth = 0
            shirtRatio = 0
        shirtImg = cv2.resize(shirtImg, (shirtWidth, int(shirtWidth * shirtRatio)))
        print("Width of shirt", shirtWidth)


        # Calculate the current scale and offset
        scale = (landmark11[0] - landmark12[0]) / 190
        offset = int(44 * scale), int(48 * scale)

        # Overlay the shirt image onto the frame
        try:
            frame = cvzone.overlayPNG(frame, shirtImg, (landmark12[0] - offset[0], landmark12[1] - offset[1]))
        except:
            pass

        # Overlay the button images onto the frame
        frame = cvzone.overlayPNG(frame, rightButtonImg, (1074, 293))
        frame = cvzone.overlayPNG(frame, leftButtonImg, (72, 293))

        # Check if the user is pointing to the right button
        if landmarks[16][1] < 300:
            # Increment the right counter and draw a progress indicator
            rightCounter += 1
            cv2.ellipse(frame, (139, 360), (66, 66), 0, 0,
                        rightCounter * speed, (0, 255, 0), 20)
            # If the progress indicator completes a full circle, change the current shirt image
            if rightCounter * speed > 360:
                rightCounter = 0
                if imgIndex < len(shirtList) - 1:
                    imgIndex += 1
        # Check if the user is pointing to the left button
        elif landmarks[15][1] > 900:
            # Increment the left counter and draw a progress indicator
            leftCounter += 1
            cv2.ellipse(frame, (1138, 360), (66, 66), 0, 0,
                        leftCounter * speed, (0, 255, 0), 20)
            # If the progress indicator completes a full circle, change the current shirt image
            if leftCounter * speed > 360:
                leftCounter = 0
                if imgIndex > 0:
                    imgIndex -= 1
        else:
            # If the user is not pointing to any button, reset the counters
            rightCounter = 0
            leftCounter = 0

    # Display the processed frame
    cv2.imshow("Frame", frame)
    # Wait for a short delay before processing the next frame
    cv2.waitKey(1)