<div align="center">

# 🛠️ Kaamgar Connect (कामगार कनेक्ट)
**Empowering the Blue-Collar Workforce Through Technology.**

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

*A bilingual, real-time job matching platform built to bridge the gap between skilled local workers and employers.*

[Explore Features](#-core-features) • [View UI Flow](#-user-workflows) • [Installation](#%EF%B8%8F-local-setup--installation) • [Tech Stack](#%EF%B8%8F-tech-stack)

</div>

---

## 🌟 The Vision: Why Kaamgar Connect?

Millions of skilled blue-collar workers (electricians, plumbers, drivers, daily wage laborers) struggle to find consistent work due to the digital divide. Traditional job portals are built for corporate roles, requiring complex resumes, formal English, and tedious email sign-ups. 

**Kaamgar Connect solves this.** We provide a highly accessible, localized digital bridge. By removing language barriers and utilizing password-less OTP authentication, we make it effortless for workers to showcase their skills and for local employers to hire reliable help instantly.

> **Mission:** *To formalize the informal sector by bringing dignity, transparency, and accessibility to local hiring.*

---

## ✨ Core Features: Tailored for Two Worlds

Kaamgar Connect features a strict role-based architecture, ensuring that both Workers and Employers have a UI customized exactly for their needs.

### 👷‍♂️ For the Workers (Kaamgar)
* **🗣️ Speak Your Language:** Instant English ↔ Hindi toggle. No more struggling with foreign menus.
* **📱 Simple Onboarding:** No passwords to forget. Secure OTP-based login. No resume required—just select your skills.
* **💼 Smart Job Board:** Browse jobs filtering by location, pay rate, and category (e.g., Construction, Domestic Help).
* **⚡ One-Click Apply:** Found a job? Apply instantly and track the status (Pending, Accepted, Rejected) in real-time.
* **💬 Direct Chat:** Talk directly to the employer to negotiate wages or discuss timing before accepting the job.

### 🏢 For the Employers (Malik)
* **🎯 Precision Hiring:** Post jobs with specific requirements, hourly/daily wages, and precise locations.
* **🔍 Worker Directory:** Don't want to wait for applicants? Browse public worker profiles and invite them to your job.
* **📋 Applicant Management Dashboard:** Review incoming applications cleanly. Accept or reject with a single click.
* **⚡ Real-Time Communication:** Use the built-in AJAX chat system to interview applicants without ever leaving the platform.

---

## 🎨 UI / UX Highlights

We believe utility shouldn't come at the cost of design. 
* **🌓 Seamless Dark Mode:** Built-in Dark/Light theme toggle that respects system preferences and saves battery on mobile devices.
* **⚡ Zero Page-Reload Chat:** Experience app-like messaging via optimized 3-second AJAX polling. No heavy WebSockets required.
* **📱 Mobile-First Responsive Design:** The entire platform, from dashboards to chat interfaces, scales perfectly to mobile screens where our primary users are.

---

## ⚙️ Tech Stack & Architecture

| Category | Technologies Used | Why we chose this? |
| :--- | :--- | :--- |
| **Backend** | Python, Django 4.2 | Rapid development, built-in ORM, and enterprise-grade security. |
| **Database** | MySQL 8.0 | High reliability and robust relational mapping for user roles and chats. |
| **Frontend** | HTML5, CSS3, Vanilla JS | Zero dependencies. Lightning-fast load times for users on slow 3G/4G networks. |
| **Media** | Pillow | Secure and optimized handling of user profile photo uploads. |

---

## 🛣️ User Workflows

### Scenario: Hiring an Electrician
1. **Employer** logs in and creates a job: *"Need an electrician in Bhopal for 4 hours."*
2. **Worker** (Ramesh, an electrician) opens the app in Hindi. He sees the job on his feed.
3. Ramesh hits **Apply**.
4. Employer gets a notification, reviews Ramesh's profile (rating, skills), and clicks **Accept**.
5. A **Chat Room** automatically opens between them to discuss the exact address. 🤝

---

## 🛠️ Local Setup & Installation

Want to run Kaamgar Connect on your machine? Follow these simple steps.

### 1. Prerequisites
Ensure you have the following installed:
* `Python 3.10+`
* `MySQL Server 8.0+`
* `Git`

### 2. Clone & Configure
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/kaamgar_connect.git](https://github.com/YOUR_USERNAME/kaamgar_connect.git)
cd kaamgar_connect

# Create a virtual environment & activate it
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

# Install all dependencies
pip install -r requirements.txt
