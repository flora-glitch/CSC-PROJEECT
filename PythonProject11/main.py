import cv2

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the image (change 'your_image.jpg' to your filename)
image = cv2.imread("C:/Users/Flora Benson/CSC PROJECT project/whatsApp images 33.jpg/pic 1.jpg")

# Convert to grayscale (Haar cascades work on grayscale images)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image
cv2.imshow('Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()