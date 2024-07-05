# Message

## Table of Contents

1. [Project Overview](#1-project-overview)
1. [Installation](#2-installation)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
   - [Setup Environment](#setup-environment)
   - [Run the Application](#run-the-application)
1. [Configuration](#configuration)
   - [Environment Variables](#environment-variables)

---

## 1. Project Overview
![app-display](https://github.com/aptarr/multirealm-chat-app/assets/116022017/d6b635db-2069-4a30-9f99-cd830e6889c5)

Message is a chat application where users can communicate through text messages, sent according to a predefined protocol.

## 2. Installation

### Prerequisites

List all dependencies and prerequisites that need to be installed before setting up the project.

1. Python
2. Git

### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/aptarr/multirealm-chat-app.git
cd multirealm-chat-app
```

### Setup Environment

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Run the Application

- Development (if you run on local):
  -   start the server

  ```bash
  python3 server.py
  ```

  -   start the app

  ```bash
  flet run
  ```

- Production (if you run on the server):

  ```bash
   docker-compose up -d
  ```

## Configuration

### Environment Variables

- Development:

  - `TARGET_IP`= "127.0.0.1" default for run local you can change if you have server on the public IP.
  - `TARGET_PORT`= "8889" we using this port but you can change to other port
