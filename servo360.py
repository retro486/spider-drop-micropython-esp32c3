from machine import Pin, PWM
from time import sleep

class Servo360():
    def __init__(self, pin):
        self.servo_pin = pin
        self.PWM_FREQ = 50
        self.STOP_US = 1500
        self.MIN_US = 1000
        self.MAX_US = 2000
  

        # Adjust if your servo's actual neutral point differs.
        # If it creeps when stopped, tune STOP_US.
        # ----------------------------------------------------

        self.servo_pwm = PWM(Pin(self.servo_pin))
        self.servo_pwm.freq(self.PWM_FREQ)


    def set_pulse_us(self, pulse_us):
        """Set the servo pulse width in microseconds."""
        pulse_us = max(self.MIN_US, min(self.MAX_US, int(pulse_us)))

        # A 50 Hz period is 20,000 microseconds.
        duty_ns = pulse_us * 1000
        self.servo_pwm.duty_ns(duty_ns)


    def stop(self):
        """Stop continuous rotation."""
        self.set_pulse_us(self.STOP_US)


    def forward(self, speed=50):
        """Rotate in one direction, from 0 to 100 percent."""
        speed = max(0, min(100, int(speed)))
        pulse = self.STOP_US + (self.MAX_US - self.STOP_US) * speed // 100
        self.set_pulse_us(pulse)


    def reverse(self, speed=50):
        """Rotate in the opposite direction, from 0 to 100 percent."""
        speed = max(0, min(100, int(speed)))
        pulse = self.STOP_US - (self.STOP_US - self.MIN_US) * speed // 100
        self.set_pulse_us(pulse)


    def cleanup(self):
        """Stop the servo and release the PWM peripheral."""
        self.stop()
        sleep(0.2)
        self.servo_pwm.deinit()