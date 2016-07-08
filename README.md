++++++++++++++++
webui automation
++++++++++++++++


Installation:
********************
Make sure to run "sudo apt-get update" before installing the packages.

1. Install python(atleast Python 2.7.6) 
2. Install python-nose(apt-get install python-nose)
3. Install git(apt-get install git)
4. Install python pip (apt-get install python-pip)
5. Install selenium(pip install -U selenium)
6. Install xvfb(apt-get install xvfb)
7. Install firefox(sudo apt-get install firefox=28.0+build2-0ubuntu2) Note: Make sure you have Firefox version 46.0.1 or below. 
8. Install vnc4server(apt-get install vnc4server)

Commnds to invoke automation:
***************************
1. Clone the testsuite from git - https://github.com/terafastnetworks/webui
2. Excecute below commands:
	cd ~/webui/testsuites
	vncserver :25 -geometry 1366x768 (Give any display number)
	export DISPLAY=:25
	echo $DISPLAY"
	echo "export PYTHONPATH=$HOME/webui/lib" >> $HOME/.bashrc
	echo "source $HOME/.bashrc"
3. Modify the config.txt file as per your switch info(eg: ip , ports (eg : 48))
4. Use python nosetests to run automation testsuites

nosetests command:
********************
1. nosetests -s python_file.py
2. nosetests -s python_file.py:class_name 
3. nosetests -s python_file.py:class_name.function_name python_file_2.py:class_name.function_name




















