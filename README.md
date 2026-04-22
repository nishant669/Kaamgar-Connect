<div align="center">

# 🛠️ Kaamgar Connect (कामगार कनेक्ट)
### **The Modern Proximity-Based Marketplace for Blue-Collar Talent**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-Real--time-3D72D7?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
[![UI](https://img.shields.io/badge/UI-Strict_Dark_SaaS-6366F1?style=for-the-badge)](https://tailwindcss.com/)

**Bridging the digital divide with high-performance proximity matching and a frictionless, bilingual interface.**

[Features](#-core-features) • [Technical Architecture](#-technical-highlights) • [Workflows](#-smart-workflows) • [Installation](#%EF%B8%8F-local-setup)

</div>

---

## 🌑 The UI/UX Philosophy: "Simplicity in the Dark"

Kaamgar Connect is built with a **Strict Dark Theme** (Midnight SaaS aesthetic) designed for high contrast and reduced eye strain. 

- **📱 Mobile-First:** Designed for workers on the move with large tap targets and bottom-navigation.
- **✨ Micro-Animations:** Uses AOS (Animate On Scroll) and CSS transitions for a premium, app-like feel.
- **💎 Glassmorphism:** Cards and Modals use subtle blurs and borders to create depth and hierarchy.
- **🗣️ Fully Bilingual:** One-tap switch between **English** and **Hindi** to ensure accessibility for all user demographics.

---

## 🎯 Core Features

### 👷 For Workers (Kaamgars)
- **📍 3km Radius Search:** Uses the **Haversine Formula** to find jobs within walking distance.
- **🔐 Password-less Auth:** Secure OTP-based login—no more forgotten passwords.
- **⚡ Instant Apply:** Apply for jobs in one tap; track status via a live-updating dashboard.
- **💬 Real-Time Chat:** Coordinate directly with employers via an integrated AJAX messaging system.

### 🏢 For Employers (Maliks)
- **📝 Effortless Posting:** Post jobs with precise geolocations and wage structures.
- **⭐ Real-Time Feedback:** Rate and review workers instantly upon task completion using **HTMX**.
- **📋 Applicant Analytics:** Filter and review worker profiles, ratings, and skills before hiring.
- **🔔 Live Notifications:** Get alerted the second a worker applies or sends a message.

---

## 🧠 Technical Highlights

| Feature | Implementation | Benefit |
| :--- | :--- | :--- |
| **Proximity Logic** | **Haversine Formula** (Python/SQL) | Precise distance calculation without expensive GIS tools. |
| **State Management**| **HTMX** | "Single Page Application" feel with zero page reloads. |
| **User Roles** | **Custom AbstractUser** | Clean, scalable database architecture for Workers vs Employers. |
| **Real-time Review**| **AJAX Partial Updates** | Instant UI feedback when ratings are submitted. |
| **Media** | **Pillow** | Optimized handling of profile photos and company logos. |

---

## 🔄 Smart Workflows

### 📍 Proximity Hiring
1. **Employer** posts a job for a "Plumber" at a specific coordinate.
2. **Worker** opens the app; the backend calculates that the job is **2.4km away**.
3. The job appears at the top of the worker's feed with a **"Nearby"** badge.

### 🤝 Real-time Feedback
1. Job is completed.
2. **Employer** clicks "Submit Review" on the dashboard.
3. **HTMX** intercepts the form, saves the rating, and updates the worker's public star-rating **instantly** without a refresh.

---

## ⚙️ Local Setup

### 1. Clone & Environment
```bash
git clone [https://github.com/nishant669/Kaamgar-Connect.git](https://github.com/nishant669/Kaamgar-Connect.git)
cd kaamgar_connect
python -m venv venv
# Windows
.\venv\Scripts\activate
