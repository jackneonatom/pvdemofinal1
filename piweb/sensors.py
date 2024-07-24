import asyncio
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from app import store_data  # Assuming store_data is defined in app.py
import aiohttp

LED_PIN = 21  # GPIO pin where the LED is connected

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def read_battery_voltage():
    return 32

def read_battery_current():
    return 21

def read_battery_temp():
    return 30

def read_panel_voltage():
    return 4

def read_panel_current():
    return 5

def read_panel_temp():
    return 10

def read_panel_light():
    return 7

async def get_led_status():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://pv-demo.local:8000/led-status') as response:
            if response.status == 200:
                data = await response.json()
                return data.get('status', False)
            else:
                return False

async def main():
    battery_current_reading = read_battery_current()
    battery_voltage_reading = read_battery_voltage()
    battery_temp_reading = read_battery_temp()
    panel_current_reading = read_panel_current()
    panel_voltage_reading = read_panel_voltage()
    panel_temp_reading = read_panel_temp()
    panel_light_reading = read_panel_light()

    led_status = await get_led_status()
    GPIO.output(LED_PIN, GPIO.HIGH if led_status else GPIO.LOW)

    task = asyncio.create_task(store_data(battery_current_reading, battery_voltage_reading, battery_temp_reading, panel_current_reading, panel_voltage_reading, panel_temp_reading, panel_light_reading))
    print("Data stored (or task created for storing data).")

asyncio.run(main())
