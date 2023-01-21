import RPi.GPIO as GPIO
import dht11 as dht11
import logging

from celery import shared_task

logger = logging.getLogger(__name__)


# Kiedy uruchamia się program, inicjalizowane są wszystkie urządzenia wykonawcze w określonym stanie
@shared_task()
def startup():
    from aquarium.models import ExecutiveDevice
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


@shared_task()
def get_measurements():
    from aquarium.models import MeasuringDevice, PointValue, Parameter
    measuring_devices = MeasuringDevice.objects.filter(is_i2c=False)

    for device in measuring_devices:
        instance = dht11.DHT11(pin=int(device.address))

        while True:
            result = instance.read()
            if result.is_valid():
                humidity_parameter = device.deviceparametermeasured_set.filter(
                    parameter__name='humidity')
                if humidity_parameter is not None and result.humidity is not None:
                    humidity_pv = PointValue.objects.create(device=device, value=result.humidity,
                                                            parameter=Parameter.objects.get(processed_name="humidity"))
                    humidity_pv.save()

                air_parameter = device.deviceparametermeasured_set.filter(
                    parameter__name='air_temperature')
                if air_parameter is not None and result.temperature is not None:
                    temperature_pv = PointValue.objects.create(device=device, value=result.temperature,
                                                               parameter=Parameter.objects.get(
                                                                   processed_name="air_temperature"))
                    temperature_pv.save()
                break
    # pass
