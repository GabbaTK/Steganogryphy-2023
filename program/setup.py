from os import system as install
# Automatically install all the necesary libs

try:
    import cv2
    import flask
    import numpy as np
except:
    install("pip install opencv-python")
    install("pip install flask")
    install("pip install numpy")

    import cv2
    import flask
    import numpy as np

# Create the "template" files
#with open("EncodedImage.png", "w") as file:
#    file.write("")
#with open("encodedVideo.avi", "w") as file:
#    file.write("")
#with open("EncodedImage.png", "w") as file:
#    file.write("")
#frame = np.zeros((480, 640, 3), dtype=np.uint8)
#videoWriter = cv2.VideoWriter("encodedVideo.avi", cv2.VideoWriter_fourcc(*"FFV1"), 30, (480, 640))
#videoWriter.write(frame)
#videoWriter.release()
#videoWriter = cv2.VideoWriter("decodedVideo.mp4", cv2.VideoWriter_fourcc(*"H264"), 30, (480, 640))
#videoWriter.write(frame)
#videoWriter.release()
#cv2.imwrite("fileOutput.png", frame)

print("Succesfully installed everything!")