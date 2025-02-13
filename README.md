# Virtual-Canvas
# Enhanced Virtual Canvas using Hand Tracking

## Overview
This project implements a **virtual drawing canvas** using **Mediapipe Hand Tracking** and **OpenCV**. Users can draw on the screen using their index finger, and a fading bubble effect is applied to strokes. The program also detects hand gestures to clear the canvas when the hand is closed.

## Features
- **Real-time hand tracking** using Mediapipe
- **Draw using index finger**
- **Bubble trail effect** for a dynamic look
- **Clear canvas with a fist gesture**
- **Multi-hand support** (right and left hands have different colors)

## Dependencies
Ensure you have the following installed:
```bash
pip install opencv-python mediapipe numpy
```

## How It Works
1. **Hand Tracking:** Uses Mediapipe's Hand Tracking solution to detect hand landmarks.
2. **Drawing Logic:**
   - The **index finger** is used for drawing.
   - If **other fingers are raised**, drawing stops.
   - A **bubble effect** is added while drawing.
3. **Canvas Clearing:**
   - If a **closed fist** is detected, the canvas is cleared.
4. **Smooth Drawing:** Uses **exponential smoothing** for smooth strokes.
5. **Real-time Video Display:** Uses OpenCV to display the processed frames.

## Usage
Run the script using:
```bash
python try_vcanvas.py
```
### Controls
- **Draw**: Move your index finger while keeping other fingers down.
- **Clear Canvas**: Make a **fist**.
- **Exit**: Press `q`.

## Example Output
The program opens a **webcam window** where users can draw on the screen in real-time with dynamic effects.

## Future Enhancements
- Add **color selection** using hand gestures.
- Support for **shape drawing** (e.g., circles, squares).
- Integration with **voice commands** for actions like clearing or saving drawings.


