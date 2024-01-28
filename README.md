# Style Lab
## Description
Introducing "StyleLab," an innovative app revolutionizing the way you discover and refine your personal fashion sense. Using cutting-edge computer vision technology, StyleLab enables you to virtually try on a vast array of clothing items, all from the comfort of your device.

With a user-friendly interface, simply activate your camera to generate a lifelike digital representation of yourself. StyleLab employs intricate algorithms to identify key body landmarks, ensuring a precise and realistic fit for every garment.

Navigate through an immersive virtual wardrobe, mix and match outfits, and witness the transformation in real-time. The app's intuitive design and responsive features make the exploration seamless, providing you with a dynamic and interactive fashion journey.

StyleLab isn't just about trying on clothes; it's about discovering and embracing your signature style with the help of cutting-edge technology. Elevate your fashion experience, redefine your wardrobe, and confidently embrace a style that's uniquely yours with StyleLab.

### Main.py
This script creates a virtual clothing try-on application using a webcam. Here's a brief rundown of its operation:

Setup: Initializes webcam capture, pose detection, and loads shirt and button images.
Processing Loop: Continuously captures frames from the webcam and detects human poses in each frame.
Shirt Display: Calculates where to overlay a shirt image on the person based on pose detection.
Interaction: Allows users to 'press' virtual left and right buttons by moving their hands, changing the displayed shirt.
Feedback: Provides visual feedback, such as progress indicators, when interacting with buttons.
Output: Displays the webcam feed with the virtual shirt and buttons, updating in real-time for an interactive try-on experience.
## Installation
Describe the installation process here. For example:

```cd backend```
```pip install -r requirements.txt```
```python main.py```

## Controls
    - Raise Left/Right Hand to switch between photos

