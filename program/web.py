# Change to search for the images and video in a different directory
SEARCH_DIRECTORY = "./"








from flask import Flask, request, send_from_directory
from SteganographyFinal import hideText, unhideText
from videoEncode import encodeVideo, decodeVideo
import os
from copy import deepcopy as dc
import threading

imgExtension = ["jpeg", "png", "bmp", "tiff", "jpg", "mp4", "avi", "mov"]
def imageFilter(extension):
    if extension in imgExtension:
        return True
    return False

def updateList(html, vid):
    homeHtml = dc(html)

    files = [f for f in os.listdir(SEARCH_DIRECTORY) if os.path.isfile(f)]
    for file in files:
        if imageFilter(file.split(".")[-1]):
            homeHtml += f'                            <option value="{file}">{file}</option>'

    homeHtmlEnd = """
                        </select>
                        <h2 class="vertical-spacer">Enter secret message to encode into file or enter the directory of the file to encode into the other file</h2>
                        <h2 class="vertical-spacer">( can only encode file into image, not video, enter DECODE to decode the message )</h2>
                        <input type="text" id="secret" name="secret" class="rounded-corners input-big-size text-align vertical-spacer input-box" autocomplete="off">
                        <br>
                        <h2 class="vertical-spacer">If decoding please enter a rough estimate of the text size, the closer the faster decoding</h2>
                        <input type="text" id="size" name="size" class="rounded-corners input-big-size text-align vertical-spacer" autocomplete="off">
                        <br>
                        <br>
                        <input type="submit" name="submit" value="Submit" class="rounded-corners input-big-size text-align">
                    </form>
"""
    if not vid:
        homeHtmlEnd += """
                    <br>
                    <button class="rounded-corners input-big-size text-align", onClick="download('img')">Download</button>
                </div>
"""
    else:
        homeHtmlEnd += """
                    <br>
                    <button class="rounded-corners input-big-size text-align", onClick="download('vid')">Download</button>
                </div>
"""

    #<button class="rounded-corners input-big-size text-align", onClick="window.location.href='mailto:'">Open mail</button>

    homeHtml = homeHtml + homeHtmlEnd

    return homeHtml

homeHtmlO = """
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="stylesheet.css">
        <title>Steganograpy</title>
        <link rel="icon" href="logo.jpg">
        <style>
            body {
            background-image: url("background.png");
            background-size: cover;
            background-repeat: no-repeat;
            }
        </style>
        <script>
function download(imgVid) {
    const link = document.createElement("a")

    if (imgVid == "img") {
        link.href = "EncodedImage.png"
        link.download = "EncodedImage.png"
    }
    if (imgVid == "vid") {
        link.href = "encodedVideo.avi"
        link.download = "encodedVideo.avi"
    }
    link.click()
}
        </script>
    </head>
    <body>
        <div class="center">
            <span class="interface-text">3NCRYPTOR WEB</span>
            <span style="margin-left: 17px" class="interface-text">INTERFACE</span>
        </div>
        <br>
        <div>
            <div class="first-third" style="margin-top: 40px">
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" class="center input-big-size text-align">
                    <br>
                    <input type="submit" value="Upload" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/refresh" method="POST">
                    <input type="submit" value="Refresh files" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/" method="post">
                    <h2 class="vertical-spacer">Plese select an encoding type</h2>
                    <select name="type" id="type" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="TEXT">Hide some text in the image</option>
                        <option value="CAPT">Add captions to a video</option>
                    </select>

                    <h2 class="vertical-spacer">Plese select an encoding mode</h2>
                    <select name="mode" id="mode" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="ATCC">All three color change</option>
                        <option value="COR">Change only red</option>
                        <option value="COG">Change only green</option>
                        <option value="COB">Change only blue</option>
                        <option value="VIS">Change a lot</option>
                        <option value="SHF">Change them the same</option>
                    </select>
                    <br>
                    <h2 class="vertical-spacer">For video encoding please create a file with the extension .capf</h2>
                    <h2 class="vertical-spacer">If there are multiple, rename the non-currect files to not end in .capf</h2>
                    <br>
                    <h2 class="vertical-spacer">Select file name to encode or decode</h2>
                    <select name="file" id="file" class="rounded-corners input-big-size text-align vertical-spacer">
"""
#<option value="FILE">Encode a file into the image</option>

homeHtml = updateList(homeHtmlO, False)

