from re import DEBUG, sub
from unicodedata import name
from flask import Flask, Response, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import telepot

token = '5251165045:AAF9mxi5CVCnrF3-GRAND-5ovvzF6LtCet4'  # telegram token 11
receiver_id = 1309210660  # https://api.telegram.org/bot<TOKEN>/getUpdates


bot = telepot.Bot(token)
bot.sendMessage(receiver_id, 'Your camera is active now.')  # send a message on telegran 14

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/live")
def live():
    return render_template('live.html')    


@app.route("/detect", methods=['POST'])  
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    subprocess.run("dir", shell=True)
    subprocess.run(['python', 'detect.py', '--source',
                   os.path.join(uploads_dir, secure_filename(video.filename))], shell=True)

    # return os.path.join(uploads_dir, secure_filename(video.filename))
    obj = secure_filename(video.filename)
    return obj

import base64
import random

@app.route("/telebot", methods=['POST'])
def telebotSender():
    print("Accessed /telebot")
    if not request.method == "POST":
        return
    #print(request.data)
    # #files = request.files
    # file = files.get('picture')
    # img = Image.open(request.files['file']) 
    # print(file)
    # decoded = base64.b64decode(file)
    # print(decoded)
    # #bot.sendPhoto(receiver_id, photo=open(fcm_photo, 'rb'))  # send message to telegram
    img_data = request.data
    img_data = img_data[23:]
    nameF = "imageTelegram"+ str(random.randint(1,257283))+".jpeg"
    with open(nameF,"wb") as fh:
        fh.write(base64.decodebytes(img_data))
    bot.sendPhoto(receiver_id, photo=open(nameF, 'rb'))  # send message to telegram        
    # with open("imageTelegram"+ str(random.randint(1,257283))+".txt","wb") as fh:
    #     fh.write(img_data)
    


@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
        # return send_from_directory(loc, obj)
    except Exception as e:
        return str(e)     

# @app.route('/display/<filename>')
# def display_video(filename):
# 	#print('display_video filename: ' + filename)
# 	return redirect(url_for('static/video_1.mp4', code=200))
