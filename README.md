# QueueWise — Smart Queue Management System

**Smarter queues. Better service. Less uncertainty.**

QueueWise is a web-based queue management system designed to make public-service visits more organized and transparent. It enables visitors to obtain digital tokens, track queue progress, and view estimated waiting times while staff manage service counters and visitor flow through a central dashboard.

> **Project status:** Independent prototype developed for OpenHack’26. QueueWise is inspired by public-service centres and is not affiliated with or endorsed by NADRA.

## 🚀 Live Demo

**[Open QueueWise](https://asadali345.pythonanywhere.com/)**

Explore the deployed application to see the queue management workflow in action.##
## 📸 Screenshots

### 1. Main Dashboard
<img width="950" alt="QueueWise Main Dashboard" src="https://github.com/user-attachments/assets/055b7e00-967d-43de-82c4-f023d32f0363" />

### 2. My Queue Token
<img width="905" alt="QueueWise My Queue Token" src="https://github.com/user-attachments/assets/aa035317-df8b-4ec0-9e8f-e239cf8841e6" />

### 3. Visitor Queue Interface
<img width="958" alt="QueueWise Visitor Queue Interface" src="https://github.com/user-attachments/assets/8ca0799e-9711-48b0-b2eb-e57079dd497d" />

### 4. Queue Status and Tracking
<img width="959" alt="QueueWise Queue Status and Tracking" src="https://github.com/user-attachments/assets/eb74a6dd-e315-4c24-a92d-efdb4b409102" />

### 5. Visitor Token Generation
<img width="948" alt="QueueWise Visitor Token Generation" src="https://github.com/user-attachments/assets/521f63b2-f482-4689-9230-91832f3b304f" />

### 6. Staff and Counter Management
<img width="947" alt="QueueWise Staff and Counter Management" src="https://github.com/user-attachments/assets/7012f453-62a8-4adb-bcde-d926cded7c67" />

### 7. Queue Tracking and Analytics
<img width="955" alt="QueueWise Queue Tracking and Analytics" src="https://github.com/user-attachments/assets/791a8cd5-14a5-4189-8640-1a1c350ac907" />
## ✨ Key Features

- **Digital Token Generation:** Visitors can request a numbered token for their selected service.
- **Live Queue Tracking:** Track waiting and currently serving visitors.
- **Estimated Waiting Time:** Estimate waiting time using queue position and active counter availability.
- **Staff Dashboard:** Manage service counters and monitor queue activity.
- **Counter Management:** Activate or pause counters according to service availability.
- **Service Workflow:** Call the next visitor and mark service as completed.
- **Queue Analytics:** View operational information about queue activity.
- **Persistent Data:** Store token and counter records in an SQLite database.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Database integration | Flask-SQLAlchemy |
| Version control | Git and GitHub |
| Deployment | PythonAnywhere |

## 🔄 How It Works

1. A visitor selects a service and requests a token.
2. QueueWise generates a queue number.
3. The visitor waits while the dashboard tracks queue progress.
4. Staff call the next visitor using an available counter.
5. Staff complete the service, and the queue updates.

**Token lifecycle:** Waiting → Serving → Completed

## 💻 Run Locally

### Prerequisites

- Python 3 installed
- Git installed
- A terminal or command prompt

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/AsadMuneerAhmed/Queue-wise.git
cd Queue-wise
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment**

Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**5. Start the application**

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

> Follow the project's current configuration if your local environment uses a different startup command or port.

## 🎯 Project Goals

QueueWise aims to improve queue visibility, reduce uncertainty for visitors, and help staff coordinate service counters more efficiently.

The prototype demonstrates how a lightweight web application can support a more organized public-service experience.

## 🔮 Future Improvements

- Role-based visitor and staff authentication
- SMS or WhatsApp queue notifications
- Downloadable daily service reports
- More detailed queue performance analytics
- Automated testing and additional validation
- Accessibility and mobile usability improvements

## 👨‍💻 Project Information

**Project:** QueueWise — Smart Queue Management System  
**Event:** OpenHack’26  
**Developer:** Asad Muneer Ahmed  
**Repository:** [GitHub](https://github.com/AsadMuneerAhmed/Queue-wise)  
**Live Application:** [QueueWise Demo](https://asadali345.pythonanywhere.com/)

---

*Built to explore practical ways to make public-service queues clearer, smarter, and easier to manage.*
