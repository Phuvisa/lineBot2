from flask import Flask, jsonify, request
import os
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    a=os.environ['Authorization']
    return "นางสาวภูวิศา จำรูญสิน เลขที่ 21 ชั้น ม.4/6"

@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        return "OK"

@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    user = decoded['originalDetectIntentRequest']['payload']['data']['replyToken'] #user = decoded["events"][0]['replyToken]
    userText = decoded['queryResult']['intent']['displayName']                     #user = decoded["events"][0]['message']['text']
    if (userText == 'กินข้าวหรือยัง') :
        sendText(user,'กินข้าวแล้วจร้า')
    elif (userText == 'ไปเที่ยวกันไหม') :
        sendText(user,'ไปครับ')
    else :
        sendText(user,'ผมไม่เข้าใจอะครับ')

    return '',200

def sendText(user, text):
  LINE_API = 'https://api.line.me/v2/bot/message/reply'
  headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': os.environ['Authorization']    # ตั้ง Config vars ใน heroku พร้อมค่า Access token
  }
  data = json.dumps({
    "replyToken":user,
    "messages":[{"type":"text","text":text}]
  })
  r = requests.post(LINE_API, headers=headers, data=data) # ส่งข้อมูล

if __name__ == '__main__':
    app.run()
