import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json

MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

MQTT_PUB_TOPIC = "mobile/jihyun/sensing"

client = mqtt.Client()

client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUTTON = 24

GPIO.setup(BUTTON, GPIO.IN,
pull_up_down=GPIO.PUD_DOWN)


buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

LED = 23
GPIO.setup(LED, GPIO.OUT)

TRIG = 13
ECHO = 19

print("start")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

global time_stamp



try :
    while True :

        GPIO.output(TRIG, True)
        time.sleep(1)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0 :
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1 :
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print("Distance : ", distance, "cm")
        
        
        sensing = {
            "distance(cm)": distance
            }
        
        value = json.dumps(sensing)
        client.publish(MQTT_PUB_TOPIC, value)
        
        if GPIO.input(BUTTON) == True:
            break
            
        if distance <= 10:
            p = GPIO.PWM(buzzer_pin, 100)
            p.start(100)
            p.ChangeDutyCycle(90)
            p.ChangeFrequency(261)
            if GPIO.input(BUTTON) == True:
                break
            
            while True:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(LED, GPIO.LOW)
                time.sleep(1)
                if GPIO.input(BUTTON) == True:
                    break
                     
        
except:
    print("I'm done!")

finally:
    GPIO.cleanup()
