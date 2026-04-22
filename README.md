<div align="center">

<img src="https://capsule-render.vercel.app/render?type=soft&color=auto&height=200&section=header&text=Kaamgar%20Connect&fontSize=70&animation=fadeIn&fontAlignY=38" />

### **The Modern Proximity-Based Marketplace for Blue-Collar Talent**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![HTMX](https://img.shields.io/badge/HTMX-Real--time-3D72D7?style=for-the-badge&logo=htmx&logoColor=white)](https://htmx.org/)
[![UI](https://img.shields.io/badge/UI-Strict_Dark_SaaS-6366F1?style=for-the-badge)](https://tailwindcss.com/)

**Bridging the digital divide with high-performance proximity matching and a frictionless, bilingual interface.**

[Features](#-core-features) • [Technical Architecture](#-technical-highlights) • [Workflows](#-smart-workflows) • [Installation](#%EF%B8%8F-local-setup)

</div>

---

## 📸 Animated Preview
<div align="center">
  <table border="0">
    <tr>
      <td>
        <p align="center"><b>📍 3km Radius Logic</b></p>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxV3H6e1Uli/giphy.gif" width="300" />
      </td>
      <td>
        <p align="center"><b>💬 Real-Time Chat</b></p>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGJqZ3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5Z3R5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26tP4mE7DV1SshNde/giphy.gif" width="300" />
      </td>
    </tr>
  </table>
  <p><i>(Replace these with GIFs of your actual project dashboard to impress recruiters!)</i></p>
</div>

---

## 🌑 The UI/UX Philosophy: "Simplicity in the Dark"

Kaamgar Connect is built with a **Strict Dark Theme** (Midnight SaaS aesthetic).

<details>
<summary><b>✨ View Micro-Animations implemented</b> (Click to expand)</summary>

- **AOS (Animate On Scroll):** Elements glide into position as the user scrolls.
- **Pulse Indicators:** "Nearby" jobs feature a live green pulse animation to signify real-time data.
- **Glassmorphism:** Cards use 1px subtle borders and `backdrop-filter` for a premium feel.
- **Button Loading:** Buttons transform into spinners during OTP verification or Job Application.
</details>

- **📱 Mobile-First:** Designed for workers on the move with large tap targets.
- **🗣️ Fully Bilingual:** One-tap switch between **English** and **Hindi**.

---

## 🎯 Core Features

### 👷 For Workers (Kaamgars)
- **📍 3km Radius Search:** Uses the **Haversine Formula** to find jobs within walking distance.
- **🔐 Password-less Auth:** Secure OTP-based login—no more forgotten passwords.
- **⚡ Instant Apply:** Apply for jobs in one tap via a live-updating dashboard.

### 🏢 For Employers (Maliks)
- **📝 Effortless Posting:** Post jobs with precise geolocations.
- **⭐ Real-Time Feedback:** Rate workers instantly using **HTMX** (Zero Page Reloads).

---

## 🧠 Technical Highlights

| Feature | Implementation | Benefit |
| :--- | :--- | :--- |
| **Proximity Logic** | **Haversine Formula** | Sub-meter precision for local hiring. |
| **State Management**| **HTMX** | Desktop-app feel in a web browser. |
| **User Roles** | **Custom User Model** | Clean separation of Employer/Worker logic. |

---

## 🔄 Smart Workflows

<details>
<summary><b>🚀 See how the 3km logic works</b></summary>
1. Employer tags job at Coordinate (X, Y).
2. Worker lat/long is detected.
3. Python backend calculates: `Distance = 2 * R * asin(sqrt(a))`.
4. If distance < 3km, job is highlighted with a <b>Nearby Pulse</b>.
</details>

---

## ⚙️ Local Setup

```bash
git clone [https://github.com/nishant669/Kaamgar-Connect.git](https://github.com/nishant669/Kaamgar-Connect.git)
cd kaamgar_connect
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
