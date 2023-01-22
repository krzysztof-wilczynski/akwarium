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
    from aquarium.models import ExecutiveDevice, DeviceParameterMeasured, TaskSequence

    # ustaw wszystkie sekwencje zgodnie ze stanem początkowym
    sequences = TaskSequence.objects.all()
    for seq in sequences:
        seq.is_active = seq.startup_value
        seq.save()

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
    from aquarium.models import MeasuringDevice, PointValue, DeviceParameterMeasured
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
                        device_parameter = DeviceParameterMeasured.objects.get(
                            parameter__processed_name='humidity', device=device)
                        humidity_pv = PointValue.objects.create(device_parameter=device_parameter,
                                                                value=result.humidity)
                        humidity_pv.save()

                    air_parameter = device.deviceparametermeasured_set.filter(
                        parameter__name='air_temperature')
                    if air_parameter is not None and result.temperature is not None:
                        device_parameter = DeviceParameterMeasured.objects.get(
                            parameter__processed_name='air_temperature', device=device)
                        temperature_pv = PointValue.objects.create(device_parameter=device_parameter,
                                                                   value=result.temperature)
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

        moisture_parameter = device.deviceparametermeasured_set.filter(parameter__processed_name='moisture')
        if moisture is not None and moisture_parameter is not None:
            device_parameter = DeviceParameterMeasured.objects.get(device=device,
                                                                   parameter__processed_name='moisture')
            moisture_pv = PointValue.objects.create(device_parameter=device_parameter,
                                                    value=get_moisture_percentage(moisture))
            moisture_pv.save()

        soil_temperature_parameter = device.deviceparametermeasured_set.filter(
            parameter__processed_name='soil_temperature')
        if soil_temperature is not None and soil_temperature_parameter is not None:
            device_parameter = DeviceParameterMeasured.objects.get(device=device,
                                                                   parameter__processed_name='soil_temperature')
            soil_temperature_pv = PointValue.objects.create(device_parameter=device_parameter,
                                                            value=round(soil_temperature, 2))
            soil_temperature_pv.save()

    check_setpoints.delay()


@shared_task(bind=True)
# TODO: nazwa funkcji
def cleanup_setpoint_entries(self, hours):
    from aquarium.models import PointValue
    from datetime import datetime, timedelta

    time_threshold = datetime.now() - timedelta(hours=hours)
    old_entries = PointValue.objects.filter(timestamp__lte=time_threshold)
    old_entries.delete()


@shared_task()
def check_setpoints():
    from aquarium.models import Setpoint, PointValue, TaskSequence, TaskPrecedingSequence
    from aquarium.helpers.comparators import compare

    sequences = TaskSequence.objects.all()

    for sequence in sequences:
        try:
            last_value = PointValue.objects.filter(
                device_parameter__parameter__processed_name=sequence.setpoint.parameter.processed_name).last()

            if compare(sequence.setpoint.value + sequence.hysteresis, sequence.comparator,
                       last_value.value) and sequence.is_active is False:

                # nie próbuj wyłączać grzania/chłodzenia, jeśli to nie jest aktywne
                # lub żadne inne powiązane sekwencje nie są aktywne

                if all([x.sequence_to_check.is_active for x in
                        TaskPrecedingSequence.objects.filter(executed_sequence=sequence)]):
                    sequence.is_active = True
                    try:
                        checked_sequence = sequence.task_sequence_executed.get().sequence_to_check
                        checked_sequence.is_active = False
                        checked_sequence.save()
                    except TaskPrecedingSequence.DoesNotExist:
                        logger.info("Brak powiązanej wstecznie sekwencji.")

                    sequence.save()
                    run_sequence.delay(sequence.id)

        except AttributeError or PointValue.DoesNotExist:
            logger.info("Brak danych historycznych do porównania dla uruchomienia sekwencji.")


@shared_task(bind=True)
def run_sequence(self, setpoint_id):
    import time
    from aquarium.models import TaskSequence

    sequence = TaskSequence.objects.get(id=setpoint_id)
    tasks = sequence.tasksequencestep_set.all().order_by('order')

    for task in tasks:
        GPIO.setup(task.device.pin, GPIO.OUT)
        GPIO.output(task.device.pin, task.output_value)
        time.sleep(task.delay)


#
@shared_task(bind=True)
def switch_light(self, state):
    from aquarium.models import ExecutiveDevice

    lightbulbs = ExecutiveDevice.objects.filter(cron=True)
    for device in lightbulbs:
        GPIO.setup(device.pin, GPIO.OUT)
        GPIO.output(device.pin, state)
