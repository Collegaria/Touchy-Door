from boltiot import Bolt
import json
import math
import time


frequency = 440  # 440 Hz is middle A
duration = 500  # 500 ms = 0.5 seconds

hit_limit = 20  # Maximum hits per minute
hit_interval = 60 / hit_limit  # Hit interval in seconds

def play_doorbell(buzzer_pin, mybolt):
    # Generate the sine wave samples
    num_samples = int(duration * 1000 / 2)  # Convert duration from ms to us and divide by 2 for positive/negative cycle
    samples = [int(127 + 127 * math.sin(2 * math.pi * frequency * i / 1000000)) for i in range(num_samples)]
    # Output the sine wave to the buzzer
    for sample in samples:
        mybolt.analogWrite(buzzer_pin, sample)
        time.sleep(1e-6)  # Wait for the next sample time
        time.sleep(hit_interval)  # Wait for the hit interval


def main():
    #play_doorbell(0, mybolt)
    with open("config.json", "r") as f:
        config_data = json.load(f)
        api_data = config_data["API"] #!
        api_key = api_data["api_key"]
        device_id = api_data["device_id"]
        mybolt = Bolt(api_key, device_id)
        print(mybolt.isOnline())
        
        play_doorbell(0, mybolt)
        
if __name__ == "__main__":
    main()