# Smartwatch IoT System – Columbia University
A real-time IoT-based smartwatch system built using ESP8266, sensors, and cloud integration for remote monitoring and control. The system supports event-driven logic, SOS alerts, and remote visualization through Android and cloud services.


## Features

-  ESP8266-based smartwatch prototype
-  Sensor integration using I2C and SPI protocols
-  Real-time SOS alert system
-  Adaptive LED feedback system
-  Cloud integration using REST APIs
-  Remote monitoring and control via Android app
-  Backend data storage using AWS RDS / NoSQL
-  Event-driven embedded system logic

---

## Tech Stack

- **Microcontroller:** ESP8266
- **Programming:** Python / Embedded C (if applicable)
- **Protocols:** I2C, SPI, HTTP/REST
- **Cloud:** AWS RDS / NoSQL database
- **Mobile:** Android (for remote dashboard/control)
- **Networking:** WiFi-based IoT communication

---

## System Architecture

1. Sensors collect real-time data (health/activity/events)
2. ESP8266 processes data locally (event-driven logic)
3. Alerts (SOS / status updates) triggered via logic rules
4. Data sent to cloud via REST APIs
5. Android app fetches and visualizes data in real time


## Demo

End-to-end demonstration of the IoT smartwatch system built with ESP8266, showing real-time sensor processing, SOS alert triggering, and cloud-based remote monitoring via REST APIs:

[![Watch Demo](https://img.youtube.com/vi/dCafMljHvvY/0.jpg)](https://www.youtube.com/watch?v=dCafMljHvvY)
