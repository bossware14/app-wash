from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import requests
import time
import gpiod
import subprocess
import os
import signal
import json
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours = 7))



# ติดตั้ง
# pip3 install flask flask_cors selenium
# วิธีรัน  python3 main.py
# เริ่มต้น 
# http://localhost:3000/start
# API 1-6 mode

# ตั้งค่า port

API_PORT = 3000 #ห้ามแก้ไข
DEBUG_MODE = True  # โหมด ทดลอง  True|False



def StartServer():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:3000']) 
    return True

# ฟังชั้น การทำงาน (API)
# SET ตั้งค่าสายไฟ
# https://youtu.be/W_kdEPdpt8Q

#เปิดและปิด 0.1 วิ
def SETLED(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1)
  time.sleep(.1)
  led_line.set_value(0)
  led_line.release()
  chip.close()
  return f"success"
 except:
  return f"error"

#เปิด-ปิด
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

#ปิด
def LEDSTOP(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(0)
  led_line.release()
  chip.close()
  return f"success"
 except:
  return f"error"

#เปิดค้าง
def LEDSTART(number):
 try:
  LED_PIN = number
  chip = gpiod.Chip('gpiochip4')
  led_line = chip.get_line(LED_PIN)
  led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
  led_line.set_value(1)
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
json_data = {}

ID_COMPUTER = subprocess.check_output('hostnamectl').decode().split()[8]
#IP_COMPUTER = requests.get('https://checkip.amazonaws.com').text.strip()

json_data['id'] = ID_COMPUTER
#json_data['ip'] = IP_COMPUTER
json_data['date'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
json_data['status'] = 'ONLINE'

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

#ปิดแอป
@app.route('/close',methods=['GET'])
def KULLSS():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'CLOSE' 
    #ExitApp()
    return jsonify(msg),200

#เปิดหน้าใหม่
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
    url = request.args.get('id')
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
    msg['msg'] = "ปิดทั้งหมด"
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


def UPDATE_API(data):
        if not data:
            return jsonify({"status": "error"}), 200
        json_data['data'] = data
        with open('data.json', 'w') as f:
          json.dump(json_data, f)
        return json_data

@app.route('/api',methods=['GET','POST'])
def WEB_API():
    if request.method == "POST" :
        data = json.loads(request.data) 
        if data['timeout'] is None:
            return jsonify({"status": "error"}), 200

        mins = int(data['timeout'])
        update = timezone(timedelta(hours = 7,minutes=int(data['timeout'])))
        json_data['data'] = data
        json_data['port'] = API_PORT
        json_data['data']['update'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
        json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
        json_data['data']['timeout'] = datetime.now(tz=update).strftime('%H:%M:%S')
        json_data['data']['action'] = int(mins)
        json_data['data']['sec'] = int(mins)*60
        json_data['data']['runtime'] = '00:00:00'
        json_data['data']['persen'] = '0' 
        #json_data['data']['status'] = 'ONLINE'
        with open('data.json', 'w') as f:
            json.dump(json_data, f) 
        return jsonify(json_data),200
    
    if request.method == "GET" :
        if os.path.isfile('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
            data['status'] = 'ONLINE'
            t1 = data['data']['timeout'].split(':')
            t2 = data['data']['time'].split(':')
            HOUR = int(t1[0]) - int(t2[0])
            MIN = int(t1[1]) - int(t2[1])
            SEC = int(t1[2]) - int(t2[2])
            xper = HOUR-MIN-SEC
            if xper <= 0 :
               data['data']['persen'] = 100
            #else:
               #data['data']['persen'] = xper*100/100*60#int(data['data']['timeout'].replace(':',''))*100/(int(data['data']['time'].replace(':',''))*60)
            TOSEC = 0;
            if HOUR > 0:
              TOSEC = TOSEC + int(HOUR*60)
            if MIN > 0:
              TOSEC = TOSEC + int(MIN*60)
            if SEC >= 0:
              TOSEC = TOSEC + int(SEC)
            else:
              TOSEC = TOSEC + int(SEC)
            data['data']['runtime'] = str(HOUR)+':'+str(MIN)+':'+str(SEC)
            data['data']['runtime'] = datetime.fromtimestamp(TOSEC).strftime('%M:%S')
            if HOUR <= 0 and MIN <= 0 and SEC <= 0:
              data['data']['runtime'] = "00:00:00"
              data['data']['timeout'] = "00:00:00"
              data['data']['msg'] = "ว่าง"
            else:
              data['data']['persen'] = 100-TOSEC*100/int(data['data']['sec'])
              data['data']['TIMSEC'] = TOSEC
              data['data']['msg'] = "กำลังทำงาน"
    
    return jsonify(data['data']),200
 

@app.route('/backend',methods=['GET','POST'])
def BACKEND_MAIN():
    if request.method == "GET" :
        if os.path.isfile('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            return jsonify(data),200

os.system("pkill chromium")
StartServer() 
# ทำงาน
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT, debug=DEBUG_MODE)
