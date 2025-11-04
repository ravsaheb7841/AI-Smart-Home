---

### 🏠 **AI Smart Home Simulation**

An interactive Streamlit-based Smart Home Simulation that allows users to control lights, fans, doors, and other devices using both voice commands and buttons. It also tracks power consumption, displays usage charts, and stores user activity logs for analysis.

⚙️ Note: This version currently simulates smart device control and does not include real IoT hardware integration yet. Future updates will focus on connecting the system with actual IoT sensors and devices for real-time automation.

---

### ⚙️ **Features**

* 🎙️ Voice command control using `SpeechRecognition`
* 💡 Control devices (Lights, Fans, Doors) with on/off buttons
* 📊 Real-time dashboard for device status
* 🔊 Voice feedback using `pyttsx3`
* 📈 Power consumption visualization using `matplotlib`
* 🧾 Logs user activity automatically
* 👤 User authentication system

---

### 🧰 **Tech Stack**

* **Frontend:** Streamlit
* **Backend:** Python
* **Libraries:** Pandas, Matplotlib, Pyttsx3, SpeechRecognition, Streamlit-Autorefresh

---

### 🧩 **Project Structure**

```
AI-Smart-Home/
│
├── app.py                   # Main Streamlit app
├── requirements.txt         # Required dependencies
├── .gitignore               # Ignore unnecessary files
├── README.md                # Project description
├── users.csv                # User data (auto-created)
├── logs/                    # Activity logs (auto-created)
└── .streamlit/
    └── config.toml          # Streamlit theme and UI configuration
```

---

### 🚀 **Setup and Run**

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Smart-Home.git
cd AI-Smart-Home
```

#### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 3️⃣ Run the Streamlit app

```bash
streamlit run app.py
```

#### 4️⃣ Open in browser

Your app will open automatically at:
👉 [http://localhost:8501](http://localhost:8501)

---

### 🧾 **Sample Voice Commands**

* “Turn on the light”
* “Turn off the fan”
* “Open the door”
* “Close the door”

---

### 📊 **Future Enhancements**

* Add smart temperature control
* Connect with IoT devices
* Add mobile app integration

---

### 🧑‍💻 **Developer**

**Sahil Banso**
📧 Email: *[bansoderav@gmail.com]*
🌐 GitHub: [https://github.com/ravsaheb7841](https://github.com/ravsaheb7841)

---
