#! /usr/bin/python3

# std
import os.path
from threading import Thread
from time import sleep

# 3rd party
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO

# local
from rover import Rover

GPIO.setmode(GPIO.BCM)
rover = Rover(in1=27, in2=22, in3=20, in4=16, ena=17, enb=21)

#Tornado Folder Paths
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static")
)

#Tornado server port
PORT = 8080


class WebpageHandler(tornado.web.RequestHandler):
    def get(self):
        print ("[HTTP](WebpageHandler) User Connected.")
        self.render("index.html")

    
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('[WS] Connection was opened.')
 
    def on_message(self, message):
        print ('[WS] Incoming message:')
        print(message)

        if message == 'forward':
            rover.drive_forward()
        elif message == 'backward':
            rover.drive_backward()
        elif message == 'left':
            rover.turn_left()
        elif message == 'right':
            rover.turn_right()
        elif message == 'stop':
            rover.stop()
        elif message.startswith('speed-left='):
            rover.set_speed_left(int(message.split('speed-left=')[1]))
        elif message.startswith('speed-right='):
            rover.set_speed_right(int(message.split('speed-right=')[1]))
        elif message.startswith('pwm-freq-left='):
            rover.set_pwm_freq_left(int(message.split('pwm-freq-left=')[1]))
        elif message.startswith('pwm-freq-right='):
            rover.set_pwm_freq_right(int(message.split('pwm-freq-right=')[1]))
        elif message == 'shutdown':
            os.system("sudo shutdown now")

    def on_close(self):
        print ('[WS] Connection was closed.')


if __name__ == "__main__":
    try:
        app = tornado.web.Application([
                (r'/', WebpageHandler),
                (r'/ws', WebsocketHandler),
            ], **settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(PORT)
        server_loop = tornado.ioloop.IOLoop.current()

        print ("Starting main loop...")
        server_loop.start()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

