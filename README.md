# 🧠 OS Deadlock Simulation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)

An interactive simulation of **Deadlock** in Operating Systems, showing how processes, resources, and schedulers interact in real-time. It includes deadlock detection and multiple visualization modes using Pygame and Tkinter.

> 🔬 Developed by **Rohit Payal**, **Ashish Chauhan**, and **Ujjawal**  
> 🎓 Presented to **Mrs. Akriti** as part of our Operating Systems coursework

---

## 🚀 Features

- 🌀 **Simulates process scheduling and resource management**
- 🔗 **Deadlock Detection** using Wait-For Graphs (WFG)
- 🎮 **Visualizations**:
  - Pygame visual interface (color-coded state display)
  - Tkinter GUI with enhanced status cards and process network view
- 📦 **JSON-based test cases** for easy input customization
- 🧩 **Modular Python codebase** for extendability


## 📁 Project Structure

deadlock-simulation/ ├── main.py # Main simulation engine
(Pygame-based) ├── tk_gui.py 
# GUI frontend using Tkinter ├── process.py 
# Process logic and actions ├── resource.py 
# Resource management ├── scheduler.py 
# Schedules process actions ├── deadlock_detector.py
# Detects cycles in Wait-For Graph ├── visualizer.py # Pygame visual representation ├── testcases/ 
# Contains test JSON files │ ├── case1.json │ └── ... ├── media└── README.md 
# This file



---

 ⚙️ Setup Instructions

 1. Clone the Repository
git clone https://github.com/student-Rohitpayal/DeadLock_simulation/new/main    <-(Copy the link of my repo)
cd deadlock-simulation

2. Install Required Packages

pip install pygame
python tk_gui.py


3. 🟢 Process States Legend (Visualizer)

State	Color
Running	🟢 Green
Waiting	🟡 Yellow
Deadlocked	🔴 Red
Terminated	⚫ Gray

🧠 How Deadlock is Detected
The deadlock_detector.py module builds a Wait-For Graph (WFG) every tick and detects cycles using depth-first search.
If a cycle is found, those processes are marked as Deadlocked.

🔮 Future Ideas
AI-based process strategies

Live editing of process/resource parameters

Web-based version of visualizer

🙌 Acknowledgments
Special thanks to Mrs. Akriti for her support and guidance throughout this project.
Made with 💻 by Rohit Payal, Ashish Chauhan, and Ujjawal.

🌟 Star this Repo
If you found this simulation interesting or useful, please consider giving it a ⭐️ on GitHub!
---

### ✅ You're Good to Go

Copy the above content into your `README.md`, update your GitHub repo link, and drop in a screenshot or GIF if you want a visual preview. Want help making that GIF or adding dark mode preview? Just say the word!

