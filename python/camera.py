import cv2

cap = cv2.VideoCapture(0)
faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while True:
    if cv2.waitKey(1)==ord('q'):
      break    
    ret, frame = cap.read()
    if not ret:
        print("Error: failed to capture image")
        break
      
    grayImg=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(grayImg,scaleFactor=1.1,minNeighbors=5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    if len(faces) == 0:
        cv2.putText(frame, "No Face Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    frame = cv2.resize(frame, (400, 300))
    frame = cv2.flip(frame, 1)
    
    cv2.imshow("Camera Feed", frame)
    
cap.release()
cv2.destroyAllWindows()
