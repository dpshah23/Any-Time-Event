# Any Time Event

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Run](#run)
- [Contact](#contact)

## Overview
Any Time Event is an online platform that connects companies needing event staff with individuals seeking paid volunteer opportunities. The platform aims to facilitate efficient event staffing, provide accessible paid volunteer opportunities, enhance user experience, and ensure reliable and secure transactions.

## Features

### Connects Companies with Volunteers for Events
The platform allows companies to post event staffing requirements and volunteers to apply for these opportunities. This helps companies find the right people for their events quickly and easily, and provides volunteers with opportunities to earn money while gaining experience.

### Secure Payment Processing with Razorpay
Payments are securely processed using Razorpay, ensuring that all transactions between companies and volunteers are safe and reliable. This feature supports various payment methods, including credit/debit cards, net banking, and UPI, providing flexibility and convenience for users.

### Real-Time Tracking of User Activities and Admin Activities
The application includes a comprehensive tracking system that monitors user activities and admin operations. This helps maintain transparency and accountability, allowing administrators to review and manage the platform effectively.

### User Authentication and Authorization
A robust authentication system ensures that only registered users can access the platform's features. Users can sign up, log in, and reset their passwords securely. Additionally, role-based access control ensures that volunteers and companies have access to the appropriate sections of the platform.

### Profile Picture and Identity Proof Uploads for Volunteers
Volunteers are required to upload their profile pictures and identity proofs during registration. This adds a layer of verification and trust, ensuring that companies can rely on the authenticity of the volunteers applying for their events.

## Technology Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** PostgreSQL hosted on Aiven
- **Payment Gateway:** Razorpay

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Docker

### Installation
To build the Docker images, run the following command:
```bash
docker-compose build
```

### Environment Variables
Environment variables are stored in multiple `.env` files across different folders. Below is a summary of the required variables without including sensitive information:

#### anytimeevent/.env
```
HOST=your_host
PORT=your_port
PASSWORD=your_password
```

#### auth1/.env
```
EMAIL=your_email
PASSWORD1=your_password
api_key='your_api_key'
api_secret='your_api_secret'
api_key_email_validation='your_api_key_email_validation'
```

#### company/.env
```
api_key_razorpay='your_api_key'
api_secret_razorpay='your_api_secret'
EMAIL=your_email
PASSWORD1=your_password
```

#### CustomAdmin/.env
```
EMAIL=your_email
PASSWORD1=your_password
acc_no=your_account_number
api_key='your_api_key'
api_secret='your_api_secret'
```

#### volunteers/.env
```
EMAIL=your_email
PASSWORD1=your_password
```

### Run
To start the Docker containers, run the following command:
```bash
docker-compose up
```

If you want to run the containers in detached mode (in the background), use the `-d` flag:
```bash
docker-compose up -d
```

## Contact
For any questions or feedback, please contact:
- **Name:** Any Time Event Team 
- **Email:** anytimeevent12@gmail.com

