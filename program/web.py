from flask import Flask, request, send_from_directory
from SteganographyFinal import hideText, unhideText
import os
from copy import deepcopy as dc

imgExtension = ["jpeg", "png", "bmp", "tiff", "jpg"]
def imageFilter(extension):
    if extension in imgExtension:
        return True
    return False

def updateList():
    homeHtml = dc(homeHtmlO)

    files = [f for f in os.listdir() if os.path.isfile(f)]
    for file in files:
        if imageFilter(file.split(".")[-1]):
            homeHtml += f'                        <option value="{file}">{file}</option>'

    homeHtmlEnd = """
                    </select>
                    <h2 class="vertical-spacer"> Enter secret message to encode into file ( enter DECODE to decode the message )</h2>
                    <input type="text" id="secret" name="secret" class="rounded-corners input-big-size text-align vertical-spacer">
                    <br>
                    <br>
                <input type="submit" name="submit" value="Submit" class="rounded-corners input-big-size text-align">
                </form>
            </div>
    """

    homeHtml = homeHtml + homeHtmlEnd

    return homeHtml

homeHtmlO = """
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
    </head>
    <body>
        <div class="center">
            <span class="interface-text">STEGANOGRAPHY WEB</span>
            <span style="margin-left: 17px" class="interface-text">INTERFACE</span>
        </div>
        <br>
        <div class="first-third" style="margin-top: 40px">
            <form action="/" method="post">
                <h2 class="vertical-spacer"> Select file name to encode or decode</h2>
                <select name="file" id="file" class="rounded-corners input-big-size text-align vertical-spacer">
"""

homeHtml = updateList()

encodingSuccess = homeHtml + """
        <br>
        <br>
        <img class="second-third" src="EncodedImage.png" alt="Encoded image">
    </body>
</html>
"""

decodingSuccess = homeHtml + """
        <br>
        <br>
        <h2>The secret text has been decoded!</h2>
        <h2>The secret text is: 
"""

app = Flask("Steganography GUI")

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

@app.route('/', methods=['GET', 'POST'])
def home():
    homeHtml = updateList()

    if request.method == "POST":
        file = request.form['file']
        secret = request.form['secret']

        if secret == "DECODE":
            return decodingSuccess + unhideText(file) + "</h2></body></html>"
        else:   
            hideText("ATCC", "TEXT", secret, file)
            return encodingSuccess
    else:
        return homeHtml + "</body></html>"

app.run(port=5010)