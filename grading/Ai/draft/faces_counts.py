# Import required libraries 
import cv2 
import numpy as np 
# import dlib 


# Connects to your computer's default camera 
cap = cv2.VideoCapture("http://192.168.137.43:8080") 


# # Detect the coordinates 

# detector = dlib.get_frontal_face_detector() 

# Capture frames continuously 
while cap.isOpened(): 
	# Capture frame-by-frame 
	ret, frame = cap.read() 

	frame = cv2.resize(frame,(int(frame.shape[1]/2) ,int(frame.shape[0]/2) ))
	frame = cv2.flip(frame)
				  
				  
	# Iterator to count faces 
	# i = 0
	# for face in faces: 

	# 	# Get the coordinates of faces 
	# 	x, y = face.left(), face.top() 
	# 	x1, y1 = face.right(), face.bottom() 
	# 	cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2) 

	# 	# Increment iterator for each face in faces 
	# 	i = i+1

		# Display the box and faces 
	# 	cv2.putText(frame, 'face num'+str(i), (x-10, y-10), 
	# 				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
	# 	print(face, i) 

 
	cv2.rectangle(frame, (0, 0), (50, 50), (0, 255, 0), 2)
	cv2.line(frame,(100, 100), (200, 200) , (0, 255, 0) ,2)

	# Display the resulting frame 
	cv2.imshow('frame', frame) 

	# This command let's us quit with the "q" button on a keyboard. 
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		break

# Release the capture and destroy the windows 
cap.release() 
cv2.destroyAllWindows() 