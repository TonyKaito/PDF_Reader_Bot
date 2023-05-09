import RPi.GPIO as GPIO
import asyncio

async def bot_ready():

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(17, GPIO.OUT)
	print("Light Test")
	GPIO.output(17, GPIO.HIGH)
	await asyncio.sleep(3)
	GPIO.output(17, GPIO.LOW)
	print("Light Ready")

async def bot_called():
	
	print("LED on")
	GPIO.output(17, GPIO.HIGH)
	await asyncio.sleep(1)
	print("LED off")
	GPIO.output(17, GPIO.LOW)
	await asyncio.sleep(1)
	print("LED on")
	GPIO.output(17, GPIO.HIGH)
	await asyncio.sleep(1)
	print("LED off")
	GPIO.output(17, GPIO.LOW)
	await asyncio.sleep(1)
	print("LED on")
	GPIO.output(17, GPIO.HIGH)
	await asyncio.sleep(1)
	print("LED off")
	GPIO.output(17, GPIO.LOW)