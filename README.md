# 🎨 Virtual Painter

Unlock your creativity with **Virtual Painter**! This project uses OpenCV and MediaPipe to turn your webcam into an interactive painting tool, detecting hand gestures for drawing in real-time. 


---

## 💡 Project Overview
The Virtual Painter interprets hand gestures to let you draw on a virtual canvas. Here’s how it works:

- 🖐️ **Hand Detection**: Uses MediaPipe to detect hands in the camera feed.
- ✌️ **Gesture Recognition**:
    - **Index finger up** ➡ Draw on the canvas
    - **Index and middle fingers up** ➡ Selection mode for color or brush size
- 📍 **Finger Tip Detection**: Tracks the finger tips for accurate line drawing.
- 🎥 **Canvas Masking**: Draws on a black canvas, which is then combined with the actual frame.

---

## 🚀 Getting Started

### Prerequisites
Make sure to install the necessary libraries to run this project:
```bash
pip install -r requirements.txt
```

Running the Project:<br/>
Once dependencies are installed, run the project with:
```
python main.py
```

### 🛠️ Tech Stack

- Python 🐍
- OpenCV for computer vision
- MediaPipe for hand tracking and gesture recognition
