# Dikuprosjekt REST API - v.0.1 (Alpha Testing)

The sourcecode for http://feedback.uib.no/. Built on python, svelte and MongoDB.

## Prerequisites 
* [Python 3.8](https://www.python.org/downloads/release/python-383/)
* [Pip 20.1.1](https://pypi.org/project/pip/)
* [Docker / Docker-compose](https://hub.docker.com/)
* [Node](https://www.npmjs.com/get-npm)
* Install `pipenv` 
  * Windows: `python -m pip install pipenv`
  * Unix: `python3 -m pip install pipenv` 
* Set environment variables for `API_KEY` and `API_URL` in your system.



## Local Setup:
1. Clone this repository by running `git clone https://github.com/arienshibani/dikuprosjekt` in the terminal. 
2. Navigate to the root folder and run `docker-compose up` in a terminal to start MongoDB. Do not close this terminal!
3. Open a 2nd terminal and navigate to `dikuprosjekt/server`. 
4. Run `pipenv shell` then `pip install -r requirements.txt` to setup the server dependancies. 
5. Run `python main.py` to start the server. Do not close this terminal!
   * The database API will run on `https:localhost:5000/`. 
5. Open a third terminal and navigate to `dikuprosjekt/frontend/app`. Run `npm install`. 
6. Run `npm run dev` to spin up the frontend and click around. Do not close this terminal!
   * The application will be hosted on `https:localhost:3000/`.

## Known Issues:
* If you are not using Windows 10 pro, you might experience problems with docker and hyper v. Make sure that you are using Windows 10 pro or a Unix based OS with docker.
* Make sure that `pip` and `python` are in PATH.
* When setting up your environment variables, make sure that they do not have trailing slashes.
* Make sure to populate your database before trying to use the frontend application.
   * Run `populate_database.py` in order to quickly fill up each chapter with test data.
   * To add questions or feedback and test the API visit `http://localhost:5000/apidocs`.

