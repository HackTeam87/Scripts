# -*- coding:utf-8 -*-
# імпортуємо необхідні бібліотеки
from flask import Flask,request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import RPi.GPIO as GPIO
import time


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

@limiter.limit("1/second", override_defaults=False)

def index():
    # Якщо метод запросу POST виконуємо код
    if request.method == 'POST':
        Relay = int(request.form.get('Relay'))
        Status = int(request.form.get('Status'))
        GPIO.setup(Relay,GPIO.OUT)
        data = {'relay_id': Relay, 'status': Status, 'message': 'Done'}
        
        # блок передумов
        try:
            if Status == 0:
                GPIO.output(Relay,GPIO.HIGH)
                time.sleep(1)
                return make_response(jsonify(data, 200))
            if Status == 1:
                GPIO.output(Relay,GPIO.LOW)
                time.sleep(1)
                return make_response(jsonify(data, 200))
        except Exception as inst:
           return make_response(jsonify(inst), 404)
           # return( type(inst), inst.args, inst)

    else:
        # в іншому випадку повертаємо повідомлення
        return make_response(jsonify("Error Not Valid Request"), 404)
if __name__ == "__main__":
    # запускаємо web сервер
    app.run(debug="True", host="0.0.0.0")

