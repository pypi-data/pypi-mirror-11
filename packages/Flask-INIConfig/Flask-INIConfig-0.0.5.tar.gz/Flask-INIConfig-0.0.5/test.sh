#! /bin/bash

cd `dirname $0`

PYTHON=${PYTHON:=`which python`}

virtualenv -p $PYTHON _install
source _install/bin/activate
pip install nose coverage
pip install -e .
nosetests --with-coverage --cover-erase --cover-package flask_iniconfig test_flask_iniconfig.py $@
deactivate
