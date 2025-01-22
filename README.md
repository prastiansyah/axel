This script uses Selenium and undetected-chromedriver to manage Chrome browser sessions. It supports GUI, headless, and manual login modes, and loads extensions and user profiles from config.json. It is suitable for browser task automation, extension testing, and secure session management.
# Selenium Browser Automation

This Python script provides an automation tool for launching and managing Chrome browser sessions using Selenium and the `undetected_chromedriver` library. It supports multiple modes of operation: manual login, GUI mode, and headless mode.

## Features
- Load browser profiles and extensions from a configuration file.
- Supports headless and GUI browser operation.
- Tracks elapsed time during operations.
- Automatically validates extension paths and configurations.

## Requirements
- Python 3.7 or later
- Chrome browser installed
- ChromeDriver compatible with the installed Chrome version

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/prastiansyah/axel.git
   cd axel
   pip install requirements.txt
   python main.py

   ## Don't forget edit paths in config.json ##
