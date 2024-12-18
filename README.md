# ติดตั้งครั้งแรก
sudo apt update

sudo apt upgrade -y

sudo apt install python3 python3-flask

curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok

ngrok config add-authtoken 2q6m1Gd0w8fEuibiwyToH0JEyfx_2ft99jvARhHn2u8Q2EPe1

git clone https://github.com/bossware14/app-wash.git

cd app-wash

pip install flask flask_cors selenium

python3 -m venv env

flask run --host=0.0.0.0 --port=3000


# Update และโหลดใหม่
rm -f -r app-wash

git clone https://github.com/bossware14/app-wash.git

cd app-wash

python3 app.py

# เคยลง Flask Download And install
git clone https://github.com/bossware14/app-wash.git

cd app-wash

python3 -m venv env

pip install flask flask_cors selenium

flask run --host=0.0.0.0 --port=3000

# กรณีติด Error: externally-managed-environment
sudo apt install python3-requests

sudo apt install python3-venv

python3 -m venv .venv

source .venv/bin/activate

pip install requests

.venv/bin/pip install requests

.venv/bin/python


# วิธีรัน  
flask run --host=0.0.0.0 --port=3000
 หรือ
python3 app.py

# คำสั่ง api
/run?on=17 (LED 1วิ)

/delay?id=17 (แสดงไฟ)

/close ปิด

/off ปิดไฟทั้งหมด

/on เปืดที่งหมด

# เปิดหน้า app (กรณีที่มันดับ)
/start
# ปิด app
/close

# Raspberry Pi pin number
(17)
(18)
(22)
(27)
(24)
(25)

<img src="https://miro.medium.com/v2/resize:fit:828/format:webp/0*m8yp9LASmibk4IVu.png">

<img src="https://miro.medium.com/v2/resize:fit:828/format:webp/0*j5wvpTn4VIDd5RsR.png">