homeHtmlNonEncodedO = """
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="stylesheet.css">
        <title>Steganograpy</title>
        <link rel="icon" href="logo.jpg">
        <style>
            body {
            background-image: url("background.png");
            background-size: cover;
            background-repeat: no-repeat;
            }
        </style>
        <script>
function download(imgVid) {
    const link = document.createElement("a")

    if (imgVid == "img") {
        link.href = "EncodedImage.png"
        link.download = "EncodedImage.png"
    }
    if (imgVid == "vid") {
        link.href = "encodedVideo.avi"
        link.download = "encodedVideo.avi"
    }
    link.click()
}
        </script>
    </head>
    <body>
        <div class="center">
            <span class="interface-text">3NCRYPTOR WEB</span>
            <span style="margin-left: 17px" class="interface-text">INTERFACE</span>
        </div>
        <br>
        <div>
            <div class="center" style="margin-top: 40px">
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" class="center input-big-size text-align">
                    <br>
                    <input type="submit" value="Upload" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/refresh" method="POST">
                    <input type="submit" value="Refresh files" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/" method="post">
                    <h2 class="vertical-spacer">Plese select an encoding type</h2>
                    <select name="type" id="type" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="TEXT">Hide some text in the image</option>
                        <option value="CAPT">Add captions to a video</option>
                    </select>

                    <h2 class="vertical-spacer">Plese select an encoding mode</h2>
                    <select name="mode" id="mode" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="ATCC">All three color change</option>
                        <option value="COR">Change only red</option>
                        <option value="COG">Change only green</option>
                        <option value="COB">Change only blue</option>
                        <option value="VIS">Change a lot</option>
                        <option value="SHF">Change them the same</option>
                    </select>
                    <br>
                    <h2 class="vertical-spacer">For video encoding please create a file with the extension .capf</h2>
                    <h2 class="vertical-spacer">If there are multiple, rename the non-currect files to not end in .capf</h2>
                    <br>
                    <h2 class="vertical-spacer">Select file name to encode or decode</h2>
                    <select name="file" id="file" class="rounded-corners input-big-size text-align vertical-spacer">
"""
#<option value="FILE">Encode a file into the image</option>

homeHtmlNonEncoded = updateList(homeHtmlNonEncodedO, True) + """
        </div>
    </body>
</html>
"""

videoDecodedO = """
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="stylesheet.css">
        <title>Steganograpy</title>
        <link rel="icon" href="logo.jpg">
        <style>
            body {
            background-image: url("background.png");
            background-size: cover;
            background-repeat: no-repeat;
            }
        </style>
        <script>
function download(imgVid) {
    const link = document.createElement("a")

    if (imgVid == "img") {
        link.href = "EncodedImage.png"
        link.download = "EncodedImage.png"
    }
    if (imgVid == "vid") {
        link.href = "decodedVideo.avi"
        link.download = "decodedVideo.avi"
    }
    link.click()
}
        </script>
    </head>
    <body>
        <div class="center">
            <span class="interface-text">3NCRYPTOR WEB</span>
            <span style="margin-left: 17px" class="interface-text">INTERFACE</span>
        </div>
        <br>
        <div>
            <div class="center" style="margin-top: 40px">
                <form action="/upload" method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" class="center input-big-size text-align">
                    <br>
                    <input type="submit" value="Upload" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/refresh" method="POST">
                    <input type="submit" value="Refresh files" class="rounded-corners input-big-size text-align">
                </form>
                <br>
                <form action="/" method="post">
                    <h2 class="vertical-spacer">Plese select an encoding type</h2>
                    <select name="type" id="type" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="TEXT">Hide some text in the image</option>
                        <option value="CAPT">Add captions to a video</option>
                    </select>

                    <h2 class="vertical-spacer">Plese select an encoding mode</h2>
                    <select name="mode" id="mode" class="rounded-corners input-big-size text-align vertical-spacer">
                        <option value="ATCC">All three color change</option>
                        <option value="COR">Change only red</option>
                        <option value="COG">Change only green</option>
                        <option value="COB">Change only blue</option>
                        <option value="VIS">Change a lot</option>
                        <option value="SHF">Change them the same</option>
                    </select>
                    <br>
                    <h2 class="vertical-spacer">For video encoding please create a file with the extension .capf</h2>
                    <h2 class="vertical-spacer">If there are multiple, rename the non-currect files to not end in .capf</h2>
                    <br>
                    <h2 class="vertical-spacer">Select file name to encode or decode</h2>
                    <select name="file" id="file" class="rounded-corners input-big-size text-align vertical-spacer">
"""
#<option value="FILE">Encode a file into the image</option>

