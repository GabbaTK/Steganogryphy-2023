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
#         MUSC - no
#         CAPT
#
#
# Encode mode: PIXEL ONE: {encode mode}-(in all three color change) {encoded type}-(in all three color change) {refrence value}-(for the configuration)
#                                |                                          |                                         
#                 ATCC    (0)   - All three color change                (0)  - FILE                                
#                 COR     (1)   - Change only red                       (1)  - TEXT                               
#                 COG     (2)   - Change only green                     (2)  - MUSIC
#                 COB     (3)   - Change only blue                      (3)  - CAPTIONS
#                 VIS     (4)   - Change a lot to make it visible
#                 SHF     (5)   - Change all the values the same
#               X ASCI    (6)   - Each value is a letter (ASCII)
#               X APND    (7)   - Add the text/file at the end 
#                                 of the image data
#
#              PIXEL TWO: {extension letter one}-(in all three color change) {extension letter two}-(in all three color change) {extension letter three}-(in all three color change)
#                                       |                                                  |                                                  |
#                         Value is the ASCII representative                  Value is the ASCII representative                  Value is the ASCII representative
#
# Encryption: To come
# Write to top or left - NO
# Add custom encode mode - ?
# GUI with flask - DONE
# Text image generator - lib
# Custom image generator - lib

# Imports
from copy import deepcopy as dc
import cv2

