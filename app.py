from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import requests
import time
import gpiod
import subprocess
import os
import signal

# ติดตั้ง
# pip3 install flask flask_cors selenium
# วิธีรัน  python3 main.py
# เริ่มต้น 
# http://localhost:3000/start
# API 1-5 mode
# 
# ตั้งค่า port

API_PORT = 3000 #ห้ามแก้ไข
DEBUG_MODE = True  # โหมด ทดลอง  True|False



def StartServer():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:3000']) 
    return True

# ฟังชั้น การทำงาน (API)
# SET ตั้งค่าสายไฟ
# https://youtu.be/W_kdEPdpt8Q
def SETLED(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1) #เปิด
  time.sleep(1)
  led_line.set_value(0) #ปิด
  led_line.release()
  chip.close()
  return f"success"
 except:
  return f"error"

def LEDDELAY(number):
 try:
  LED_PIN = number#17 ขาจ่ายไฟ
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1) #เปิด
  time.sleep(1)
  led_line.set_value(0) #ปิด
  led_line.release()
  chip.close()
  return f"success"
 except:
  led_line.release()
  chip.close()
  return f"error"

def LEDSTOP(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(0) #ปิด
  chip.close()
  return f"success"
 except:
  return f"error"

def LEDSTART(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1) #ปิด
  led_line.release()
  chip.close()
  return f"success"
 except:
  led_line.release()
  chip.close()
  return f"error"


#อนุญาติ forder = html
app = Flask(__name__,template_folder="html")
CORS(app)

#ห้ามแก้ไข แจ้งเตือนข้อผิดพลาด
@app.errorhandler(500)
def page_not_s(err):
   return jsonify({"status": "error","code": "500"}),200
@app.errorhandler(404)
def page_not_found(err):
   return jsonify({"status": "error","code": "404"}),200
@app.errorhandler(400)
def page_not_found_400(err):
   return jsonify({"status": "error","code": "400"}),200

## หน้าแรก ไฟล์ index.html
@app.route('/',methods=['GET'])
def start_template():
    return render_template('index.html'),200

def ExitApp():
    os.system("fuser -k 3000/tcp")

@app.route('/close',methods=['GET'])
def KULLSS():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'CLOSE' 
    #ExitApp()
    return jsonify(msg),200

@app.route('/reload',methods=['GET'])
def RELOAD():
    os.system("pkill chromium")
    StartServer()
    msg = {}
    msg['msg'] = 'RELOAD'
    return jsonify(msg),200
#
@app.route('/start',methods=['GET'])
def RUNAPP():
    StartServer()
    msg = {}
    msg['msg'] = 'START SERVER'
    return jsonify(msg),200

@app.route('/reboot',methods=['GET'])
def REBOOT():
    os.system('reboot')
    msg = {}
    msg['msg'] = 'REBOOT'
    return jsonify(msg),200

# URL 1
@app.route('/run',methods=['GET'])
def start_run():
    url = request.args.get('on')
    if not url:
        return jsonify({"status": "error"}), 200
    msg = {}
    msg['status'] = SETLED(int(url))
    msg['msg'] = int(url)
    return jsonify(msg),200

# URL 1
@app.route('/delay',methods=['GET'])
def start_delay():
    # รับ on จาก query parameters
    url = request.args.get('id')
    # ตรวจสอบว่า on ถูกต้อง
    if not url:
        return jsonify({"status": "error"}), 200
    msg = {}
    msg['status'] = LEDSTART(int(url)) 
    msg['msg'] = int(url)
    return jsonify(msg),200 

# URL 1  
@app.route('/off',methods=['GET'])
def stop_run():
    LEDSTOP(7)
    LEDSTOP(17)
    LEDSTOP(27)
    LEDSTOP(22)
    LEDSTOP(23)
    LEDSTOP(24)
    LEDSTOP(18)
    msg = {}
    msg['status'] = "success"
    msg['msg'] = "ปิกทั้งหมด"
    return jsonify(msg),200
# URL 1
@app.route('/on',methods=['GET'])
def on_run():
    LEDSTART(7)
    LEDSTART(17)
    LEDSTART(27)
    LEDSTART(22)
    LEDSTART(23)
    LEDSTART(24)
    LEDSTART(18)
    msg = {}
    msg['status'] = "success"
    msg['msg'] = "เปิดทั้งหมด"
    return jsonify(msg),200

@app.route('/v',methods=['GET'])
def Ngo():
  os.system("ngrok http http://localhost:3000")

StartServer()
# ทำงาน
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT, debug=DEBUG_MODE)
