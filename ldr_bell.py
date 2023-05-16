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
            return 2 #* Default API key and device ID detected. Please update the config.json file with your API key and device ID.
        else:
            return 1  #* Configuration file is valid.



# Define the Bolt IoT module API key and device ID
# Define the sine wave parameters
frequency = 440  # 440 Hz is middle A
duration = 500  # 500 ms = 0.5 seconds

# Define a function to read the distance from the ultrasonic sensor
def read_light_intensity(ldr_pin, mybolt):
    response = mybolt.analogReadLight(ldr_pin)
    data = json.loads(response)
    light_intensity = int(data['value'])
    return light_intensity


# Define a function to play the doorbell sound
def play_doorbell(buzzer_pin, mybolt):
    # Generate the sine wave samples
    num_samples = int(duration * 1000 / 2)  # Convert duration from ms to us and divide by 2 for positive/negative cycle
    samples = [int(127 + 127 * math.sin(2 * math.pi * frequency * i / 1000000)) for i in range(num_samples)]
    # Output the sine wave to the buzzer
    for sample in samples:
        mybolt.analogWrite(buzzer_pin, sample)
        time.sleep(1e-6)  # Wait for the next sample time

# Define a function to send an alert notification
def send_alert(ntfy_endpoint, ntfy_title, ntfy_priority, ntfy_tags, mybolt, green_led_pin):
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
    print("ntfy POST response status code:", response.status_code)
    if response.status_code == 200:
        print("Alert notification sent successfully.")
    else:
        print("Failed to send alert notification.")

# Define the main function
def main():
    global num_instances_triggered
    num_instances_triggered = 0

    config_status = check_config("config.json")
    if config_status == 2:
        print("Default API key and device ID detected. Please update the config.json file with your API key and device ID.")
    elif config_status == 1:
        with open("config.json", "r") as f:
            config_data = json.load(f)

        delay_time = config_data["delay_time"]
        hit_interval = 60 / 20  # Hit interval for 20 hits per minute
        
        
        ntfy_data = config_data["NTFY"] #!
        ntfy_title = ntfy_data["ntfy_title"]
        ntfy_tags = ntfy_data["ntfy_tags"]
        ntfy_priority = ntfy_data["ntfy_priority"]
        ntfy_endpoint = ntfy_data["ntfy_endpoint"]
        
        api_data = config_data["API"] #!
        api_key = api_data["api_key"]
        device_id = api_data["device_id"]
        mybolt = Bolt(api_key, device_id)
        
        pinout_data = config_data["PinOut"] #!
        buzzer_pin = pinout_data["buzzer_pin"]
        ldr_pin = pinout_data["trig_pin"]
        green_led_pin = pinout_data["green_led_pin"]
        
        distance_threshold = config_data["distance_threshold"] #!

        while True:
            # Check hit limit
            current_time = time.time()
            elapsed_time = current_time - last_hit_time
            if elapsed_time < hit_interval:
                time.sleep(hit_interval - elapsed_time)
                continue
            
            last_hit_time = current_time
            
            distance = read_light_intensity(ldr_pin, mybolt)
            if distance < distance_threshold:
                mybolt.digitalWrite(green_led_pin, "HIGH")
                time.sleep(delay_time)
                distance = read_light_intensity(ldr_pin, mybolt)
                if distance < distance_threshold:
                    play_doorbell(buzzer_pin, mybolt)
                    send_alert(ntfy_endpoint, ntfy_title, ntfy_priority, ntfy_tags, mybolt, green_led_pin)
            else:
                mybolt.digitalWrite(buzzer_pin, "LOW")
                mybolt.digitalWrite(green_led_pin, "LOW")
                num_instances_triggered = 0
            time.sleep(0.1)


if __name__ == '__main__':
    main()