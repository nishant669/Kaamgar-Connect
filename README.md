# 🛠️ Kaamgar Connect (कामगार कनेक्ट)

### 🚀 Proximity-Based Marketplace for the Blue-Collar Workforce

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql)](https://www.mysql.com/)
[![Frontend](https://img.shields.io/badge/UI-Strict_Dark_Theme-1E293B?style=flat)](https://tailwindcss.com/)
[![HTMX](https://img.shields.io/badge/Real--time-HTMX-3D72D7?style=flat)](https://htmx.org/)

**Kaamgar Connect** is a modern, bilingual job marketplace designed to bridge the gap between local skilled workers (Kaamgars) and employers (Maliks). Built with a focus on ease of use, it features high-performance proximity matching and a real-time feedback ecosystem.

---

## 🌟 Key Innovations

### 📍 Smart Proximity Matching (3km Radius)
Unlike traditional job boards, Kaamgar Connect uses the **Haversine Formula** to calculate real-time geographic distances. 
- Users can filter jobs or workers within a **3km radius** or custom distances.
- Optimized backend queries ensure fast results without heavy GIS dependencies.

### ⚡ Real-Time Review System (HTMX)
A seamless, no-reload feedback system.
- Employers can rate and review workers instantly after job completion.
- Reviews are injected into the DOM via **HTMX**, providing a "Single Page Application" feel.

### 🌑 "Eye-Comfort" Dark Interface
A strictly dark-themed, professional UI/UX.
- Developed with **Tailwind CSS/Bootstrap 5** using a Deep Slate palette (`#0F172A`).
- Focuses on accessibility, high contrast for outdoor visibility, and smooth micro-animations.

---

## 🎯 Core Features

### 👷 For Workers (Kaamgars)
- **Bilingual Support:** Toggle between Hindi and English seamlessly.
- **OTP-Based Access:** Simplified login via mobile/OTP for accessibility.
- **Location-Aware Feed:** Discover daily-wage work available within walking distance.
- **Status Tracking:** Real-time updates on application acceptance/rejection.

### 🏢 For Employers (Maliks)
- **Instant Job Posting:** Mobile-optimized forms for quick posting.
- **Candidate Analytics:** View worker ratings and previous feedback before hiring.
- **Direct Communication:** Integrated real-time chat UI for coordination.
- **Verification System:** Mark workers as "Trusted" based on completed tasks.

---

## 🧠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Django 6.0 (Python) |
| **Database** | MySQL / SQLite (Development) |
| **Real-time Engine** | HTMX & AJAX |
| **Frontend** | Tailwind CSS / Bootstrap 5, Javascript |
| **Geolocation** | Geopy / Haversine Formula |
| **Media Handling** | Pillow (Profile & Logo management) |

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nishant669/Kaamgar-Connect.git](https://github.com/nishant669/Kaamgar-Connect.git)
   cd Kaamgar-Connect
