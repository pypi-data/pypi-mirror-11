REQUIREMENTS
------------

tipy is written for Python 3.

On debian: $ sudo apt-get install python3

You will also need pip for python3.

On debian: $ sudo apt-get install python3-pip

In order to install tipy using the setup.py you will need the setuptools module.

On debian: $ sudo apt-get install python3-setuptools

The GUI require the Qt library with Python bindings.

On debian: $ sudo apt-get install python3-pyqt5

INSTALLATION
------------

Install with pip3:

$ sudo pip3 install tipy

Install from sources:

$ sudo python3 setup.py install

After the installation you will need to change the owner of ~/.config/tipy.
The directory is created during the installation, which require root permissions
and therefore set every created file owner to root.
Typing the following should works:

$ sudo chown <your_user_name> -R ~/.config/tipy/
