🕹️ Hand-Controlled Flappy Bird Game

This project is a modern twist on the classic Flappy Bird game, allowing players to control the bird using hand gestures instead of keyboard input. 
Built with Python, PyGame, and MediaPipe, it offers an interactive computer vision-based gameplay experience.

📌 Features
	•	✋ Hand tracking control: Control the bird’s vertical position using your hand’s Y-coordinate detected via webcam.
	•	🐤 Classic Flappy Bird gameplay logic
	•	❤️ Life system with heart icons
	•	🎮 Game menu and restart functionality
	•	📷 Real-time webcam feed processed with MediaPipe Hands

 🛠️ Technologies Used
	•	Python 3.x
	•	PyGame – for game logic and UI
	•	MediaPipe – for hand gesture recognition
	•	OpenCV – for webcam access and image processing
	•	Threading – for non-blocking hand tracking
▶️ How to Run
	1.	Install dependencies:
 pip install pygame mediapipe opencv-python

 2.	Run the game:
python main.py

 3.	Control:
	•	Move your hand up or down in front of your webcam to control the bird’s position.
	•	Press SPACE to start the game or restart after Game Over.
Start game SPACE
Restart game SPACE after Game Over
Bird control Hand gesture (Y-position)
Quit game ESC or close window

project/
│
├── main.py
├── assets/
│   ├── background.png
│   ├── ground.png
│   ├── bird_up.png
│   ├── bird_mid.png
│   ├── bird_down.png
│   ├── pipe_top.png
│   ├── pipe_bottom.png
│   ├── game_over.png
│   ├── start.png
│   └── redHeart.png

⚠️ Notes
	•	Ensure your webcam is connected and accessible.
	•	The game uses index finger tip (landmark 8) to track hand height.
	•	Runs best in a well-lit environment for accurate hand detection.

