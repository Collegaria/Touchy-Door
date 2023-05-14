import time
import json
import requests
from boltiot import Bolt
import math
from modules import configurator

def check_config(config_filename):
    configured = configurator.create_config(config_filename)
    if not configured:
        return "Creating Config"
    else:
        with open(config_filename, 'r') as f:
            data = json.load(f)
        device = data['API']
        if device["api_key"] == "your_api_key" or device["device_id"] == "your_device_id":
            return "Default API key and device ID detected. Please update the config.json file with your API key and device ID."
        else:
            return "Configuration file is valid."



# Define the Bolt IoT module API key and device ID
API_KEY = "your_api_key"
DEVICE_ID = "your_device_id"

# Define the ultrasonic sensor pins
trig_pin = "0"
echo_pin = "1"

# Define the buzzer
buzzer_pin = "2"

# Define the green LED pin
green_led_pin = "3"

# Define the distance threshold
distance_threshold = 30

# Define the delay time
delay_time = 2

# Define the ntfy API endpoint and token
ntfy_endpoint = "https://ntfy.sh/mytopic"
ntfy_title = "Doorbell Alert"
ntfy_priority = "normal"
ntfy_tags = "doorbell,alert"

# Define the sine wave parameters
frequency = 440  # 440 Hz is middle A
duration = 500  # 500 ms = 0.5 seconds

# Define a function to read the distance from the ultrasonic sensor
def read_distance():
    response = mybolt.analogRead(trig_pin)
    data = json.loads(response)
    distance = int(data['value'])
    return distance

# Define a function to play the doorbell sound
def play_doorbell():
    # Generate the sine wave samples
    num_samples = int(duration * 1000 / 2)  # Convert duration from ms to us and divide by 2 for positive/negative cycle
    samples = [int(127 + 127 * math.sin(2 * math.pi * frequency * i / 1000000)) for i in range(num_samples)]
    # Output the sine wave to the buzzer
    for sample in samples:
        mybolt.analogWrite(buzzer_pin, sample)
        time.sleep(1e-6)  # Wait for the next sample time

# Define a function to send an alert notification
def send_alert():
    global ntfy_priority
    global num_instances_triggered
    mybolt.digitalWrite(green_led_pin, "HIGH")
    # Increment the number of instances triggered
    num_instances_triggered += 1
    # Send a ping to ntfy with higher priority if multiple instances are triggered
    if num_instances_triggered > 1:
        ntfy_priority = "high"
    headers = {"Title": ntfy_title, "Priority": ntfy_priority, "Tags": ntfy_tags}
    payload = "Someone is at the door!"
    response = requests.post(ntfy_endpoint, headers=headers, data=payload.encode(encoding='utf-8'))

# Define the main function
def main():
    global num_instances_triggered
    num_instances_triggered = 0
    while True:
        distance = read_distance()
        if distance < distance_threshold:
            time.sleep(delay_time)
            distance = read_distance()
            if distance < distance_threshold:
                play_doorbell()
                send_alert()
        else:
            mybolt.digitalWrite(buzzer_pin, "LOW")
            mybolt.digitalWrite(green_led_pin, "LOW")
            num_instances_triggered = 0
        time.sleep(0.1)

# Create a Bolt object and start the program
mybolt = Bolt(API_KEY, DEVICE_ID)
if __name__ == '__main__':
    main()
