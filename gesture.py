import os
import time
import cv2
import mediapipe as mp
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

prev_time = 0
cooldown = 1.5

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-modify-playback-state user-read-playback-state",
        open_browser=True
    )
)

def play_pause():
    playback = sp.current_playback()

    if playback and playback["is_playing"]:
        sp.pause_playback()
        print("Spotify paused")
    else:
        sp.start_playback()
        print("Spotify playing")

def next_song():
    sp.next_track()
    print("Next song")

def prev_song():
    sp.previous_track()
    print("Previous song")

def volume_up():
    playback = sp.current_playback()

    if playback and playback.get("device"):
        volume = playback["device"].get("volume_percent")

        if volume is not None:
            sp.volume(min(volume + 10, 100))
            print("Volume increased")

def volume_down():
    playback = sp.current_playback()

    if playback and playback.get("device"):
        volume = playback["device"].get("volume_percent")

        if volume is not None:
            sp.volume(max(volume - 10, 0))
            print("Volume decreased")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

try:
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    while True:
        ret, img = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_index, hand_landmarks in enumerate(result.multi_hand_landmarks):
                h, w, _ = img.shape

                lm_list = [
                    (int(lm.x * w), int(lm.y * h))
                    for lm in hand_landmarks.landmark
                ]

                fingers = []

                hand_label = result.multi_handedness[hand_index].classification[0].label

                thumb_tip = lm_list[4][0]
                thumb_joint = lm_list[3][0]

                if hand_label == "Right":
                    fingers.append(int(thumb_tip > thumb_joint))
                else:
                    fingers.append(int(thumb_tip < thumb_joint))

                for tip_id in [8, 12, 16, 20]:
                    fingers.append(
                        int(lm_list[tip_id][1] < lm_list[tip_id - 2][1])
                    )

                current_time = time.time()

                if current_time - prev_time > cooldown:
                    gesture = tuple(fingers)

                    try:
                        if gesture == (0, 0, 0, 0, 0):
                            play_pause()
                            prev_time = current_time

                        elif gesture == (0, 1, 0, 0, 0):
                            next_song()
                            prev_time = current_time

                        elif gesture == (0, 1, 1, 0, 0):
                            prev_song()
                            prev_time = current_time

                        elif gesture == (1, 0, 0, 0, 0):
                            volume_up()
                            prev_time = current_time

                        elif gesture == (0, 0, 0, 0, 1):
                            volume_down()
                            prev_time = current_time

                    except Exception as e:
                        print(f"Spotify error: {e}")
                        prev_time = current_time

                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                cv2.putText(
                    img,
                    f"Fingers: {fingers}",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow("Windows Hand Gesture Controller", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()