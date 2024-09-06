# Microservices Project Structure Generator

This project provides a script to generate a standardized directory structure for microservices projects.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Structure Script](#structure-script)
4. [Generated Directory Structure](#generated-directory-structure)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Project Overview

This repository contains a Bash script called `structure.sh` that automates the creation of a consistent directory structure for microservices projects. It helps developers quickly set up new microservices with a standardized layout, improving project organization and reducing setup time.

## Getting Started

To use this project:

1. Clone the repository:
```
git clone <repository-url> 
cd <repository-directory>
```
## Structure Script

The `structure.sh` script creates a directory structure for multiple microservices. It generates the following components for each service:

- Source code directory (`src`)
- Test directory (`tests`)
- Configuration directory (`config`)
- Placeholder Python files (`__init__.py`, `main.py`)
- Test file template
- Dockerfile
- Requirements file
- README.md file
- Makefile

The script creates files only if they don't already exist, making it safe to run repeatedly without overwriting existing files.

## Generated Directory Structure

After running the script, your project will have the following structure:
```
/services
├── /auth-service
│   ├── /src
│   │   ├── __init__.py
│   │   └── main.py
│   ├── /tests
│   │   └── test_auth.py
│   ├── /config
│   │   └── settings.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── Makefile
├── /user-service
│   ├── /src
│   │   ├── __init__.py
│   │   └── main.py
│   ├── /tests
│   │   └── test_user.py
│   ├── /config
│   │   └── settings.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── Makefile
├── /payment-service
│   ├── /src
│   │   ├── __init__.py
│   │   └── main.py
│   ├── /tests
│   │   └── test_payment.py
│   ├── /config
│   │   └── settings.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── Makefile
├── /order-service
│   ├── /src
│   │   ├── __init__.py
│   │   └── main.py
│   ├── /tests
│   │   └── test_order.py
│   ├── /config
│   │   └── settings.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── README.md
│   └── Makefile
└── /inventory-service
    ├── /src
    │   ├── __init__.py
    │   └── main.py
    ├── /tests
    │   └── test_inventory.py
    ├── /config
    │   └── settings.py
    ├── Dockerfile
    ├── requirements.txt
    ├── README.md
    └── Makefile
```