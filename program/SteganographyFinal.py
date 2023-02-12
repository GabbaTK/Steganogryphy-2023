# Ideas:
#
# Mode: All three color change
#       Change only one color
#       Change by 101 to make it visible
#       Add it at the end of the image
#       Change all of the RGB value the same value
#       Each RGB value is the same as the ASCII code for the character
#       Append at the end of the file
#
# Types: Message -> Image
#        File -> Image
#        Music -> Image          - no
#        Log captions -> Video
#        Music -> Video          - no
#
# Config: FILE {EXTENSION}
#         TEXT
#         MUSC
#         CAPT
#
# Hidden mode - dont specify the encoder type
#
# Encode mode: PIXEL ONE: {encode mode}-(in all three color change) {encoded type}-(in all three color change) {hidden mode}-(in all three color change)
#                                |                                          |                                         |
#                 ATCC    (0)   - All three color change                (0)  - FILE                                (0) - Hidden mode disabled
#                 COR     (1)   - Change only red                       (1)  - TEXT                                (1) - Hidden mode enabled
#                 COG     (10)  - Change only green                     (10) - MUSIC
#                 COB     (11)  - Change only blue                      (11) - CAPTIONS
#                 VIS     (100) - Change a lot to make it visible
#                 SHF     (101) - Change all the values the same
#                 ASCI    (110) - Each value is a letter (ASCII)
#                 APND    (111) - Add the text/file at the end 
#                                 of the image data
#
#              PIXEL TWO: {extension letter one}-(in all three color change) {extension letter two}-(in all three color change) {extension letter three}-(in all three color change)
#                                       |                                                  |                                                  |
#                         Value is the ASCII representative                  Value is the ASCII representative                  Value is the ASCII representative
#
# Encryption: To come
# Write to top or left - DONE
# Add custom encode mode - ?
# GUI with flask
# Text image generator - lib
# Custom image generator - lib

# Imports
from copy import deepcopy as dc
import cv2

# Main function
def hideText(encodeMode: str, encodedType: str, message: str, imageName: str, fileExtension=None):
    if not __encodeTypeToNumber__(encodedType):
        print("""
UNKNOWN TYPE!

Please select:

TEXT - Text
FILE - File
MUSC - Python Music
CAPT - Video Captions
        """)
        return False

    if __encodeModeToNumber__(encodeMode) == "FAIL":
        print("""
UNKNOWN TYPE!

Please select:

ATCC - All three color change
COR - Change only red
COG - Change only gree
COB - Change only blue
VIS - Change a lot to make it visible
SHF - Change all the values the same
ASCI - Each value is a letter (ASCII)
APND - Add the text/file at the end of the image data
        """)
        return False

    imageData, x, y = openImage(imageName)

    # Encode data
    encodedMessage = messageToBinary(message)

    # Write data to image
    encodedImage = writeBinaryToImage(imageData, x, y, encodedMessage, __encodeModeToNumber__(encodeMode), __encodeTypeToNumber__(encodedType), fileExtension)
    
    saveImage(encodedImage)

def unhideText(imageName: str):
    imageData, x, y = openImage(imageName)

    binaryData = readBinaryFromImage(imageData, x, y)

    message = binaryToMessage(binaryData)

    return "".join(list(message)[0:-9])

# Returns pixel image data for some image, including the x and y size
def openImage(file: str):
    image = cv2.imread(file)
    return image, image.shape[0], image.shape[1]

# Write image data to a file
def saveImage(data):
    cv2.imwrite(f"EncodedImage.png", data)

def messageToBinary(message: str):
    endText = "000100000001000101001001110001000100000100000001010100001000101001011000001010100" # END TEXT, ends the reading

    binaryM = ""
    binaryT = []

    for letter in message:
        lNum = ord(letter)
        lBinary = list(bin(lNum))

        # If the binary letter is not nine digits
        if len(lBinary) < 11:
            binaryT = ["0"] * (11 - len(lBinary))
            binaryT.extend(lBinary[2:len(lBinary)])
        else:
            binaryT = lBinary
        
        binaryM += ''.join(binaryT)

    binaryM += endText
    return binaryM

def binaryToMessage(binaryData: str):
    splitedData = []
    decoded = ""

    # Split the data into groups of nine
    for index in range(0, len(binaryData), 9):
        splitedData.append(binaryData[index:index + 9])

    # Convert the groups of nine to letters
    for binary in splitedData:
        num = int(binary, 2)
        letter = chr(num)

        decoded += letter

    return decoded

def writeBinaryToImage(imageData: list, xSize: int, ySize: int, binaryData: str, encodeMode: int, encodedType: int, extension: list):
    image = dc(imageData)
    count = 0
    
    dataLenght = len(binaryData)
    
    for x in range(xSize):
        for y in range(ySize):
            if count > dataLenght:
                return image
            if __colorEnabled__(encodeMode):
                for color in range(3):
                    if count >= dataLenght:
                        return image
                    if encodeMode != 110: # Encodes in binary
                        if (image[x][y][color]%2 == 0 and binaryData[count] == "1") or (image[x][y][color]%2 != 0 and binaryData[count] == "0"):
                            count += 1
                            continue
                        else:
                            if image[x][y][color] < 1:
                                image[x][y][color] += 1
                            else:
                                image[x][y][color] -= 1

                            count += 1

    return image

def readBinaryFromImage(imageData: list, xSize: int, ySize: int):
    count = 0
    data = ""
    endText = "000100000001000101001001110001000100000100000001010100001000101001011000001010100" # END TEXT, ends the reading
    
    for x in range(xSize):
        for y in range(ySize):
            #if __colorEnabled__(encodeMode):
                for color in range(3):
                    if endText in data:
                        return data
                    else:
                    #if encodeMode != 110: # Encodes in binary
                        if imageData[x][y][color]%2 == 0:
                            data += "1"
                            count += 1
                            continue
                        else:
                            data += "0"
                            count += 1
                    
    return data

def __colorEnabled__(encodeMode: int):
    if encodeMode == 0: # All three color change
        return True

    if encodeMode == 100: # Change a lot
        return True

    if encodeMode == 110: # Each color is ASCII
        return True

    return False

def __encodeModeToNumber__(encodeMode: str):
    match encodeMode:
        case "ATCC":
            return 0
        case "COR":
            return 1
        case "COG":
            return 10
        case "COB":
            return 11
        case "VIS":
            return 100
        case "SHF":
            return 101
        case "ASCI":
            return 110
        case "APND":
            return 111

    return "FAIL"

def __encodeTypeToNumber__(encodeType: str):
    match encodeType:
        case "FILE":
            return 0
        case "TEXT":
            return 1
        case "MUSIC":
            return 10
        case "CAPTIONS":
            return 11
        
    return False