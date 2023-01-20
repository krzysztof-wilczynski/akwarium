from celery import shared_task
import RPi.GPIO as GPIO

from aquarium.models import ExecutiveDevice


@shared_task
# Kiedy uruchamia się program, inicjalizowane są wszystkie urządzenia wykonawcze w określonym stanie
def startup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    executive_devices = ExecutiveDevice.objects.all()
    if executive_devices:
        for device in executive_devices:
            if device.is_out:
                GPIO.setup(device.pin, GPIO.OUT)
            else:
                GPIO.setup(device.pin, GPIO.IN)
            GPIO.output(device.pin, device.state)

    # i2c_bus = board.I2C()
    # ss = Seesaw(i2c_bus, addr=0x36)
