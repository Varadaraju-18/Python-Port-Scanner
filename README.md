# Python Port Scanner

A multi-threaded Python Port Scanner built for cybersecurity learning and network reconnaissance.

## Features

* Multi-threaded port scanning for faster results
* Quick Scan mode (common ports)
* Standard Scan mode (1-10000 ports)
* Full Scan mode (1-65535 ports)
* Service detection
* Banner grabbing
* Colorized terminal output
* TXT report generation
* CSV report generation

## Technologies Used

* Python 3
* Socket Programming
* Threading
* Queue
* Colorama

## Installation

Clone the repository:

```bash
git clone https://github.com/Varadaraju-18/Python-Port-Scanner.git
cd Python-Port-Scanner
```

Install dependencies:

```bash
pip install colorama
```

## Usage

Run the scanner:

```bash
python advanced_scanner.py
```

Enter a target IP address or hostname when prompted.

Select a scan mode:

1. Quick Scan
2. Standard Scan
3. Full Scan

## Example

```text
Enter Target IP or Hostname: scanme.nmap.org

Select Scan Mode
1. Quick Scan
2. Standard Scan
3. Full Scan
```

## Output

The scanner displays:

* Open ports
* Service names
* Banner information (when available)

Reports are automatically saved:

```text
reports/scan_results.txt
reports/scan_results.csv
```

## Learning Objectives

This project was created to strengthen understanding of:

* TCP/IP Networking
* Port Scanning Techniques
* Socket Programming
* Multi-threading
* Service Enumeration
* Cybersecurity Fundamentals

## Disclaimer

This tool is intended for educational purposes and authorized security testing only. Do not scan systems without proper permission.

## Author

Varadaraju

Aspiring Cybersecurity Professional
