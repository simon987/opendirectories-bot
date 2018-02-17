# opendirectories-bot
Installation Instructions:

Python 3 is required to run the script.

To install Python 3 follow the steps below in Ubuntu (Other Distros too have same procedure).

Check installed Python version

$ python3 --version

To update installed Python to Python 3 run the following command

$ sudo apt-get update

If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.6 with the following commands:

$ sudo apt-get update

$ sudo apt-get install python3.6

If you’re using another version of Ubuntu (e.g. the latest LTS release), we recommend using the deadsnakes PPA to install Python 3.6:

$ sudo apt-get install software-properties-common

$ sudo add-apt-repository ppa:deadsnakes/ppa

$ sudo apt-get update

$ sudo apt-get install python3.6

Python 2.7.9 and later (on the python2 series), and Python 3.4 and later include pip by default.

To see if pip is installed, open a command prompt and run

$ command -v pip

Note that on some Linux distributions including Ubuntu and Fedora the pip command is meant for Python 2, while the pip3 command is meant for Python 3.

$ command -v pip3

To install pip, securely download get-pip.py. [1]:

$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

Inspect get-pip.py for any malevolence. Then run the following:

$ sudo python get-pip.py

Using the Script:

$ git clone https://github.com/simon987/opendirectories-bot.git

$ cd opendirectories-bot/

$ mkdir static/reports

$ pip3 install -r requirements.txt

$ python3 manual.py mkreport "{{URL}}" "{{6 character id}}"


Example Usage:

python3 manual.py mkreport "http://example.com/library/ePub/" "list.json" 

