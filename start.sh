#!/bin/bash
source ~/.virtualenvs/flask-workshop/bin/activate
export $(cat env | grep -v ^# | xargs)
flask run
