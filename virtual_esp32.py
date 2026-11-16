
import os
import json
import time
import ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

# AWS IoT Core Configuration
ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")
PORT = int(os.getenv("AWS_IOT_PORT", "8883"))
TOPIC = os.getenv("AWS_IOT_TOPIC", "visitor/button")
CLIENT_ID = os.getenv("AWS_IOT_CLIENT_ID", "virtual_esp32")

ROOT_CA = os.getenv("AWS_IOT_ROOT_CA", "certs/AmazonRootCA1.pem")
DEVICE_CERT = os.getenv("AWS_IOT_CERT", "certs/certificate.pem.crt")
PRIVATE_KEY = os.getenv("AWS_IOT_KEY", "certs/private.pem.key")


def validate_configuration():
    if not ENDPOINT:
        raise ValueError("AWS_IOT_ENDPOINT is missing in .env")

    for path in [ROOT_CA, DEVICE_CERT, PRIVATE_KEY]:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Certificate file not found: {path}")


def publish_visitor_event(event_number):
    payload = {
        "device_id": CLIENT_ID,
        "action": "button_press"
    }

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
        protocol=mqtt.MQTTv311
    )

    client.tls_set(
        ca_certs=ROOT_CA,
        certfile=DEVICE_CERT,
        keyfile=PRIVATE_KEY,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    try:
        print(f"\n--- [Event #{event_number}] Button Pressed! Waking up ESP32 ---")
        print(f"[ESP32] Connecting to AWS IoT Core at {ENDPOINT}:{PORT}...")

        client.connect(ENDPOINT, PORT, keepalive=60)
        client.loop_start()

        # Allow the connection to complete
        time.sleep(1)

        if not client.is_connected():
            raise ConnectionError("MQTT connection was not established.")

        print("[ESP32] Connected successfully!")
        print(f"[ESP32] Publishing to '{TOPIC}': {json.dumps(payload)}")

        info = client.publish(
            TOPIC,
            json.dumps(payload),
            qos=1
        )

        info.wait_for_publish(timeout=10)

        if not info.is_published():
            raise TimeoutError("Message publishing timed out.")

        print(f"[ESP32] Message published successfully (mid={info.mid}).")

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
        if client.is_connected():
            print("[ESP32] Disconnecting from AWS IoT Core...")
            client.disconnect()

        client.loop_stop()

    print(f"--- [Event #{event_number}] Done! ESP32 deep-sleeping until next press. ---")


def main():
    print("=" * 65)
    print("       VIRTUAL ESP32 - AWS IoT Core Button Press Simulator")
    print("=" * 65)

    try:
        validate_configuration()
    except Exception as error:
        print(f"\n[CONFIGURATION ERROR] {error}")
        return

    print(f"Endpoint:    {ENDPOINT}")
    print(f"Port:        {PORT}")
    print(f"Topic:       {TOPIC}")
    print(f"Device ID:   {CLIENT_ID}")
    print(f"Client ID:   {CLIENT_ID}")
    print(f"Root CA:     {ROOT_CA}")
    print(f"Device Cert: {DEVICE_CERT}")
    print(f"Private Key: {PRIVATE_KEY}")
    print('Payload:     {"device_id": "' + CLIENT_ID +
          '", "action": "button_press"}')

    print("=" * 65)
    print("\n[Ready] Press [ENTER] to simulate ESP32 button press.")
    print("Type 'q' or press [Ctrl+C] to quit.")

    event_number = 0

    try:
        while True:
            command = input(
                "\n[Virtual ESP32] Press [ENTER] to send button press "
                "(or 'q' to quit): "
            )

            if command.strip().lower() == "q":
                print("\n[Virtual ESP32] Shutting down...")
                break

            event_number += 1
            publish_visitor_event(event_number)

    except KeyboardInterrupt:
        print("\n[Virtual ESP32] Program interrupted. Goodbye!")


if __name__ == "__main__":
    main()
