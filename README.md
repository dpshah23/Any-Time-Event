

# Any Time Event

## Table Of Contents

- [Documentation](#Documentation)
  - [Modules](#modules)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
<!-- - [Usage](#usage) -->


This project sets up the necessary environment using Docker and Docker Compose. Follow the instructions below to build and run the project.



# Documentation


  ## Modules

   - Authentication Module
   - Error Handling Module
   - Company Module
   - Paid Volunteer Module
---

  ### Authentication Module  
  The validate function processes OTP verification:
1.	POST Check: Ensures the request is a POST.
2.	Retrieve OTP: Collects the OTP digits and concatenates them.
3.	Get Email: Gets the user's email from the session.
4.	Validate OTP: Checks the OTP in the database and verifies it's not expired.
5.	User Role Handling:
    o	Volunteer: Sets cookies, session data, deletes the OTP, and redirects to the home page.
    o	Company: Sets cookies, session data, deletes the OTP, and renders the home page.
6.	Invalid OTP: Shows an error and reloads the OTP page if OTP is incorrect.
7.	Expired OTP: Shows an error and redirects to login if OTP is expired.
8.	Render OTP Page: Displays the OTP entry page for non-POST requests.




# getting-started

## prerequisites

    - Python (3.x)
    - Django
    - Docker




## Installation

To build the Docker images, run the following command:

```bash
docker-compose build
```

## Run

To start the Docker containers, run the following command:

```bash
docker-compose up
```

If you want to run the containers in detached mode (in the background), use the `-d` flag:

```bash
docker-compose up -d
```

