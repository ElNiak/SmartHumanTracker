install:
	sudo apt-get --fix-missing -y install python3 python3-dev python3-pip
	python3 -m venv penv
	. penv/bin/activate
	pip3 install wheel
	pip3 install .

run:
	. penv/bin/activate
	python3 src/main.py 
