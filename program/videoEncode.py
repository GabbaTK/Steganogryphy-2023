import cv2
from SteganographyFinal import hideText, unhideText

def encodeVideo(videoName: str, captionsFileName: str, encodeMode: str):
    video = cv2.VideoCapture(videoName)

    frameWidth = int(video.get(3))
    frameHeight = int(video.get(4))
    size = (frameWidth, frameHeight)

    videoWriter = cv2.VideoWriter("encodedVideo.avi", cv2.VideoWriter_fourcc(*"FFV1"), video.get(cv2.CAP_PROP_FPS), size)

    writing = False
    captionLine = ""
    lineRed = False
    frameId = 0
    captionsEnd = False

    with open(captionsFileName, "r") as captionsFile:
        while True:
            success, frame = video.read()

            if not success:
                break

            if not writing:
                if not lineRed and not captionsEnd:
                    captionLine = captionsFile.readline().split("-")
                    if len(captionLine) == 3:
                        captionLine[0] = int(captionLine[0])
                        captionLine[1] = int(captionLine[1])
                        lineRed = True
                    else:
                        captionsEnd = True
                
                if frameId == captionLine[0]:
                    writing = True
                else:
                    #print(hideText(encodeMode, "TEXT", " ", "PASS", frame)[0][0])
                    #cv2.imwrite("AAA.png", hideText(encodeMode, "TEXT", " ", "PASS", frame))
                    #videoWriter.write(frame)
                    videoWriter.write(hideText(encodeMode, "TEXT", " ", "PASS", frame))

            if writing:
                #videoWriter.write(frame)
                videoWriter.write(hideText(encodeMode, "TEXT", captionLine[2], "PASS", frame))

                if frameId == captionLine[1]:
                    writing = False
                    lineRed = False

            frameId += 1
            #print(f"ENCODED FRAME ID {frameId}")

    video.release()
    videoWriter.release()

def decodeVideo(videoName: str):
    video = cv2.VideoCapture(videoName)

    frameWidth = int(video.get(3))
    frameHeight = int(video.get(4))
    size = (frameWidth, frameHeight)
    videoWriter = cv2.VideoWriter("decodedVideo.mp4", cv2.VideoWriter_fourcc(*"H264"), video.get(cv2.CAP_PROP_FPS), size)

    while True:
        success, frame = video.read()

        if not success:
            break

        #print(len(frame))

        text = unhideText("PASS", frame)
        
        frame = cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        videoWriter.write(frame)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)

    video.release()
    videoWriter.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    ed = input("Encode or decode >>>")

    if ed == "e":
        encodeVideo(input("VideoName >>>"), input("CaptionsFile >>>"), input("EncodeMode >>>"))
    elif ed == "d":
        decodeVideo(input("VideoName >>>"))
