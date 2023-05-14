import json
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

def main():
    print(check_config("config.json"))


if __name__ == "__main__":
    main()