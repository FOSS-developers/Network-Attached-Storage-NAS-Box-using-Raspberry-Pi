# Network-Attached-Storage-NAS-Box-using-Raspberry-Pi
Network Attached Storage (NAS) Box using Raspberry Pi allows you to install comprehensive applications and services on your Raspberry Pi,
whenever you need them.


![Graphical User Interface](https://github.com/ntkathole/Network-Attached-Storage-NAS-Box-using-Raspberry-Pi/blob/master/1.png "Graphical User Interface")

The connectivity of NAS Box in network is as follows:

![Connectivity Diagram](https://github.com/ntkathole/Network-Attached-Storage-NAS-Box-using-Raspberry-Pi/blob/master/connectivity.jpg "Connectivity Diagram")

The technology stack includes:

![Technology Stack](https://github.com/ntkathole/Network-Attached-Storage-NAS-Box-using-Raspberry-Pi/blob/master/technical.jpg "Technology Stack")

To get started, you need to have Python and Flask installed.
Clone this repository and run the following commands to install prerequisites.

## Initial setup

You can run setup.py for installation of all pre-requisites having MariaDb database user as root and password
as root.
OR
You can manually install pre-requisites as follows.

### Installing Flask
    ```sh
    $ sudo apt-get install python-opencv 
    $ sudo apt-get install python-mysql.connector
    $ sudo apt-get install python-pip
    $ pip install flask
    $ pip install flask_mail
    $ pip install mysql
    ```

### Installing MariaDB database
    ```sh
    $ sudo apt-get install mariadb-server
    $ mysql_secure_installation
    ```

### Importing database
    ```sh
    $ mysql -u root -p
    $ mysql -u root -p nas < nas.dump
    ```

### Deploy flask app

1. Run a local server
    ```sh
    $ python app.py
    ```
2. Next, browse to http://0.0.0.0:5000

