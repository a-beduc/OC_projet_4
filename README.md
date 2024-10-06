# Chess Tournament Application - Project 4

Fourth project for the online course of Python application development on OpenClassroom.

<p align="center">
    <img alt="Logo of the chess application" height="238" src="images/0-LOGO.png" title="Logo of the chess application" width="300"/>
</p>

## Description

This project is a terminal-based application designed to help chess clubs manage tournaments, including player pairing and tournament flow.

## Where are the data stored?

The user can manually modify the data stored in several `.JSON` files found in the `data` directory.  
Alternatively, the application can be used to create new players and tournaments directly.

## Installation

Ensure you have the following installed on your system:

- [Python 3.x](https://www.python.org/downloads/)

### Steps to Install

* Clone the project or download the files to your local machine:
    ```bash
    git clone https://github.com/a-beduc/formation_project_4
    ```
* Open a terminal and navigate to the project directory.
* Create a virtual environment:
    ```bash
    python -m venv venv
    ```
* Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
* Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Generate a Flake8 Report

* To generate a Flake8 HTML report, run the following command:
  ```bash
  flake8 --format=html --htmldir=flake8-report
  ```

## How to Run the Application
* From the terminal, navigate to the project directory.
* Activate the virtual environment:
    - On Windows:
        ```bash
        cd venv/Scripts/activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
* Execute the script:
    ```bash
    python main.py
    ```

<p align="center">
    <img alt="Image of the menu of the application" height="489" src="images%2F1-MENU.png" title="MENU" width="800"/>
</p>