videoDecoded = updateList(videoDecodedO, True) + """
        </div>
    </body>
</html>
"""

encodingSuccess = homeHtml + """
            <br>
            <br>
            <img class="second-third image-scale" src="EncodedImage.png" alt="Encoded image" id="encodedImage">
        </div>
    </body>
</html>
"""

decodingSuccess = homeHtml + """
        <br>
        <br>
        <h2>The secret text has been decoded!</h2>
        <h2>The secret text/error is: 
"""

app = Flask("3NCRYPTOR WEB INTERFACE")

@app.route('/EncodedImage.png')
def eImage():
    return send_from_directory(".", "EncodedImage.png")

@app.route('/background.png')
def bImage():
    return send_from_directory(".", "background.png")

@app.route('/stylesheet.css')
def stylesheet():
    return send_from_directory(".", "stylesheet.css")

@app.route("/TypoGraphica.ttf")
def interfaceTextFont():
    return send_from_directory(".", "TypoGraphica.ttf")

@app.route("/logo.jpg")
def webLogo():
    return send_from_directory(".", "logo.jpg")

@app.route("/encodedVideo.avi")
def eVideo():
    return send_from_directory(".", "encodedVideo.avi")

@app.route("/decodedVideo.mp4")
def dVideo():
    return send_from_directory(".", "decodedVideo.mp4")

@app.route("/fileOutput.png")
def imgOut():
    return send_from_directory(".", "fileOutput.png")


@app.route("/refresh", methods=["POST"])
def refresh():
    homeHtmlNonEncoded = updateList(homeHtmlNonEncodedO, True) + """
        </div>
    </body>
</html>
"""

    return homeHtmlNonEncoded

@app.route("/upload", methods=["POST"])
def upload():
    if "file" in request.files:
        file = request.files["file"]

        if file.filename != "":
            file.save(file.filename)

    return refresh()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        file = request.form['file']
        secret = request.form['secret']
        mode = request.form["mode"]
        type = request.form["type"]
        expectedSize = request.form["size"]

        try:
            expectedSize = int(expectedSize)
        except:
            expectedSize = 0

        return encode(file, secret, mode, type, expectedSize)
    else:
        return refresh()

def encode(file, secret, mode, type, expectedSize):
    videoDecoded = updateList(videoDecodedO, True) + """
        </div>
    </body>
</html>
"""
    homeHtml = updateList(homeHtmlO, False)
    encodingSuccess = homeHtml + """
            <br>
            <br>
            <img class="second-third image-scale" src="EncodedImage.png" alt="Encoded image" id="encodedImage">
        </div>
    </body>
</html>
"""

    decodingSuccess = homeHtml + """
        <br>
        <br>
        <h2>The secret text has been decoded!</h2>
        <h2>The secret text/error is: 
"""

    secret = secret.replace("š", "s")
    secret = secret.replace("đ", "d")
    secret = secret.replace("č", "c")
    secret = secret.replace("ć", "c")
    secret = secret.replace("ž", "z")
    secret = secret.replace("Š", "S")
    secret = secret.replace("Đ", "D")
    secret = secret.replace("Č", "C")
    secret = secret.replace("Ć", "C")
    secret = secret.replace("Ž", "Z")
    secret = secret.replace('”', '"')
    secret = secret.replace('“', '"')
    secret = secret.replace('—', "-")

    if secret == "DECODE":
        if type != "CAPT":
            textResult = unhideText(file, expectedSize)
            
            return decodingSuccess + textResult + "</h2></body></html>"
        elif type == "CAPT":
            decodeVideo(file)
            return videoDecoded
    else:   
        if type != "CAPT":
            hideText(mode, secret, file)

            return encodingSuccess
        else:
            captionFileName = ""
            files = [f for f in os.listdir(SEARCH_DIRECTORY) if os.path.isfile(f)]
            for capFile in files:
                if capFile.split(".")[-1] == "capf":
                    captionFileName = capFile

            if captionFileName == "":
                return decodingSuccess + "!!ERROR!! Caption file .capf was not found!</h2></body></html>"
            else:
                encodeVideo(file, captionFileName, mode)

                return refresh()

app.run(port=5010)