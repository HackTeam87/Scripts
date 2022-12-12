# -*- coding:utf-8 -*-
from flask import Flask,request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import RPi.GPIO as GPIO
import time


import RPi.GPIO as GPIO

#Relay_Ch1 = 26
#Relay_Ch2 = 20
#Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(Relay_Ch1,GPIO.OUT)
#GPIO.setup(Relay_Ch2,GPIO.OUT)
#GPIO.setup(Relay_Ch3,GPIO.OUT)

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.route("/", methods=['GET','POST'])
@limiter.limit("1/second", override_defaults=False)
def index():
    if request.method == 'POST':
        Relay = int(request.form.get('Relay'))
        print({'type relay is ': type(Relay)})
        GPIO.setup(Relay,GPIO.OUT)

        try:
            GPIO.output(Relay,GPIO.LOW)
            time.sleep(1)
            GPIO.output(Relay,GPIO.HIGH)
            time.sleep(1)
        except:
            pass
        data = {'message': 'Done', 'code': 'SUCCESS','id': str(Relay)}
        return make_response(jsonify(data), 200)
if __name__ == "__main__":
    app.run(debug="True", host="0.0.0.0")  
  
