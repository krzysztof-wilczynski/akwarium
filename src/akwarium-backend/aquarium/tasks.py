import RPi.GPIO as GPIO
import dht11 as dht11
import board
from adafruit_seesaw.seesaw import Seesaw
import logging

from celery import shared_task

from aquarium.helpers.get_moisture_percentage import get_moisture_percentage

logger = logging.getLogger(__name__)


# Kiedy uruchamia się program, inicjalizowane są wszystkie urządzenia wykonawcze w określonym stanie
@shared_task()
def startup():
    from aquarium.models import ExecutiveDevice
    GPIO.cleanup()
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


@shared_task()
def get_measurements():
    from aquarium.models import MeasuringDevice, PointValue, Parameter
    # pobierz wartości z czujników one wire
    measuring_devices = MeasuringDevice.objects.filter(is_i2c=False)

    for device in measuring_devices:
        instance = dht11.DHT11(pin=int(device.address))

        retries = 0
        while True:
            retries += 1
            result = instance.read()
            try:
                if result.is_valid():
                    humidity_parameter = device.deviceparametermeasured_set.filter(
                        parameter__name='humidity')
                    if humidity_parameter is not None and result.humidity is not None:
                        humidity_pv = PointValue.objects.create(device=device, value=result.humidity,
                                                                parameter=Parameter.objects.get(
                                                                    processed_name="humidity"))
                        humidity_pv.save()

                    air_parameter = device.deviceparametermeasured_set.filter(
                        parameter__name='air_temperature')
                    if air_parameter is not None and result.temperature is not None:
                        temperature_pv = PointValue.objects.create(device=device, value=result.temperature,
                                                                   parameter=Parameter.objects.get(
                                                                       processed_name="air_temperature"))
                        temperature_pv.save()
                    break
                if retries >= 50:
                    break
            except RuntimeError:
                pass

    # pobierz dane z czujników i2c
    i2c_measuring_devices = MeasuringDevice.objects.filter(is_i2c=True)

    i2c_bus = board.I2C()
    for device in i2c_measuring_devices:
        ss = Seesaw(i2c_bus, addr=int(device.address, 16))
        moisture, soil_temperature = None, None
        moisture = ss.moisture_read()
        soil_temperature = ss.get_temp()

        moisture_parameter = device.deviceparametermeasured_set.filter(parameter__name='moisture')
        if moisture is not None and moisture_parameter is not None:
            moisture_pv = PointValue.objects.create(device=device, value=get_moisture_percentage(moisture), parameter=
            Parameter.objects.get(processed_name='moisture'))
            moisture_pv.save()

        soil_temperature_parameter = device.deviceparametermeasured_set.filter(parameter__name='soil_temperature')
        if soil_temperature is not None and soil_temperature_parameter is not None:
            soil_temperature_pv = PointValue.objects.create(device=device, value=round(soil_temperature, 2),
                                                            parameter=Parameter.objects.get(
                                                                processed_name='soil_temperature'))
            soil_temperature_pv.save()


@shared_task(bind=True)
def cleanup_setpoint_entries(self, hours):
    from aquarium.models import PointValue
    from datetime import datetime, timedelta

    time_threshold = datetime.now() - timedelta(hours=hours)
    old_entries = PointValue.objects.filter(timestamp__lte=time_threshold)
    old_entries.delete()
