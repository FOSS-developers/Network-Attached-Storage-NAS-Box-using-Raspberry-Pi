from flask import Flask, render_template, Response
from flask import request, redirect
from camera import VideoCamera
from flask_mail import Mail, Message

import mysql.connector as mariadb
import platform
import os
import datetime
import time

music_dir = '/root/Desktop/nikhil/static/music'
video_dir = '/root/Desktop/nikhil/static/video'
image_dir = '/root/Desktop/nikhil/static/image'



app = Flask(__name__)
mariadb_connection = mariadb.connect(user='root', password='123', database='nas')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mail@gmail.com'
app.config['MAIL_PASSWORD'] = '************'

mail = Mail(app)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   #ip= os.popen('ip addr show wlp19s0').read().split("inet ")[1].split("/")[0]   your_ip = request.remote_addr
   model=os.popen("cat /proc/cpuinfo  | grep 'model name\|Hardware\|Serial' | uniq").read()
   running_duration=os.popen("uptime -p").read()
   start_time=os.popen("uptime -s").read()
   host=os.popen("hostname").read()
   core=os.popen("nproc").read()
   serial=os.popen("dmidecode -s system-serial-number").read()
   total=os.popen("free -m -t | awk 'NR==2' | awk '{print $2'}").read()
   used=os.popen("free -m -t | awk 'NR==2' | awk '{print $3'}").read()
   free=os.popen("free -m -t | awk 'NR==2' | awk '{print $4'}").read()
   a=int(os.popen("cat /sys/class/thermal/thermal_zone0/temp").read())
   temp=a/float(1000)
   release=os.popen("cat /etc/*-release | grep PRETTY_NAME | cut -d= -f2").read()
   cpu_use=os.popen("top -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4 }'").read()
   disk=os.popen("df -h").read()
   proc_type=platform.processor()
   templateData = {
      'time': timeString,
      #'IP' : ip,
      'model' : model,
      'running_duration' : running_duration,
      'start_time' : start_time,
      'release' : release,
      'host' : host,
      'core' : core,
      'serial' : serial,
      'total' : total,
      'used' : used,
      'free' : free,
      'temp' : temp,
      'cpu_use' : cpu_use,
      'proc_type' : proc_type,
      'disk' : disk
      }
   error = None
   if request.method == 'GET':
        return render_template('index.html', **templateData)
   if request.method == 'POST':
       username=request.form['username']
       password=request.form['password']
       cursor = mariadb_connection.cursor()
       query = "SELECT * FROM `login` WHERE `username` = %s AND `password` = %s"
       cursor.execute(query, (username, password))   
       if cursor.fetchone():
                    return render_template('index.html', **templateData)
       else:
            error = "Invalid Credentials. Please try again."
   return render_template('home.html', error=error)
@app.route('/restart', methods = ['POST'])
def restart():
     os.system("init 6")
@app.route('/register')
def register():
     return render_template('register.html')

@app.route('/backup')
def backup():
     return render_template('backup.html')


@app.route('/samba')
def samba():
     return render_template('samba.html')

@app.route('/browse')
def browse():
     return render_template('browse.html')

@app.route('/help')
def help():
     return render_template('help.html')

@app.route('/control_panel')

def control():
     return render_template('control_panel.html')
@app.route('/shutdown', methods = ['POST'])
def shutdown():
     os.system("init 0")

@app.route('/video')
def index():
   error = None
   try:
    video_files = [f for f in os.listdir(video_dir) if f.endswith('mp4')]
    video_files_number = len(video_files)
    return render_template("video.html",
                        title = 'Home',
                        video_files_number = video_files_number,
                        video_files = video_files)
   except IOError:
        error = "Broken pipe."
        return render_template('home.html', error=error)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio')
def audio():
    music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_files_number = len(music_files)
    return render_template("audio.html",
                        title = 'Home',
                        music_files_number = music_files_number,
                        music_files = music_files)

@app.route('/contact', methods = ['POST'])
def contact():
    if request.method == 'POST':
            result= None
            name=request.form['name']
            email=request.form['email']
	    message=request.form['message']
            total="Name : "+name+"\nEmail : "+email+"\nMessage : "+message
	    msg = Message('Help-NAS Box using Raspberry Pi', sender = 'sender@gmail.com', recipients = ['receiver@gmail.com'])
   	    msg.body = total
  	    mail.send(msg)
            result="Response saved Successfully...Admin will contact within 24 hours."
            return render_template('help.html', result=result)
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


