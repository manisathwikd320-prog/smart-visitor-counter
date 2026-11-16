# 🚀 Smart Visitor Counter – Serverless IoT Dashboard

A cloud-based Smart Visitor Counter that simulates ESP32 button presses using Python and integrates with AWS IoT Core, AWS Lambda, Amazon DynamoDB, and Amazon S3 to process visitor events and display real-time visitor counts.

## 📌 Project Overview

The Smart Visitor Counter is an IoT-based cloud computing project designed to demonstrate how connected devices can communicate with cloud services to track visitor activity.

A Python-based Virtual ESP32 simulator generates button-press events and publishes them securely to AWS IoT Core using MQTT over TLS. AWS IoT Rules trigger an AWS Lambda function to process incoming events and update the visitor count stored in Amazon DynamoDB.

A separate Lambda function exposes the latest count through an HTTPS Function URL. An interactive web dashboard hosted on Amazon S3 retrieves the count automatically and displays the latest visitor statistics.

## ✨ Key Features

- **Virtual ESP32 Simulation:** Simulates ESP32 button presses using Python.
- **Secure MQTT Communication:** Uses mutual TLS authentication with AWS IoT Core.
- **Automated Event Processing:** AWS IoT Rules trigger Lambda functions.
- **Cloud Database:** Amazon DynamoDB stores the visitor count.
- **Serverless Architecture:** Uses AWS Lambda for event processing and count retrieval.
- **Live Dashboard:** Displays the latest visitor count through an S3-hosted website.
- **Automatic Synchronization:** Dashboard polls the API every 3 seconds without requiring a manual page refresh.

## 🏗️ System Architecture

```text
Virtual ESP32 Simulator
        |
        | MQTT over TLS (Port 8883)
        v
    AWS IoT Core
        |
        v
     IoT Rule
        |
        v
  Processor Lambda
        |
        v
  Amazon DynamoDB
        |
        v
   Getter Lambda
        |
        | HTTPS Function URL
        v
   S3 Web Dashboard
        |
        v
 Live Visitor Count
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Virtual ESP32 simulation |
| Paho MQTT | MQTT communication |
| AWS IoT Core | Secure device connectivity |
| AWS IoT Rules | Event routing |
| AWS Lambda | Serverless processing |
| Amazon DynamoDB | Visitor count storage |
| AWS Lambda Function URL | HTTPS API endpoint |
| Amazon S3 | Static website hosting |
| HTML, CSS, JavaScript | Dashboard frontend |

## 📂 Project Structure

```text
Smart-Visitor-Counter/
│
├── virtual_esp32.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── index.html
│
├── lambda/
│   ├── processor/
│   └── getter/
│
└── docs/
    ├── screenshots/
    └── project-presentation.pptx
```

*Note: The Lambda folders should contain the actual function source code if you choose to publish it.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Smart-Visitor-Counter
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AWS IoT Core

Create an IoT Thing in AWS IoT Core and generate its device certificate and private key.

Configure the IoT policy to allow the required MQTT connection and publishing permissions.

Place your certificate files locally:

```text
certs/
├── AmazonRootCA1.pem
├── certificate.pem.crt
└── private.pem.key
```

**Security:** Never upload your private key, device certificate, or `.env` file to GitHub.

### 4. Configure Environment Variables

Create a `.env` file using `.env.example` as a template.

```env
AWS_IOT_ENDPOINT=YOUR_AWS_IOT_ENDPOINT
AWS_IOT_PORT=8883

AWS_IOT_ROOT_CA=certs/AmazonRootCA1.pem
AWS_IOT_CERT=certs/certificate.pem.crt
AWS_IOT_KEY=certs/private.pem.key

AWS_IOT_TOPIC=visitor/button
AWS_IOT_CLIENT_ID=virtual_esp32
```

Replace the placeholder endpoint with your AWS IoT Core endpoint.

### 5. Run the Virtual ESP32 Simulator

```bash
python virtual_esp32.py
```

Press ENTER in the terminal to simulate a visitor event.

The simulator connects to AWS IoT Core, publishes a button-press message, and disconnects.

## 📡 MQTT Message Format

**Topic:**

```text
visitor/button
```

**QoS:** 1

**Payload:**

```json
{
  "device_id": "virtual_esp32",
  "action": "button_press"
}
```

## ☁️ AWS Services Configuration

The project uses the following AWS resources:

| AWS Service | Resource |
|---|---|
| AWS IoT Core | VirtualESP32 Thing and MQTT topic |
| AWS IoT Rules | Visitor event processing rule |
| AWS Lambda | Processor and Getter functions |
| Amazon DynamoDB | VisitorCounter table |
| Lambda Function URL | Visitor count API |
| Amazon S3 | Static dashboard hosting |

**DynamoDB Table:** `VisitorCounter`

**Partition Key:** `id` (String)

**Visitor Count Item:**

```json
{
  "id": "visitor_count",
  "count": 0
}
```

## 🖥️ Dashboard

The web dashboard displays:

- Current visitor count
- Live connection status
- Last synchronization time
- Automatic count updates every 3 seconds

The dashboard is hosted using Amazon S3 static website hosting.

## 🧪 Verification and Testing

The following scenarios are used to verify the project:

| Test Case | Expected Result |
|---|---|
| MQTT Connection | Successful connection to AWS IoT Core |
| Visitor Event | MQTT message successfully published |
| Database Update | Visitor count increases by one |
| Dashboard Update | Latest visitor count displayed |
| Automatic Refresh | Dashboard updates without manual refresh |
| API Response | Current count returned in JSON format |

## 🔐 Security Considerations

- MQTT communication uses TLS with mutual certificate authentication.
- AWS IAM roles provide service-specific permissions.
- Private keys and AWS credentials are excluded from the repository.
- Environment variables are maintained locally.
- Public dashboard API access should be limited to the read-only visitor count endpoint.

## 🚀 Future Enhancements

- Integration with a physical ESP32 device.
- Multiple visitor counters for different locations.
- Visitor analytics and historical reports.
- Dashboard charts and daily visitor statistics.
- Cloud monitoring and alert notifications.

## 👨‍💻 Project Team

**School of Computer Science & Artificial Intelligence**  
**SR University**

- U. Rishikateja
- MD. Abdul Muqeet
- D. Mani Sathwik
- V. Adil Basha

## 📄 License

This project is developed for academic and educational purposes.

---

**Smart Visitor Counter – Connecting IoT Devices with the Cloud.**
