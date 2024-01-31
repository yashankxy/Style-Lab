import os
import cv2
from PoseModule import PoseDetector
from addShirt import addShirt

# Setup video capture and pose detection
videoCap = cv2.VideoCapture(1)
# videoCap = cv2.VideoCapture("Resources/Videos/1.mp4")
videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
poseDetect = PoseDetector()


# Constants and variables for image size and aspect ratio
ratio = 262 / 190
shirtRatio = 581 / 440
imgIndex = 0
rightCounter = 0
leftCounter = 0

# Load images
shirtDir = "Resources/Shirts"
shirtList = os.listdir(shirtDir)
rightButtonImg = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
leftButtonImg = cv2.flip(rightButtonImg, 1)

  

# cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while flag  == True:
    # Capture and detect pose in a frame from the video
    success, frame = videoCap.read()
    frame = poseDetect.findPose(frame)
    
    # Find landmark positions in the frame
    landmarks, bbox = poseDetect.findPosition(frame, bboxWithHands=False, draw=False)
    
    if landmarks:
        # center = bbox["center"]
        frame, imgIndex, rightCounter, leftCounter = addShirt(frame, landmarks, imgIndex, rightCounter, leftCounter, shirtList, shirtDir, ratio, shirtRatio, speed, rightButtonImg, leftButtonImg)
         
    # Close on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        flag = False
    
    # Add a case to capture the frame when the user presses the spacebar
    if cv2.waitKey(1) & 0xFF == 32:
        imgIndex += 1
        cv2.imwrite(f"Resources/Images/{imgIndex}.png", frame)
        print("Image saved successfully!")
      
    # Display the processed frame
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

        
    

# Delete all images in the Resources/Images directory
for file in os.listdir("Resources/Images"):
    os.remove(os.path.join("Resources/Images", file))

# Release the video capture object and close all windows
videoCap.release()
cv2.destroyAllWindows()
