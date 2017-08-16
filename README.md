# MeetUp #

### How do I get set up? ###

* Clone the repository
* Start a new python virtual environment

  ```pip install virtualenv```
  
  ```virtualenv meetup_venv```
  
  ```source meetup_venv/bin/activate```
  
* Download Requirements

  ```pip install -r requirements.txt```
* Database configuration
  - You'll need to setup a Neo4j instance
  - I used grapheneDB but any service will do
* Watson configuration
  - You'll need an account on IBM Bluemix and to setup a Natural Language Understanding instance.
  - rename the `constants_example.py` to `contants.py` and add in your information
* Deployment instructions
Run with: ```python run.py```
