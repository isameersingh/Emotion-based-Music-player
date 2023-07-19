import cv2
from deepface import DeepFace
import time
import webbrowser
import pandas as pd
from db_helper import dbHelper
db=dbHelper()
try:
    # Load the pre-trained face cascade classifier
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Could not open video device")

    # Set the start time
    start_time = time.time()

    # Initialize variables to keep track of predicted emotions
    emotion_counts = {}

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Analyze the frame using DeepFace to detect emotions
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        # Draw a rectangle around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Set the font and display the dominant emotion on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,
                    result[0]['dominant_emotion'],
                    (50, 50),
                    font, 3,
                    (0, 0, 255),
                    2,
                    cv2.LINE_4)

        # Update the emotion counts
        emotion = result[0]['dominant_emotion']
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        # Display the frame in a window named "Live"
        cv2.imshow('Live', frame)

        # Check if 10 seconds have passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            break

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    # Release the webcam and close the windows
    cap.release()
    cv2.destroyAllWindows()

    # Get the most predicted emotion
    most_predicted_emotion = max(emotion_counts, key=emotion_counts.get)
    print("Most predicted emotion:", most_predicted_emotion)

    happy_gnr=('Hip Hop','EDM',"disco songs","POP")
    if most_predicted_emotion=="happy":
        emotion_dct={"Geners":"'Hip Hop','EDM','disco songs','POP'",'Mood':[most_predicted_emotion]}
        emotion_df=pd.DataFrame(emotion_dct)
    print(emotion_df)
    db.store(most_predicted_emotion)
    print("mood is stored into db")

except Exception as e:
    print('Error:', str(e))
# opening songs in webbrowser 
# lang=input("please select the language ")
# singer=input("please select your fav singer")
# webbrowser.open(f"https://www.youtube.com/results?search_query={lang}+{most_predicted_emotion}+song+{singer}")