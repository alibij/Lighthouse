# Python VPN Tester with Xray

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview
This Python project is designed to test VPN services using Xray, a powerful tool for network traffic inspection and manipulation. It provides a comprehensive framework to assess VPN performance, reliability, and security features across various protocols, including VMess, VLESS, Trojan, and Shadowsocks.

## Features
- **Protocol Support**: Test popular VPN protocols like VMess, VLESS, Trojan, and Shadowsocks.
- **Performance Metrics**: Measure key performance indicators such as latency, throughput, and connection stability under different conditions.
- **Security Evaluation**: Assess critical security aspects including DNS leakage, IP address concealment, and the strength of traffic encryption for each supported protocol.
- **Automation**: Automate tests for scalability and repeatability using customizable Python scripts.
- **Report Generation**: Generate detailed reports with comprehensive test results and recommendations for improving VPN configurations.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/VPN-Tester.git
    cd VPN-Tester
    ```

2. **Install Dependencies**:
    Ensure you have Python 3.8+ installed, then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Build the Application** (Optional):
    If you want to build a standalone executable:
    ```bash
    python -m PyInstaller --name LightHouseVPN --onefile --icon icon/vpn-01.png --windowed app2.py
    ```

## Usage

To start testing your VPN services, configure the necessary parameters in the Python scripts and execute them as needed. The scripts are designed to be flexible and customizable for various testing scenarios.

## TODO

- **Create UI For :**: 
  - Static settings
  - Select location

## Resources

- For the latest version of Xray, visit the [Xray Releases](https://github.com/XTLS/Xray-core/releases).
- For the latest version of geo files, visit the [GeoIP Releases](https://github.com/v2fly/geoip/releases).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
