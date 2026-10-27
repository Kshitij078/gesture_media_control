# Gesture Media Control

Control Spotify playback using hand gestures through your webcam. This Python project uses computer vision and hand tracking to recognize gestures and perform media actions without requiring a keyboard or mouse.

## Features

- **Play/Pause:** Close your fist to toggle playback.
- **Next Track:** Raise your index finger.
- **Previous Track:** Raise your index and middle fingers.
- **Volume Up:** Raise your thumb.
- **Volume Down:** Raise your pinky finger.
- **Real-Time Hand Tracking:** Detect and track hand landmarks using MediaPipe.
- **Gesture Cooldown:** Reduce repeated commands with a delay between actions.
- **Spotify Integration:** Control playback through the Spotify Web API.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam capture and video processing |
| MediaPipe | Hand landmark detection |
| Spotipy | Spotify Web API integration |
| python-dotenv | Load Spotify credentials from environment variables |

## Project Structure

```text
gesture-media-control/
├── gesture.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file is local and must not be committed to GitHub.

## Prerequisites

- Windows 10 or Windows 11
- Python installed
- Visual Studio Code or another Python editor
- A working webcam
- A Spotify account with access to the required playback-control features
- A Spotify Developer application

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kshitij078/gesture-media-control.git
cd gesture-media-control
```

### 2. Create a virtual environment

```powershell
python -m venv env
```

Activate it:

```powershell
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## Spotify API Configuration

### 1. Create a Spotify Developer application

Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an application.

### 2. Configure the redirect URI

Add the following redirect URI to your application's settings:

```text
http://127.0.0.1:8888/callback
```

The redirect URI must match the value used in your Python application.

### 3. Configure environment variables

Create a `.env` file in the project root:

```text
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

Replace the placeholder values with your Spotify application credentials.

Never share or commit your Client Secret.

### 4. Start Spotify

Open Spotify, sign in, and start playback on your computer. The application will request authorization when it first runs.

Spotify API playback controls require an eligible account and an active playback device. Availability can also depend on Spotify's current API access requirements.

## Run the Application

From the project directory, run:

```powershell
python gesture.py
```

Allow webcam access if prompted. Hold your hand in front of the camera and perform the supported gestures.

Press `q` to exit the application.

## How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe detects hand landmarks in each frame.
3. The application evaluates landmark positions to identify finger configurations.
4. Recognized gestures trigger the corresponding Spotify Web API operation.
5. A cooldown prevents commands from firing continuously while a gesture is held.

## Future Improvements

- Add a graphical user interface.
- Display the current track and artist.
- Add configurable gestures.
- Improve gesture recognition and reduce accidental triggers.
- Add support for additional media applications.
- Display clear feedback for Spotify authentication and playback errors.

## Troubleshooting

**Webcam not detected**

Check camera permissions and ensure another application is not using the webcam.

**MediaPipe `solutions` error**

Check the installed MediaPipe version and use a version compatible with the API used in the code.

**Spotify authentication error**

Verify the Client ID, Client Secret, and redirect URI in your `.env` file and Spotify Developer settings.

**No active device error**

Open Spotify and start playback on your computer before using the controls.

**Missing Python dependencies**

Activate your virtual environment and run:

```powershell
python -m pip install -r requirements.txt
```

## Security

- Keep `.env` out of version control.
- Never publish API secrets or authentication tokens.
- Keep virtual environments and temporary cache files out of the repository.
- Review files before committing changes.

## License

This project is available for educational and portfolio purposes. Add a license file if you intend to specify formal reuse and distribution permissions.

## Author
GitHub: Kshitij078