# Main function
def hideText(encodeMode: str, encodedType: str, message: str, imageName: str, passedFrame = []):
    fileExtension = []

    if __encodeTypeToNumber__(encodedType) == "ERR":
        print("""
UNKNOWN TYPE!

Please select:

TEXT - Text
FILE - File
CAPT - Video Captions
        """)
        return False
    
    if __encodeModeToNumber__(encodeMode) == "ERR":
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
        """)
        return False

    if imageName == "PASS":
        imageData = passedFrame
        y = passedFrame.shape[0]
        x = passedFrame.shape[1]
    else:
        imageData, y, x = openImage(imageName)

    if encodedType == "TEXT":
        # Encode data
        encodedMessage = messageToBinary(message)

    elif encodedType == "FILE":
        with open(message, "rb") as fileToEncode:
            fileToEncodeContents = fileToEncode.read()
            encodedMessage = "".join(format(byte, "08b") for byte in fileToEncodeContents)
            encodedMessage += "000100000001000101001001110001000100000100000001010100001000101001011000001010100"

        fileExtension = message.split(".")[-1]

    # Write data to image
    encodedImage = writeBinaryToImage(imageData, x, y, encodedMessage, __encodeModeToNumber__(encodeMode), __encodeTypeToNumber__(encodedType), fileExtension)
    
    if imageName == "PASS":
        return encodedImage
    else:
        saveImage(encodedImage)

def unhideText(imageName: str, passedFrame = []):
    if imageName == "PASS":
        imageData = passedFrame
        y = passedFrame.shape[0]
        x = passedFrame.shape[1]
    else:
        imageData, y, x = openImage(imageName)

    binaryData = readBinaryFromImage(imageData, x, y)
    
    if abs(int(imageData[0][0][0]) - int(imageData[0][0][1])) == 1:
        message = binaryToMessage(binaryData)

        return "".join(list(message)[0:-9])
    
    if abs(int(imageData[0][0][0]) - int(imageData[0][0][1])) == 0:
        with open(f"fileOutput.{chr(imageData[1][0][2])}{chr(imageData[1][0][1])}{chr(imageData[1][0][0])}", "wb") as outputFile:
            binaryNumber = int(binaryData, 2)
            outputFile.write(binaryNumber.to_bytes((binaryNumber.bit_length() + 7) // 8, "big"))

        return "IMAGE_DECODE_SAVE"

# Returns pixel image data for some image, including the x and y size
def openImage(file: str):
    image = cv2.imread(file, cv2.IMREAD_UNCHANGED)
    return image, image.shape[0], image.shape[1]

# Write image data to a file
def saveImage(data):
    cv2.imwrite("EncodedImage.png", data, [cv2.IMWRITE_PNG_COMPRESSION, 0])

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
    #print(f"ENCODING: {binaryData}")

    image = dc(imageData)
    count = 0
    dataLenght = len(binaryData)
    
    if image[0][0][0] > 20:
        image[0][0][2] = image[0][0][0] - encodeMode
        image[0][0][1] = image[0][0][0] - encodedType
    else:
        image[0][0][2] = image[0][0][0] + encodeMode
        image[0][0][1] = image[0][0][0] + encodedType

    if encodedType == 0:
        image[1][0][2] = ord(extension[0])
        image[1][0][1] = ord(extension[1])
        image[1][0][0] = ord(extension[2])
    
    for x in range(xSize):
        for y in range(2, ySize):
            if encodedType == 1:
                if encodeMode == 0: # All three color change
                    for color in range(3):
                        if count == dataLenght:
                            return image

                        if binaryData[count] == "1" and image[y][x][color]%2 == 0:
                            count += 1
                            continue
                        elif binaryData[count] == "0" and image[y][x][color]%2 == 1:
                            count += 1
                            continue
                        else:
                            if image[y][x][color] < 50:
                                image[y][x][color] += 1
                            else:
                                image[y][x][color] -= 1

                            count += 1
                elif encodeMode == 1: # Change only red
                    if count == dataLenght:
                        return image

                    # CV2 uses BGR colors, so red is actually last
                    if binaryData[count] == "1" and image[y][x][2]%2 == 0:
                        count += 1
                        continue
                    elif binaryData[count] == "0" and image[y][x][2]%2 == 1:
                        count += 1
                        continue
                    else:
                        if image[y][x][2] < 50:
                            image[y][x][2] += 1
                        else:
                            image[y][x][2] -= 1

                        count += 1
                elif encodeMode == 2: # Change only green
                    if count == dataLenght:
                        return image

                    if binaryData[count] == "1" and image[y][x][1]%2 == 0:
                        count += 1
                        continue
                    elif binaryData[count] == "0" and image[y][x][1]%2 == 1:
                        count += 1
                        continue
                    else:
                        if image[y][x][1] < 50:
                            image[y][x][1] += 1
                        else:
                            image[y][x][1] -= 1

                        count += 1
                elif encodeMode == 3: # Change only blue
                    if count == dataLenght:
                        return image

                    # CV2 uses BGR colors, so blue is actually first
                    if binaryData[count] == "1" and image[y][x][0]%2 == 0:
                        count += 1
                        continue
                    elif binaryData[count] == "0" and image[y][x][0]%2 == 1:
                        count += 1
                        continue
                    else:
                        if image[y][x][0] < 50:
                            image[y][x][0] += 1
                        else:
                            image[y][x][0] -= 1

                        count += 1
                elif encodeMode == 4: # Change a lot
                    for color in range(3):
                        if count == dataLenght:
                            return image

                        if binaryData[count] == "1" and image[y][x][color]%2 == 0:
                            count += 1
                            continue
                        elif binaryData[count] == "0" and image[y][x][color]%2 == 1:
                            count += 1
                            continue
                        else:
                            if image[y][x][color] < 50:
                                image[y][x][color] += 51
                            else:
                                image[y][x][color] -= 51

                            count += 1
                elif encodeMode == 5: # Change them the same
                    if count == dataLenght:
                        return image

                    for color in range(3):
                        if binaryData[count] == "1" and image[y][x][color]%2 == 0:
                            continue
                        elif binaryData[count] == "0" and image[y][x][color]%2 == 1:
                            continue
                        else:
                            if image[y][x][color] < 50:
                                image[y][x][color] += 1
                            else:
                                image[y][x][color] -= 1

                    count += 1
            elif encodedType == 0:
                for color in range(3):
                    if count == dataLenght:
                        return image
            
                    if binaryData[count] == "1" and image[y][x][color]%2 == 0:
                        count += 1
                        continue
                    elif binaryData[count] == "0" and image[y][x][color]%2 == 1:
                        count += 1
                        continue
                    else:
                        if image[y][x][color] < 50:
                            image[y][x][color] += 1
                        else:
                            image[y][x][color] -= 1

                        count += 1

    return image

def readBinaryFromImage(imageData: list, xSize: int, ySize: int):
    data = ""
    endText = "000100000001000101001001110001000100000100000001010100001000101001011000001010100" # END TEXT, ends the reading
    decodeMode = abs(int(imageData[0][0][0]) - int(imageData[0][0][2]))
    decodeType = abs(int(imageData[0][0][0]) - int(imageData[0][0][1]))
    
    for x in range(xSize):
        for y in range(2, ySize):
            if decodeType == 1:
                if decodeMode == 0: # All three color change
                    for color in range(3):
                        if endText in data:
                            return data
                        
                        if imageData[y][x][color]%2 == 0:
                            data += "1"
                        else:
                            data += "0"
                elif decodeMode == 1: # Change only red
                    if endText in data:
                        return data
                    
                    if imageData[y][x][2]%2 == 0:
                        data += "1"
                    else:
                        data += "0"
                elif decodeMode == 2: # Change only green
                    if endText in data:
                        return data
                    
                    if imageData[y][x][1]%2 == 0:
                        data += "1"
                    else:
                        data += "0"
                elif decodeMode == 3: # Change only blue
                    if endText in data:
                        return data
                    
                    if imageData[y][x][0]%2 == 0:
                        data += "1"
                    else:
                        data += "0"
                elif decodeMode == 4: # Change a lot
                    for color in range(3):
                        if endText in data:
                            return data
                        
                        if imageData[y][x][color]%2 == 0:
                            data += "1"
                        else:
                            data += "0"
                elif decodeMode == 5: # Change them the same
                    if endText in data:
                        return data
                    
                    if imageData[y][x][0]%2 == 0:
                        data += "1"
                    else:
                        data += "0"
            elif decodeType == 0:
                for color in range(3):
                    if endText in data:
                        return data
                    
                    if imageData[y][x][color]%2 == 0:
                        data += "1"
                    else:
                        data += "0"

    return data

def __encodeModeToNumber__(encodeMode: str):
    match encodeMode:
        case "ATCC":
            return 0
        case "COR":
            return 1
        case "COG":
            return 2
        case "COB":
            return 3
        case "VIS":
            return 4
        case "SHF":
            return 5
        case "ASCI":
            return 6
        case "APND":
            return 7

    return "ERR"

def __encodeTypeToNumber__(encodeType: str):
    match encodeType:
        case "FILE":
            return 0
        case "TEXT":
            return 1
        #case "MUSIC":
            #return 2
        case "CAPT":
            return 2
        
    return "ERR"