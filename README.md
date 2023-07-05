# Vamanit KIOSK

## Step-1
* Clone the project
* Use Python Version - 3.8.5
* create a virtual env
```
python3 -m venv virtualEnvName
```
* activate the virtual environment
```
source bin\activate
```
* Install the required packages
```
pip install -r requirements.txt
```


## Step-2
Initially create a sqlite3 database with the following details
* DB name as _kioskDB.db_
* table name as _locker_
* table fileds and data

|lockerNumber|occupied|lockerState|mobileNumber|otp|
|------------|--------|-----------|------------|---|
|1|0|0|None|None|
|2|0|0|None|None|
|3|0|0|None|None|

## Step-3
Configure the configuration file

Edit configuration.cfg
```

## Step-4
Run the code
```
python3 KioskUI.py
```

# Setup in Raspberry Pi 3

* Copy files from Code directory to ```/home/pi/```
    * can ignore VamanitKioskResources directory
* Copy daemon file to ```/lib/systemd/system/```
* copy SystemFiles directory to ```/usr/bin/```
* install required python packages from ```requirements.txt```
    * But for raspberry pi, Install pyqt by
        ```
        sudo apt install python3-pyqt5
        ```
* configure the configuration.cfg file
    ```
    [LOCKER]
    IP = 192.168.100.188
    PORT = 502

    [SMS]
    ACCOUNT_ID = ACcc46fe659d63da45991634d32b2770d3
    TOKEN = 7591be4983178c5aebffe346a9130e59
    MOBILE_NUMBER = +18509902103

    [DATABASE]
    PATH = kioskDB.db
    ```

# Useful Commands

* To convert ```.qrc``` file to python file
    ```
    pyrcc5 VamanitKioskResources/vamanitkioskresources.qrc -o ui_resources.py
    ```
# Autostart Application
* Make an autostart directory for the current user:
    ```
    mkdir -p ~/.config/autostart
    ```
* Create a .desktop file which runs the script:
    ```
    cat > ~/.config/autostart/vamanitkioskui.desktop << EOF
    [Desktop Entry] 
    Type=Application
    Exec=/usr/bin/python3 /home/pi/KioskUI.py
    EOF
    ```
