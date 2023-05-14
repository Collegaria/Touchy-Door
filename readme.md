# Doorbell Alert System

This is a Python script that uses a Bolt IoT module and an ultrasonic sensor to detect when someone is close to the door and trigger a buzzer and green LED. The script also sends a ping to ntfy to alert the user that someone is at the door.

## Prerequisites

To use this script, you will need:

- A Bolt IoT module
- An ultrasonic sensor
- A buzzer
- A green LED
- Jumper wires to connect the components
- A ntfy API token

## Installation

1. Connect the ultrasonic sensor, buzzer, and green LED to the Bolt IoT module according to the pinout described in the code.
2. Install the Bolt IoT Python library by running pip install boltiot in the terminal.
3. Clone or download the doorbell_alert.py file to your computer.
4. Open the doorbell_alert.py file in a text editor and replace the placeholders for the Bolt IoT API key, device ID, and ntfy API token with your own values.
5. Save the doorbell_alert.py file.

## Usage

1. Open a terminal and navigate to the directory where the doorbell_alert.py file is located.
2. Run the script by typing python doorbell_alert.py in the terminal and pressing Enter.
3. The script will start running and will detect when someone is close to the door. When someone is detected, the buzzer and green LED will be triggered and a ping will be sent to ntfy to alert the user.

> To stop the script, press Ctrl+C in the terminal.

## Customization

You can customize the script by changing the following variables:

- distance_threshold: The distance in centimeters at which the ultrasonic sensor should trigger the alert.
- delay_time: The time in seconds to wait before triggering the alert to prevent false triggers.
- ntfy_title: The title of the ping sent to ntfy.
- ntfy_priority: The priority of the ping sent to ntfy. Set to "normal" by default, but can be changed to "high" if multiple instances are triggered at once.
- ntfy_tags: The tags to include in the ping sent to ntfy.

## Pinout

- Ultrasonic sensor:
  - VCC pin to 5V pin on the Bolt IoT module
  - GND pin to GND pin on the Bolt IoT module
  - Trig pin to digital pin 0 on the Bolt IoT module
  - Echo pin to digital pin 1 on the Bolt IoT module
- Buzzer:
  - Positive pin to digital pin 2 on the Bolt IoT module
  - Negative pin to GND pin on the Bolt IoT module
- Green LED:
  - Positive pin to digital pin 3 on the Bolt IoT module
  - Negative pin to GND pin on the Bolt IoT module
