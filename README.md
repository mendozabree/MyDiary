# MyDiary
[![Coverage Status](https://coveralls.io/repos/github/mendozabree/MyDiary/badge.svg?branch=without_tests)](https://coveralls.io/github/mendozabree/MyDiary?branch=without_tests)
[![Build Status](https://travis-ci.com/mendozabree/MyDiary.svg?branch=without_tests)](https://travis-ci.com/mendozabree/MyDiary)
[![Maintainability](https://api.codeclimate.com/v1/badges/4d73ae24b5343edbc393/maintainability)](https://codeclimate.com/github/mendozabree/MyDiary/maintainability)

This is a web application where one can write down their thoughts , feelings. Day to Day activities, it's a personal diary.

## Getting Started
This is the software that you need to get started with.

### Prerequisites

* Python 3.6 to 3.7
* pip
* postgresql 10


  [Here](https://www.python.org/getit/) is how to get python up and running

  [Here](https://pip.pypa.io/en/stable/installing/) is how to get pip up and running

  [Here](http://www.postgresqltutorial.com/install-postgresql/) is how to install postgresql


## Setting Up for Development
These are instructions for setting up MyDiary app in a development environment.

* Make a directory on your computer and a virtual environment
  ```
  $ mkdir Diary
  $ cd ~/Diary
  ```

* Prepare the virtual environment
    ```
    $ py -m venv myDiaryvenv
    $ myDiaryvenv/Scripts/actiavte
    ```

* Clone the project repo
  ```
  $ git clone https://github.com/mendozabree/My-Diary.git
  ```


* Install necessary requirements
  ```
  $ pip install -r myDiary/requirements.txt
  ```

* Create database and it's tables
  ```
  $ python database.py
  ```

* Run development server
  ```
  $ python run.py
  ```

This site should now be running at http://localhost:5000

These are the endpoints to test
![| METHOD       | Endpoint           | Description  |
| ------------- |:-------------:| -----|
| POST      | /api/v1/auth/signup | Signup a new user |
| GET      | /api/v1/auth/login | Login a user |
| GET      | /api/v1/entries | Get all entries |
| GET      | /api/v1/entries/id      | Get specific entry using an id |
| POST | /api/v1/entries      | Create a new entry |
| PUT      | /api/v1/entries/id      | Modify a specific entry using an id |]
<img style="float:left" src="https://github.com/mendozabree/MyDiary/blob/without_tests/endpoints.PNG" />

## Running the tests with coverage

* Setup environment variables
  ```
  $ set app_env=testing
  ```

* Running the tests
  ```
  $ nosetests -v --with-coverage --cover-package=api
  ```

## Deployment sites
The user interfaces are hosted at https://mendozabree.github.io/My-Diary/UI/index.html
A working demo of the application can be found at https://mydiary-cha3.herokuapp.com/
