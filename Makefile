install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python3 -m pytest -vv --cov=coreWeather test_coreWeather.py
	

lint:
	pylint --disable=R,C *.py

format: 
	black *.py

all: install lint test format deploy