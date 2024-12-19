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



API_PORT = 3000 #ห้ามแก้ไข
DEBUG_MODE = True # โหมด ทดลอง  True|False

def StartServer():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:3000']) 
    return True

def StartApp():
    subprocess.Popen(['chromium-browser','--allow-file-access-from-files','--start-fullscreen','--kiosk', 'http://localhost:3000/server']) 
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
json_data['id'] = ID_COMPUTER
json_data['date'] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')
json_data['status'] = 'ONLINE'
json_data['msg'] = 'พร้อมใช้งาน'

#ตั้งค่า MODE นาที
jsopn_mode = {}
jsopn_mode['modewash1'] = 15
jsopn_mode['modewash2'] = 10
jsopn_mode['modewash3'] = 30
jsopn_mode['modewash4'] = 25

# ตั้งค่า MODE ราคา
jsopn_price = {}
jsopn_price['modewash1'] = 30   #ซักปกติ
jsopn_price['modewash2'] = 30   #ซักด่วน 
jsopn_price['modewash3'] = 50   #ผ้าหุ่ม
jsopn_price['modewash4'] = 40   #ถหนอม
# ความร้อน
jsopn_price['temperature1'] = 0 #ปกติ
jsopn_price['temperature2'] = 30 #น้ำอุ่น
jsopn_price['temperature3'] = 0 #น้ำเย็น

json_data['price'] = jsopn_price
json_data['mode'] = jsopn_mode

## หน้าแรก ไฟล์ index.html
@app.route('/',methods=['GET'])
def start_template():
    return render_template('index.html'),200

@app.route('/server',methods=['GET'])
def server_template():
    return render_template('server.html'),200

def ExitApp():
    os.system('python3 app.py')
    os.system('fuser -k 3000/tcp')

def ShutdownApp():
    os.system("fuser -k 3000/tcp")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


#ปิดแอป
@app.route('/close',methods=['GET'])
def KULLSS():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'CLOSE' 
    ExitApp()
    return jsonify(msg),200

@app.route('/shutdown',methods=['GET'])
def Shutdowns():
    os.system("pkill chromium")
    ShutdownApp()
    msg = {}
    msg['msg'] = 'CLOSE' 
    return jsonify(msg),200


@app.route('/stop',methods=['GET'])
def STOPAPP():
    os.system("pkill chromium")
    msg = {}
    msg['msg'] = 'STOP'
    return jsonify(msg),200

#เปิดหน้าใหม่
@app.route('/reload',methods=['GET'])
def RELOAD():
    os.system("pkill chromium")
    StartServer()
    msg = {}
    msg['msg'] = 'RELOAD'
    return jsonify(msg),200

#เปิดหน้าใหม่
@app.route('/start',methods=['GET'])
def START():
    os.system("pkill chromium")
    StartServer()
    msg = {}
    msg['msg'] = 'START'
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




#ห้ามแก้ไข แจ้งเตือนข้อผิดพลาด
@app.errorhandler(500)
def page_not_s(err):
   return jsonify({"status": "error","code": "500","msg":"ไม่พร้อมใช้งาน"}),200
@app.errorhandler(404)
def page_not_found(err):
   return jsonify({"status": "error","code": "404","msg":"ไม่พร้อมใช้งาน"}),200
@app.errorhandler(400)
def page_not_found_400(err):
   return jsonify({"status": "error","code": "400","msg":"ไม่พร้อมใช้งาน"}),200



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
            return jsonify({"status":"error","msg":"ไม่พร้อมใช้งาน"}), 200

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
        with open('data.json', 'w') as f:
            json.dump(json_data, f) 
        return jsonify(json_data),200
    
    if request.method == "GET" : 
        if os.path.isfile('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
            json_data['data'] = data['data']
            if json_data['data']['status'] == "START" :
                json_data['data']['time'] = datetime.now(tz=tz).strftime('%H:%M:%S')
                #data['status'] = 'ONLINE'
                t1 = json_data['data']['timeout'].split(':')
                t2 = json_data['data']['time'].split(':')
                HOUR = int(t1[0]) - int(t2[0])
                MIN = int(t1[1]) - int(t2[1])
                SEC = int(t1[2]) - int(t2[2])
                xper = HOUR-MIN-SEC
                if xper <= 0 :
                    json_data['data']['persen'] = 100
                TOSEC = 0
                if HOUR > 0:
                    TOSEC = TOSEC + int(HOUR*60)
                if MIN > 0:
                    TOSEC = TOSEC + int(MIN*60)
                if SEC >= 0:
                    TOSEC = TOSEC + int(SEC)
                else:
                    TOSEC = TOSEC + int(SEC)
                    json_data['data']['runtime'] = str(HOUR)+':'+str(MIN)+':'+str(SEC)
                    json_data['data']['runtime'] = datetime.fromtimestamp(TOSEC).strftime('%M:%S')
                if HOUR <= 0 and MIN <= 0 and SEC <= 0:
                    json_data['data']['runtime'] = "00:00:00"
                    json_data['data']['timeout'] = "00:00:00"
                    json_data['data']['msg'] = "ว่าง"
                    json_data['data']['monitor'] = "ซักผ้า"
                    json_data['data']['status'] = 1
                    json_data['data']['start'] = 0
                else:
                    json_data['data']['persen'] = 100-TOSEC*100/int(json_data['data']['sec'])
                    json_data['data']['TIMSEC'] = TOSEC
                    json_data['data']['msg'] = "กำลังทำงาน"
                    json_data['data']['monitor'] = "ซักผ้า"
                    json_data['data']['status'] = 0
                    json_data['data']['start'] = 1

                return jsonify(json_data),200
            return jsonify(json_data),200
        else :
           json_data['data'] = {
                "id": "wash",
                "msg": "พร้อม",
                "status": 1,
                "start": 0,
                "modewash": "modewash1",
                "temperature": "temperature2",
                "monitor": "....",
                "timeout": "00:00:00",
                "update": "2024-00-1800 00:00:00",
                "time": "23:59:59",
                "action": 0,
                "sec": 0,
                "runtime": "00:00:00",
                "persen": "0"
                }

    return jsonify(json_data),200
 

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
