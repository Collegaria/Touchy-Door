import json
import os

config = {
        "API": {
            "api_key": "your_api_key",
            "device_id": "your_device_id"
        },
        "PinOut": {
            "trig_pin": "0",
            "echo_pin": "1",
            "buzzer_pin": "2",
            "green_led_pin": "3"
        },
        "distance_threshold": 30,
        "delay_time": 2,
        "NTFY": {
            "ntfy_endpoint": "https://ntfy.sh/mytopic",
            "ntfy_title": "Doorbell Alert",
            "ntfy_priority": "normal",
            "ntfy_tags": "doorbell,alert"
        }
    }

def create_config(filename):
    # check if file exists
    if os.path.exists(filename):
        return True


    with open(filename, "w") as f:
        json.dump(config, f, indent=2)
        return False

def main():
    create_config()
    
if __name__ == "__main__":
    main()