from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)

# this is like the "path" thing in Django GET is a method were using (we'll also be using POST) later
# this is basically views.py with index as a render function
@app.route("/", methods = ["GET", "POST"])
def index():
    convertedText = ""
    if request.method == "POST":
        # this ensures that if ppl just hit the convert button without uploading a file
        # the button redirects to homepage and no POST request is submitted
        if "file" not in request.files: # make sure that the file actually exists
            return redirect(request.url)

        # this ensures that the file isn't blank
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        print("FORM DATA UPLOAD SUCCESFULL")

        # this is parsing the audio file uploaded if it exists
        # goal is to create an audio file "wav" format from the uploaded audio file by "recording it" with Recognizer module
        # then apply recognization funciton on audio file
        if file:
            recognizer = sr.Recognizer() # c
            audioFile = sr.AudioFile(file) # taken uploaded file and created audio file object to read
            with audioFile as f:
                data = recognizer.record(f) # reads in audio file through recognizer object
            convertedText = recognizer.recognize_google(data, key=None) # key = None => no key for google API

    return render_template('index.html', convertedText = convertedText)

if __name__ == "__main__":
    app.run(debug=True, threaded = True)
    # debug = True => allows us to Ctrl + S and it'll refresh the webpage with updates
    # threaded = True => when dealing with files and file upload we need to have a threaded basis so comp can process multiple requests
    # this is just threads kinda like multiprocessing