import os
import cv2
from cvzone.PoseModule import PoseDetector
from addShirt import addShirt

# Setup video capture and pose detection
videoCap = cv2.VideoCapture(1)
# videoCap = cv2.VideoCapture("Resources/Videos/1.mp4")
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
speed = 10

while True:
    # Capture a frame from the video
    success, frame = videoCap.read()
    # Detect poses in the frame
    frame = poseDetect.findPose(frame)
    
    # Find landmark positions in the frame
    landmarks, bbox = poseDetect.findPosition(frame, bboxWithHands=False, draw=False)
    
    if landmarks:
        # center = bbox["center"]
        frame, imgIndex, rightCounter, leftCounter = addShirt(frame, landmarks, imgIndex, rightCounter, leftCounter, shirtList, shirtDir, ratio, shirtRatio, speed, rightButtonImg, leftButtonImg)
        
    # Display the processed frame
    cv2.imshow("Frame", frame)
    # Wait for a short delay before processing the next frame
    cv2.waitKey(1)