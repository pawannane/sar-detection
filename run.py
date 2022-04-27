import time
import numpy as np
import cv2
import torch
import torch.backends. cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression
import telepot

token = '5251165045:AAF9mxi5CVCnrF3-GRAND-5ovvzF6LtCet4'  # telegram token 11
receiver_id = 1309210660  # https://api.telegram.org/bot<TOKEN>/getUpdates


bot = telepot.Bot(token)
bot.sendMessage(receiver_id, 'Your camera is active now.')  # send a message on telegran 14

camera = 0  # webcam

path = 'D:/Sem 8/major project/krish naik/YOLOv5-Flask with alert/'

weights = f'{path}yolov5s.pt'

device = torch.device('cpu')


model = attempt_load(weights, map_location=device)  # load FP32 model
stride = int(model.stride.max())  # model stride

cudnn.benchmark = True

# Capture with opencv and detect object
cap = cv2.VideoCapture(camera)
width, height = (352, 288)  # quality 28 cap.set (4, height) # height
cap.set(3, width)  # width

while (cap.isOpened()):

    time.sleep(0.2)  # wait for 0.2 second
    ret, frame = cap.read()
    if ret == True:
        now = time.time()
        img = torch.from_numpy(frame). float().to(device).permute(2, 0, 1)
        img /= 255.0  # 0 - 255 to to 0.0 - 1.0

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.39, 0.45, classes=0, agnostic=True)  # ing, conf. 100, classes.
        print('time ->', time.time() - now)

        for det in pred:
            if len(det):
                print(det)
                time_stamp = int(time.time())
                fcm_photo = f'{path}/detected/{time_stamp}.png'
                cv2.imwrite(fcm_photo, frame)  # notification photo
                bot.sendPhoto(receiver_id, photo=open(fcm_photo, 'rb'))  # send message to telegram
                time.sleep(1)  # wait for 1 second. Only when it detects
    else:
        break

cap.release()
