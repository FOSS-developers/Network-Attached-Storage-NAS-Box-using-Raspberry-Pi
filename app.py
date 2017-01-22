#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response, flash
from flask import request, redirect, session, url_for
from camera import VideoCamera
from flask_mail import Mail, Message
from werkzeug import secure_filename

import mysql.connector as mariadb
import platform
import os
import datetime
import time
import flask

music_dir = '/home/pi/Desktop/nikhil/static/music'
video_dir = '/home/pi/Desktop/nikhil/static/video'
image_dir = '/home/pi/Desktop/nikhil/static/image'
upload_dir= '/home/pi/Desktop/nikhil/Private_cloud'


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
mariadb_connection = mariadb.connect(user='root', password='root', database='nas')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'XXX@gmail.com'
app.config['MAIL_PASSWORD'] = 'XXX'
app.config['UPLOAD_FOLDER'] = '/home/pi/Desktop/nikhil/Private_cloud'
app.config['BACKUP_FOLDER'] = '/home/pi/Desktop/nikhil/Backup'


mail = Mail(app)

def get_ip():
	return request.remote_addr

@app.route('/')
def home():
   if 'username' in session:
         username = session['username']
         return redirect(url_for('signup'))
   return render_template('home.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   remote_ip=get_ip()
   error = None
   if request.method == 'GET':
        error= None
        if 'username' in session:
          username = session['username']
          return render_template('monitor.html',username=username)
          #return render_template('index.html' ,username=username , **templateData)
        error="Login first"
        return render_template('home.html',error=error)
   if request.method == 'POST':
       username=request.form['username']
       password=request.form['password']
       cursor = mariadb_connection.cursor()
       query = "SELECT * FROM `login` WHERE `username` = %s AND `password` = %s"
       cursor.execute(query, (username, password))   
       if cursor.fetchone():
                    session['username']=request.form['username']
                    cursor = mariadb_connection.cursor()
                    cursor.execute("insert into log values(%s,%s,%s)",(username,timeString,remote_ip)) 
                    mariadb_connection.commit()
                    return render_template('monitor.html',username=username)
                    #return render_template('index.html',username=username , **templateData)
       else:
            
            error = "Invalid Credentials. Please try again."
   return render_template('home.html', error=error)
@app.route('/restart', methods = ['POST'])
def restart():
  error= None
  if 'username' in session:
     username = session['username']
     os.system("init 6")
  error="Login first"
  return render_template('home.html',error=error)
@app.route('/register')
def register():
     return render_template('register.html')

@app.route('/backup')
def backup():
  error= None
  if 'username' in session:
     username = session['username']
     return render_template('backup.html',username=username)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/start_backup',methods=['POST'])
def start_backup():
  error= None
  result=None
  if 'username' in session:
     username = session['username']
     f = request.files['file']
     f.save(os.path.join(app.config['BACKUP_FOLDER'], f.filename))
     result="Folder Backup Scheduled!"
     return render_template('backup.html',username=username,result=result)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/samba')
def samba():
  error= None
  data=None
  if 'username' in session:
     username = session['username']
     cursor = mariadb_connection.cursor()
     cursor.execute("select directory,share_name from samba") 
     data = cursor.fetchall()  
     return render_template('samba.html',username=username,data=data)
  error="Login first"
  return render_template('home.html',error=error)


@app.route('/web')
def web():
  error= None
  data=None
  if 'username' in session:
     username = session['username']
     cursor = mariadb_connection.cursor()
     cursor.execute("select project_name, url , port from web") 
     data = cursor.fetchall()  
     return render_template('web.html',username=username,data=data)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/ftp')
def ftp():
  error= None
  data=None
  if 'username' in session:
     username = session['username']
     cursor = mariadb_connection.cursor()
     cursor.execute("select username,directory from ftp") 
     data = cursor.fetchall()  
     return render_template('ftp.html',username=username,data=data)
  error="Login first"
  return render_template('home.html',error=error)


@app.route('/share', methods = ['POST'])
def share():
  error= None
  result=None
  if request.method == 'POST':
   if 'username' in session:
     username = session['username']
     directory=request.form['directory']
     network=request.form['network']
     share_name=request.form['share_name']
     user=request.form['user']
     password=request.form['password']
     '''os.system("mkdir %s"%directory )
     os.system("chcon -t samba_share_t %s "%directory)
     os.system('echo [%s] >> /etc/samba/smb.conf'%share_name)
     os.system('echo comment = public >> /etc/samba/smb.conf')
     os.system('echo path = %s >> /etc/samba/smb.conf'%directory)
     os.system('echo public = yes >> /etc/samba/smb.conf')
     os.system('echo browsable = yes >> /etc/samba/smb.conf')
     os.system("echo valid users = %s >> /etc/samba/smb.conf"%user)
     os.system("echo host allow = %s >> /etc/samba/smb.conf"%network)'''
     cursor = mariadb_connection.cursor()
     cursor.execute("insert into samba(directory,share_name) values(%s,%s)",(directory,share_name)) 
     result="Folder shared Successfully!!"
     mariadb_connection.commit()
     cursor = mariadb_connection.cursor()
     cursor.execute("select directory,share_name from samba") 
     data = cursor.fetchall() 
     return render_template('samba.html',username=username,result=result,data=data)
   error="Login first"
   return render_template('home.html',error=error)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/start_web', methods = ['POST'])
def start_web():
  error= None
  result=None
  if request.method == 'POST':
   if 'username' in session:
     username = session['username']
     project_name=request.form['project_name']
     config_file=request.form['config_name']
     url=request.form['url']
     project="sudo mkdir /var/www/html/"+ project_name
     os.system(project)
     app.config['PROJECT_FOLDER'] = '/var/www/html/'+project_name
     f = request.files['file']
     f.save(os.path.join(app.config['PROJECT_FOLDER'], f.filename))
     data='<VirtualHost *:80> \nServerAdmin webmaster@localhost\nDocumentRoot "/var/www/html/'+project_name+'"\nServerName localhost\n</VirtualHost>\n<Directory /var/www/html/'+project_name+'>\nrequire all granted\n</Directory>'
     configure="/etc/apache2/sites-available/"+config_file
     file=open(configure,"w")
     file.write(data)
     file.close()
     os.system("sudo service apache2 restart ")

  
     cursor = mariadb_connection.cursor()
     cursor.execute("insert into web(project_name,url) values(%s,%s)",(project_name,url)) 
     result="Web hosted Successfully!!"
     mariadb_connection.commit()
     cursor = mariadb_connection.cursor()
     cursor.execute("select project_name,url,port from web") 
     data = cursor.fetchall() 
     return render_template('web.html',username=username,result=result,data=data)
   error="Login first"
   return render_template('home.html',error=error)
  error="Login first"
  return render_template('home.html',error=error)


@app.route('/browse', methods = ['GET','POST'])
def browse():
  error= None
  result=None
  
  if request.method == 'GET':
   if 'username' in session:
     username = session['username']
     files = [f for f in os.listdir(upload_dir) if f.endswith('')]
     files_number = len(files)
     return render_template('browse.html',username=username,files=files,files_number=files_number)
   error="Login first"
   return render_template('home.html',error=error)
  if request.method == 'POST':
   if 'username' in session:
      username = session['username']
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      result="File successfully Uploaded"
      files = [f for f in os.listdir(upload_dir) if f.endswith('')]
      files_number = len(files)
      return render_template('browse.html',username=username,result=result,files=files,files_number=files_number)

@app.route('/help')
def help():
  error= None
  if 'username' in session:
     username = session['username']
     return render_template('help.html',username=username)
  error="Login first"
  return render_template('home.html',error=error)



@app.route('/monitor')
def monitor():
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
   remote_ip=get_ip()
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
   error= None
   if 'username' in session:
     username = session['username']
     return render_template('index.html' ,username=username , **templateData)
     
   else :
    error="Login first"
    return render_template('home.html',error=error)

@app.route('/start_ftp', methods = ['POST'])
def start_ftp():
  error= None
  result=None
  if request.method == 'POST':
   if 'username' in session:
     username = session['username']
     app.config['FTP_FOLDER'] = '/home/pi/Desktop/nikhil/ftpuploads'
     f = request.files['file']
     f.save(os.path.join(app.config['FTP_FOLDER'], f.filename))
     os.system("sudo service vsftpd restart")
     cursor = mariadb_connection.cursor()
     cursor.execute("insert into ftp(username,directory) values(%s,%s)",(username,f.filename)) 
     result="FTP started Successfully!!"
     mariadb_connection.commit()
     cursor = mariadb_connection.cursor()
     cursor.execute("select username,directory from ftp") 
     data = cursor.fetchall() 
     return render_template('ftp.html',username=username,result=result,data=data)
   error="Login first"
   return render_template('home.html',error=error)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/user', methods = ['GET','POST'])
def user():
  error= None
  result=None
  if request.method == 'GET':
   if 'username' in session:
     username = session['username']
     if username=="admin" :
	return render_template('user.html',username=username)
     result="You are not authorized user!!!"
     return render_template('control_panel.html',username=username,result=result)
   error="Login first"
   return render_template('home.html',error=error)
  if request.method == 'POST': 
     if 'username' in session:  
  	username = session['username']
        if username=="admin" :
           username=request.form['username']
           password=request.form['password']
           cursor = mariadb_connection.cursor()
           cursor.execute("insert into login(username,password) values(%s,%s)",(username,password)) 
           mariadb_connection.commit()
           result="User Created Successfully!!"
           return render_template('user.html',username=username,result=result)
        result="You are not authorized user!!!"
        return render_template('control_panel.html',username=username,result=result)
     error="Login first"
     return render_template('home.html',error=error)

@app.route('/log', methods = ['GET'])
def log():
  error= None
  result=None
  if request.method == 'GET':
   if 'username' in session:
     username = session['username']
     if username=="admin" :
        cursor = mariadb_connection.cursor()
        cursor.execute("select username,intime,outtime from log") 
        data = cursor.fetchall() 
	return render_template('log.html',username=username,data=data)
     result="You are not authorized user!!!"
     return render_template('control_panel.html',username=username,result=result)
   error="Login first"
   return render_template('home.html',error=error)
  

@app.route('/logout')
def logout():
     session.pop('username', None)
     session.clear()
     return render_template('home.html')

@app.route('/control_panel')

def control():
  error= None
  if 'username' in session:
     username = session['username']
     return render_template('control_panel.html',username=username)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/shutdown', methods = ['POST'])
def shutdown():
  error= None
  if 'username' in session:
     username = session['username']
     os.system("init 0")
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/video')
def index():
  error = None
  if 'username' in session:
   username = session['username']
   try:
    video_files = [f for f in os.listdir(video_dir) if f.endswith('mp4')]
    video_files_number = len(video_files)
    return render_template("video.html",
                        title = 'Home',username=username ,
                        video_files_number = video_files_number,
                        video_files = video_files)
   except IOError:
        error = "Broken pipe."
        return render_template('home.html', error=error)
  error="Login first"
  return render_template('home.html',error=error)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
  error = None
  if 'username' in session:
   username = session['username']
   return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
  error="Login first"
  return render_template('home.html',error=error)


@app.route('/audio')
def audio():
  error= None
  if 'username' in session:
    username = session['username']
    music_files = [f for f in os.listdir(music_dir) if f.endswith('mp3')]
    music_files_number = len(music_files)
    return render_template("audio.html",
                        title = 'Home',username=username,
                        music_files_number = music_files_number,
                        music_files = music_files)
  error="Login first"
  return render_template('home.html',error=error)

@app.route('/contact', methods = ['POST'])
def contact():
  error= None
  if 'username' in session:
    username = session['username']
    if request.method == 'POST':
            result= None
            name=request.form['name']
            email=request.form['email']
	    message=request.form['message']
            total="Name : "+name+"\nEmail : "+email+"\nMessage : "+message
	    msg = Message('Help-NAS Box using Raspberry Pi', sender = 'ntkathole@gmail.com', recipients = ['nikhilkathole2683@gmail.com'])
   	    msg.body = total
  	    mail.send(msg)
            msg = Message('Admin-NAS Box using Raspberry Pi', sender = 'ntkathole@gmail.com', recipients = [email])
            total1=" Hello "+ name +","+"\n Thank you for request...We will resolve you query and will get back to you soon..."
   	    msg.body = total1
  	    mail.send(msg)
            result="Response saved Successfully...Admin will contact within 24 hours."
            return render_template('help.html', result=result,username=username)
  error="Login first"
  return render_template('home.html',error=error)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


