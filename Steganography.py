# Imports
from os import system as install
from copy import deepcopy as dc
# Automatically install all the necesary libs
try:
    import cv2
except:
    install("pip install opencv-python")

    import cv2

# Imported as module
#def hideText(mode, file, text=""):
#    '''
#    Given the mode encode/decode, it will encode or decode the text to the given image file
#    '''
#
#    if mode == "encode":
#        saveImage(writeData(openImage(file)[0], openImage(file)[1], openImage(file)[2], encodeMessage(text)))
#    elif mode == "decode":
#        decodeImage(openImage(file)[0], openImage(file)[1], openImage(file)[2])

# Returns pixel image data for some image, including the x and y size
def openImage(file):
    image = cv2.imread(file)
    return image, image.shape[0], image.shape[1]

# Saves the array as image
def saveImage(array):
    cv2.imwrite("Encoded image.png", array)

# Convert the message (string) to binary (string)
def encodeMessage(message):
    endText = "000100000001000101001001110001000100000100000001010100001000101001011000001010100" # END TEXT, ends the reading

    binaryM = ""
    binaryT = []

    for letter in message:
        lNum = ord(letter)
        lBinary = list(bin(lNum))

        if len(lBinary) < 11:
            binaryT = ["0"] * (11 - len(lBinary))
            binaryT.extend(lBinary[2:len(lBinary)])
        else:
            binaryT = lBinary
        
        binaryM += ''.join(binaryT)

    binaryM += endText
    return binaryM

# Converts the binary (string) to a message (string)
def decodeMessage(binaryData):
    splitedData = []
    decoded = ""

    for index in range(0, len(binaryData), 9):
        splitedData.append(binaryData[index:index + 9])

    for binary in splitedData:
        num = int(binary, 2)
        letter = chr(num)

        decoded += letter

    return decoded

# Write binary data to file
def writeData(imageData, xSize, ySize, binaryData, mode):
    image = dc(imageData)
    count = 0
    dataLen = len(binaryData)

    for y in range(ySize):
        for x in range(xSize):
            if mode == "full color" or mode == "visible":
                for color in range(3):
                    if count == dataLen:
                        return image

                    if image[x][y][color]%2 == 0 and list(binaryData)[count] == "1":
                        count += 1
                        continue
                    else:
                        if mode != "visible":
                            if image[x][y][color] == 0:
                                image[x][y][color] += 1
                            else:
                                image[x][y][color] -= 1
                        else:
                            if image[x][y][color] > 100:
                                image[x][y][color] -= 101
                            else:
                                image[x][y][color] += 101

                    count += 1

            elif mode == "red only":
                if image[x][y][2]%2 == 0 and list(binaryData)[count] == "1":
                    count += 1
                    continue
                else:
                    if image[x][y][2] == 0:
                        image[x][y][2] += 1
                    else:
                        image[x][y][2] -= 1

                count += 1
            elif mode == "green only":
                if image[x][y][1]%2 == 0 and list(binaryData)[count] == "1":
                    count += 1
                    continue
                else:
                    if image[x][y][1] == 0:
                        image[x][y][1] += 1
                    else:
                        image[x][y][1] -= 1

                count += 1
            elif mode == "blue only":
                if image[x][y][0]%2 == 0 and list(binaryData)[count] == "1":
                    count += 1
                    continue
                else:
                    if image[x][y][0] == 0:
                        image[x][y][0] += 1
                    else:
                        image[x][y][0] -= 1

                count += 1

            elif mode == "shift":
                if image[x][y][0]%2 != 0 or list(binaryData)[count] != "1":
                    if image[x][y][0] == 0:
                        image[x][y][0] += 1
                    else:
                        image[x][y][0] -= 1
                if image[x][y][1]%2 != 0 or list(binaryData)[count] != "1":
                    if image[x][y][1] == 0:
                        image[x][y][1] += 1
                    else:
                        image[x][y][1] -= 1
                if image[x][y][2]%2 != 0 or list(binaryData)[count] != "1":
                    if image[x][y][2] == 0:
                        image[x][y][2] += 1
                    else:
                        image[x][y][2] -= 1

                count += 1

    return image

# Given the encoded image, this converts it back to string
def decodeImage(imageData, xSize, ySize):
    endText = "000100000001000101001001110001000100000100000001010100001000101001011000001010100" # END TEXT, ends the reading
    decodedData = ""

    for y in range(ySize):
        for x in range(xSize):
            for color in range(3):
                if endText in decodedData:
                    return decodedData

                if imageData[x][y][color]%2 == 0:
                    decodedData += "1"
                else:
                    decodedData += "0"

    return decodedData

# If run directly
if __name__ == "__main__":
    encodeDecode = input("Do you want to encode or decode >>>")

    if encodeDecode == "encode":
        message = input("Enter you message to hide >>>")
        imageName = input("Enter your image name, including path >>>")
        mode = input("Enter your encoding mode (full color/red only/green only/blue only/shift/visible/append) >>>")

        print("Encoding message...", end=" ")
        
        encoded = encodeMessage(message)

        print("DONE")
        print(f"Preview: {encoded}")
        print("Opening image...", end=" ")

        image, x, y = openImage(imageName)

        print("DONE")
        print("Writing data to image...", end=" ")

        encodedImage = writeData(image, x, y, encoded, mode)

        print("DONE")
        print("Saving image...", end=" ")

        saveImage(encodedImage)

        print("DONE")
    elif encodeDecode == "decode":
        imageName = input("Enter your image name, including path >>>")

        print("Opening image...", end=" ")

        image, x, y = openImage(imageName)

        print("DONE")
        print("Decoding image...", end=" ")

        decodedBinary = decodeImage(image, x, y)

        print("DONE")
        print(f"Binary preview: {decodedBinary}")
        print("Decoding binary...", end=" ")

        decoded = decodeMessage(decodedBinary)

        print("DONE")
        print(f"Message: {decoded}")