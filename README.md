# AI Smart Home Simulation 🏠

A Streamlit-powered smart home simulation featuring voice control, device automation, and energy monitoring dashboard.

## Overview

This project simulates a modern smart home interface with:

- Voice and text-based device control
- Temperature-based automation
- Power usage monitoring
- User authentication
- Activity logging

> **Note:** This is a simulation - no actual IoT hardware integration yet.

## Features

- 🎙️ Voice commands via `SpeechRecognition`
- 💡 Interactive device controls (Lights, Fan, AC, TV)  
- 🌡️ Temperature-based automation
- 📊 Real-time power usage charts
- 🔊 Voice feedback using `pyttsx3`
- 📝 Hourly activity logging
- 🔐 User accounts system

## Tech Stack

- Frontend: Streamlit
- Backend: Python 3.8+
- Key Libraries:
  - `streamlit`
  - `pandas` 
  - `matplotlib`
  - `pyttsx3`
  - `SpeechRecognition`
  - `streamlit-autorefresh`

## Project Structure

```
smart-home/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── users.csv          # User database
├── logs/              # Activity logs
│   └── device_log_*.csv
└── .streamlit/
    └── config.toml    # Streamlit config
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-home.git
cd smart-home
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Access at http://localhost:8501

## Usage

### Voice Commands

Examples:
- "Turn on light"
- "Turn off fan" 
- "Show device status"
- "What's the temperature?"

### Text Commands

Type commands in the input box:
- "light on"
- "fan off"
- "ac on"
- "status"

## Coming Soon

- [ ] IoT device integration
- [ ] Mobile app
- [ ] Advanced automation rules
- [ ] Remote access

## Developer

Ravsaheb Bansode
- Email: bansoderav@gmail.com 
- GitHub: [@ravsaheb7841](https://github.com/ravsaheb7841)

---
