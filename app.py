from flask import Flask, render_template
from flask import request, redirect

import mysql.connector as mariadb
import platform
import os
import datetime
import time

app = Flask(__name__)
mariadb_connection = mariadb.connect(user='root', password='123', database='nas')
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/signup', methods = ['POST'])
def signup():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   ip= os.popen('ip addr show wlp19s0').read().split("inet ")[1].split("/")[0]
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
      'IP' : ip,
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
@app.route('/browse')
def browse():
     return render_template('browse.html')
@app.route('/control')
def control():
     return url_for("http://localhost/owncloud")
@app.route('/shutdown', methods = ['POST'])
def shutdown():
     os.system("init 0")
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


