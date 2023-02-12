# Imports
from os import system as install
from copy import deepcopy as dc

# So it can run on every system
try:
    import cv2
except:
    install("pip install opencv-python")
    import cv2

def convertMessage(message):
    binary = ""

    for letter in message:
        lNum = ord(letter)
        binary += bin(lNum).strip("0b")

    return binary

def openImage(file):
    image = cv2.imread(file)
    return image, image.shape[0], image.shape[1]

def writeImage(array):
    cv2.imwrite(f"Encoded image.png", array)

def decodeBinary(binary):
    binSplit = []

    for index in range(len(binary), 7):
        binSplit.append(binary[index : index + 7]) 

    return binSplit

def writeText(openedFile, xSize, ySize, binaryText):
    image = dc(openedFile)
    count = 0

    for y in range(ySize):
        for x in range(xSize):
            for color in range(3):
                if count == len(binaryText):
                    return image

                if image[x][y][color]%2 == 0 and list(binaryText)[count] == "1":
                    count += 1
                    continue
                else:
                    image[x][y][color] -= 1

                count += 1

    return image

def decodeImage(openedFile, xSize, ySize):
    binary = ""
    for y in range(ySize):
        for x in range(xSize):
            for color in range(3):
                if openedFile[x][y][color]%2 == 0:
                    binary += "1"
                else:
                    binary += "0"

    return binary

if __name__ == "__main__":
    #message = input("Enter secret text >>>")
    #message = convertMessage(message)
    #file = input("Enter file name, including path >>>")
    #image, x, y = openImage(file)
    #writeImage(image)
    #secret = writeText(image, x, y, message)
    #writeImage(secret)

    f,x,y=openImage("./Encoded image.png")
    f=decodeImage(f, x, y)
    f=decodeBinary(f)
    #print(f)