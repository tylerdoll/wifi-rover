import RPi.GPIO as GPIO

class Rover:
    def __init__(self, in1, in2, in3, in4, ena=None, enb=None):
        # Pins for power
        self._in1 = in1
        self._in2 = in2
        self._in3 = in3
        self._in4 = in4
        GPIO.setup(self._in1, GPIO.OUT)
        GPIO.setup(self._in2, GPIO.OUT)
        GPIO.setup(self._in3, GPIO.OUT)
        GPIO.setup(self._in4, GPIO.OUT)

        # PWM pins
        PWM_FREQ = 1000
        DEFAULT_DC = 100
        if (ena):
            GPIO.setup(ena, GPIO.OUT)
            self._pwm_a = GPIO.PWM(ena, PWM_FREQ)
            self._pwm_a.start(DEFAULT_DC)
        if (enb):
            GPIO.setup(enb, GPIO.OUT)
            self._pwm_b = GPIO.PWM(enb, PWM_FREQ)
            self._pwm_b.start(DEFAULT_DC)

    def _left_forward(self):
        GPIO.output(self._in1, GPIO.HIGH)
        GPIO.output(self._in2, GPIO.LOW)

    def _right_forward(self):
        GPIO.output(self._in3, GPIO.HIGH)
        GPIO.output(self._in4, GPIO.LOW)

    def _left_backward(self):
        GPIO.output(self._in1, GPIO.LOW)
        GPIO.output(self._in2, GPIO.HIGH)

    def _right_backward(self):
        GPIO.output(self._in3, GPIO.LOW)
        GPIO.output(self._in4, GPIO.HIGH)

    def _left_stop(self):
        GPIO.output(self._in1, GPIO.LOW)
        GPIO.output(self._in2, GPIO.LOW)

    def _right_stop(self):
        GPIO.output(self._in3, GPIO.LOW)
        GPIO.output(self._in4, GPIO.LOW)

    def drive_forward(self):
        print("driving forward")
        self._left_forward()
        self._right_forward()

    def drive_backward(self):
        print("driving backward")
        self._left_backward()
        self._right_backward()

    def turn_left(self):
        print("turning left")
        self._left_backward()
        self._right_forward()

    def turn_right(self):
        print("turning right")
        self._left_forward()
        self._right_backward()

    def stop(self):
        self._left_stop()
        self._right_stop()

    def set_speed_left(self, x):
        print("Setting left speed to " + str(x) + "%")
        if (self._pwm_a): self._pwm_a.ChangeDutyCycle(x)

    def set_speed_right(self, x):
        print("Setting right speed to " + str(x) + "%")
        if (self._pwm_b): self._pwm_b.ChangeDutyCycle(x)

    def set_pwm_freq_left(self, x):
        print("Setting left pwm freq to " + str(x) + "Hz")
        if (self._pwm_a): self._pwm_a.ChangeFrequency(x)

    def set_pwm_freq_right(self, x):
        print("Setting right pwm freq to " + str(x) + "Hz")
        if (self._pwm_b): self._pwm_b.ChangeFrequency(x)

