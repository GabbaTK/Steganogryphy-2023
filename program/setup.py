from os import system as install
# Automatically install all the necesary libs
try:
    import cv2
    import flask
except:
    install("pip install opencv-python")
    install("pip install flask")

    import cv2
    import flask

print("Succesfully installed everything!")