## Shelfe

![Version](https://img.shields.io/badge/version-1.0.0-7B1FA2?style=flat)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white&style=flat)
![Streamlit](https://img.shields.io/badge/Web-Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat)
![Database](https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white&style=flat)
![API](https://img.shields.io/badge/API-Open%20Library-0D47A1?style=flat)
![License](https://img.shields.io/badge/License-Academic-4CAF50?style=flat)

Your personal book-reading manager built with Streamlit and MySQL.

### Overview

Shelfe is a Streamlit-based application crafted for a Database Management Lab. It showcases relational design, CRUD workflows, search/filtering, authentication, and API enrichment inside a single reading-management experience. Book metadata and cover art are pulled on demand via the Open Library Covers API to keep the UI lightweight yet visual.

### Academic Purpose

- apply SQL design concepts in a working web app
- demonstrate relational schema modeling
- execute CRUD actions through SQL queries
- practice filtering, search, and authentication logic
- connect MySQL persistence with a Python UI layer
- deliver an end-to-end full-stack database solution

### Core Features

**Authentication**

- secure sign-up/sign-in backed by MySQL credentials
- personalized shelves per user session

**Book Management (CRUD)**

- add new reads with notes and progress
- list catalog entries with key details
- update status, progress, or annotations
- delete records when finished

**Search & Filter**

- query by title or author keyword
- filter by reading status for quick context

**Dashboard**

- track reading progress by user
- visualize structured stats in Streamlit widgets

**Admin Panel**

- manage user accounts
- review system-wide logs and entries

**Book Covers & Metadata**

- fetch cover art from Open Library for a polished look
- avoid storing bulky media locally

### Technology Stack

| Technology | Role |
| --- | --- |
| Python | Core programming language |
| Streamlit | Frontend/web experience |
| MySQL | Relational datastore |
| mysql-connector-python | Database connectivity layer |
| Open Library Covers API | Metadata and imagery |

### Database Implementation

Shelfe models users, books, reading states, and admin actions in MySQL tables. SQL coverage includes:

- parameterized `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- `WHERE` filters and `LIKE` search clauses
- joins when correlating users with their books or status types

All database interactions are routed through Python helpers to maintain integrity and prevent SQL injection.

### Project Structure

```
Shelfe/
├── main.py            # Streamlit entry point
├── home.py            # Landing page
├── signin.py          # Auth logic
├── dashboard.py       # CRUD dashboard
├── admin_panel.py     # Admin controls
├── about.py           # About/info page
├── UI/                # UI components
├── DB_ss/             # Database references
├── ScreenShots/       # App visuals
├── requirements.txt   # Dependencies
├── sql.txt            # Schema & seed data
└── instruction.txt    # Setup directions
```

### How to Run

```bash
pip install -r requirements.txt
```

Configure MySQL using `sql.txt`, update credentials inside the Streamlit scripts, then launch:

```bash
streamlit run main.py
```

### Learning Outcome

- executed full CRUD cycles against MySQL
- bridged database theory with a Streamlit front end
- integrated external APIs for richer UX
- applied relational modeling, filtering, and search in practice
- delivered a cohesive full-stack database project
