
from ultralytics import YOLO
import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587
USERNAME = 'chlwlsgh1996@naver.com'
PASSWORD = 'jinho1996'

def calculate_distance(pos1, pos2):
    return np.sqrt(np.sum((pos1 - pos2) ** 2))

def send_email(subject, body, to):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = USERNAME
    msg['To'] = to

    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(USERNAME, PASSWORD)
    smtp_server.sendmail(USERNAME, to, msg.as_string())
    smtp_server.quit()

model = YOLO('yolov8n.pt')
results = model('tcp://127.0.0.1:8888', stream=True)

last_position = None
start_time = None
while True:
    for result in results:
        if len(result.boxes) > 0:
            image = result.orig_img
            person_indices = [i for i, (cls, conf) in enumerate(zip(result.boxes.cls, 
result.boxes.conf)) if cls == 0 and conf > 0.5]

            if len(person_indices) > 0:
                boxes = result.boxes.xyxy[person_indices].cpu().numpy()
                confidences = result.boxes.conf[person_indices].cpu().numpy()

                # Find the index of the person with the highest confidence
                max_conf_index = np.argmax(confidences)
                box = boxes[max_conf_index]
                max_conf = confidences[max_conf_index]
                x_min, y_min, x_max, y_max = map(int, box[:4])
                current_position = np.array([x_min, y_min, x_max, y_max])

                if last_position is None:
                    last_position = current_position
                elif calculate_distance(current_position, last_position) > 50:  # 
                    last_position = current_position
                    start_time = None  # Reset time tracking due to position change
                else:
                    if start_time is None:
                        start_time = time.time()  # Start tracking time
                    else:
                        elapsed_time = time.time() - start_time  # Calculate elapsed time
                        if int(elapsed_time) == 30:
                            print('30 seconds passed')
                            send_email('danger', '30 seconds passed', 'dpcks367@naver.com')
                        if int(elapsed_time) == 60:
                            print('60 seconds passed')
                            send_email('danger', '60 seconds passed', 'dpcks367@naver.com')

                label = f'Person: {max_conf:.2f}'
                color = (0, 255, 0)

                image = cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
                image = cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.imshow('YOLO Detection - BedRoom', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
