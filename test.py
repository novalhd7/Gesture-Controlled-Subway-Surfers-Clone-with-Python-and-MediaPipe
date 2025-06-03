import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Inisialisasi Keyboard Controller
keyboard = Controller()

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)

# Variabel untuk menyimpan posisi tangan sebelumnya
prev_x, prev_y = None, None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip gambar agar mirip dengan cermin
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Ambil posisi jari tengah (landmark 9) sebagai referensi
            x, y = int(hand_landmarks.landmark[9].x * frame.shape[1]), int(hand_landmarks.landmark[9].y * frame.shape[0])
            
            if prev_x is not None and prev_y is not None:
                dx, dy = x - prev_x, y - prev_y
                
                # Deteksi gerakan tangan
                if abs(dx) > abs(dy):  # Gerakan horizontal
                    if dx > 30:
                        print("Swipe Kanan")
                        keyboard.press(Key.right)
                        time.sleep(0.2)
                        keyboard.release(Key.right)
                    elif dx < -30:
                        print("Swipe Kiri")
                        keyboard.press(Key.left)
                        time.sleep(0.2)
                        keyboard.release(Key.left)
                else:  # Gerakan vertikal
                    if dy > 30:
                        print("Swipe Turun")
                        keyboard.press(Key.down)
                        time.sleep(0.2)
                        keyboard.release(Key.down)
                    elif dy < -30:
                        print("Swipe Atas")
                        keyboard.press(Key.up)
                        time.sleep(0.2)
                        keyboard.release(Key.up)
                    
            prev_x, prev_y = x, y
    
    cv2.imshow("Subway Surfers Gesture Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
