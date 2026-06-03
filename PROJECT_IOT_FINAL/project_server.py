from flask import Flask, render_template,request, url_for, flash, redirect
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
import random
import ast
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app= Flask(__name__)
global code
# pymongo_client = MongoClient()
# db = pymongo_client["flask_db"]
global sleep
global temp_humid
global sleep_start_time
global sleep_end_time
global final_temp_humid
global measured
measured = False
temp_humid = list()
final_temp_humid = list()
sleep = list()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return(str(o))
        return(json.JSONEncoder.default(self, o))

'''
example mongodb code
# todos.insert_one({'content': content, 'degree': degree})
# all_todos = todos.find()
input_json = request.json
'''

code = random.randint(100,20000)
def generate():
    return random.randint(100,20000)

@app.route('/generate', methods=['GET'])
def generate_code(): 
    global code  
    code = generate()
    return jsonify({'result':'success'})

@app.route('/led', methods=['GET'])
def led_show(): 
    global code  
    return jsonify({'result':str(code)})

@app.route('/send', methods=['GET'])
def get_coordinate():
    global code
    args = request.args
    val = args.get("val")
    if val == str(code):
        return jsonify({'result' : True})
    else:
        return jsonify({'result' : False})
    
#temperature_humidity collection 
@app.route('/value/temphumid', methods=['GET'])
def post_temp_humid():
    global temp_humid
    args = request.args
    temp = args.get("temp")
    humid = args.get("humid")
    input_json = request.json
    # input_json["time_stamp"] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    temp_humid.append({"temperature":temp,"humid":humid})
    return jsonify({'sent' : True})


#sleep start and end
@app.route('/sleeping/sleep_start', methods=['GET'])
def sleep_start():
    global sleep_start
    global measured
    if not measured:
        measured = True
        sleep_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sleep_start = datetime.now()
    return jsonify({'sent' : True})
    
@app.route('/sleeping/sleep_end', methods=['GET'])
def sleep_end():
    global sleep_end
    global measured
    global sleep_start
    global final_temp_humid
    global temp_humid
    if measured:
        sleep_end = datetime.now()
        diff = sleep_end - sleep_start
        diff = diff.total_seconds()
        sleep.append({"sleep":diff,"time":sleep_start})
        final_temp_humid = temp_humid.copy()
        temp_humid.clear()
        
    measured = False
    return jsonify({'sent' : True})

@app.route('/')
def start():
    return render_template('base.html')
    
#sleep pressure collection 
@app.route('/value/sleep', methods=['POST'])
def post_sleep():
    # input_json["time_stamp"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    global sleep
    ob = request.json
    print(ob)
    for o in ob:
        sleep.append(o)
    return  jsonify({'sent' : True})

@app.route('/fetch/temphumid', methods=['GET'])
def get_temp_humid():
    global temp_humid
    return json.dumps(temp_humid)


@app.route('/fetch/sleep', methods=['GET'])
def get_sleep():
    global sleep
    return json.dumps(sleep)
    
@app.route('/sleep_analysis')
def sleep_analyse(): 
    global sleep
    bar_labels = [s["time"] for s in sleep]
    bar_values = [s["sleep"] for s in sleep]
    return render_template('bar_chart.html', title='Past Sleep Activity', max=24, labels=bar_labels, values=bar_values)

@app.route('/Conditions_sleep')
def humidity(): 
    global final_temp_humid
    print(final_temp_humid)
    bar_labels = [s["temperature"] for s in final_temp_humid]
    bar_values = [s["humid"] for s in final_temp_humid]
    return render_template('line.html', title='Temperature(C) / Humidity(%) for Last Sleep', max=100, labels=bar_labels, values=bar_values)

##SMTP EMAIL 
@app.route('/not_woken',methods=['GET'])
def not_woken(): 
    username = 'mkuraloviyan@gmail.com'
    password = 'n0tfWM3EQeUlxQIO'
    msg = MIMEMultipart('mixed')

    sender = 'mkuraloviyan@gmail.com'
    recipient = 'eashan15sapre@gmail.com'

    msg['Subject'] = 'Kural Hasnt woken up.'
    msg['From'] = sender
    msg['To'] = recipient

    text_message = MIMEText('Kural hasnt woken up. Its past his alarm time', 'plain')
    html_message = MIMEText('', 'html')
    msg.attach(text_message)
    msg.attach(html_message)

    mailServer = smtplib.SMTP('mail.smtp2go.com', 2525) # 8025, 587 and 25 can also be used. 
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(username, password)
    mailServer.sendmail(sender, recipient, msg.as_string())
    mailServer.close()
    return jsonify({'sent' : True})

if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0", port= 5000)
