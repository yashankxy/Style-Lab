from flask import Flask, render_template, Response
import cv2
import numpy as np
import time
import pafy
import os
from PoseModule import PoseDetector
from addShirt import addShirt

app = Flask(__name__)
cap1 = cv2.VideoCapture(0)
# video = pafy.new("https://www.youtube.com/watch?v=Ic1f9wKjoJg")
# best = video.getbest(preftype="mp4")
# cap2 = cv2.VideoCapture(best.url)


def generate_frames(videoCap):
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

    speed = 10
    imgIndex = 0
    flag = True   

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
        
        #! Take the photo can show the perfect Fit
        
            
        # Display the processed frame
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)


    # Delete all images in the Resources/Images directory
    for file in os.listdir("Resources/Images"):
        os.remove(os.path.join("Resources/Images", file))

    # Release the video capture object and close all windows
    videoCap.release()
    cv2.destroyAllWindows()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video1')
def video1():
    return Response(generate_frames(cap1), mimetype='multipart/x-mixed-replace; boundary=frame')
# @app.route('/video2')
# def video2():
#     return Response(generate_frames(cap2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 8000)