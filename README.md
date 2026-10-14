# QueueWise — Smart Queue Management System

**Smarter queues. Better service. Less uncertainty.**

QueueWise is a web-based queue management system designed to make public-service visits more organized and transparent. It enables visitors to obtain digital tokens, track queue progress, and view estimated waiting times while staff manage service counters and visitor flow through a central dashboard.

> **Project status:** Independent prototype developed for OpenHack’26. QueueWise is inspired by public-service centres and is not affiliated with or endorsed by NADRA.

## 🚀 Live Demo

**[Open QueueWise](https://asadali345.pythonanywhere.com/)**

Explore the deployed application to see the queue management workflow in action.

## 📸 Screenshots

Screenshots of the actual running application will be added here.

<!-- Replace these paths with screenshots captured from the real application. -->
<!-- Save screenshot files in the docs/screenshots/ folder. -->

### Main Dashboard
![QueueWise Main Dashboard](<img width="959" height="437" alt="image" src="https://github.com/user-attachments/assets/fba6c45f-3924-4465-b269-2520a2327f51" />
)

### Visitor Token Generation
![Visitor Token Generation](docs/screenshots/visitor-token.png)

### Staff and Counter Management
![Staff Counter Management](docs/screenshots/staff-dashboard.png)

### Queue Tracking and Analytics
![Queue Tracking and Analytics](docs/screenshots/queue-analytics.png)

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
