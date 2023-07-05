import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QStackedWidget, QSizePolicy
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QEventLoop, Qt
import sqlite3
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from twilio.rest import Client
import random
import configparser
from PyQt5.QtGui import QCursor

# vamanitkioskresource.qrc resource file to python file ui_resources.py
import ui_resources

class AppUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Variables
        self.whoCalled = None  # containes who called for Mobile page takeaway or delivery. Based on that OTP page will be shown and for processing page and logic
        self.lockerIP = None
        self.lockerPort = None
        self.accountID = None
        self.token = None
        self.mobileNumber = None
        self.databasePath = None

        # getting configuration details from configuratons.cfg file
        self.getConfiguration()

        # load ui file
        uic.loadUi('kiosk.ui', self)

        """
        Index of pages StackedWidget Pages
        0 - KIOSK Home
        1 - Logistics Home
        2 - Mobile Number Home
        3 - OTP Number Home
        4 - Processing Message Home
        """
        # Display currently unavailable message for following services
        self.BankingButton.clicked.connect(self.showMessage)
        self.EducationButton.clicked.connect(self.showMessage)
        self.HealthcareButton.clicked.connect(self.showMessage)
        self.LogisticsButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.DeliveryButton.clicked.connect(self.forDelivery)
        self.TakeawayButton.clicked.connect(self.forTakeaway)
        self.MobileConfirmButton.clicked.connect(self.selectPage)
        self.MobileCancelButton.clicked.connect(self.goToHomepage)
        self.OtpCancelButton.clicked.connect(self.goToHomepage)
        self.OtpConfirmButton.clicked.connect(self.verifyOTP)

        # NumpadButton
        # adding action to each of the button in Mobile Number Page
        self.push1Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="1"))
        self.push2Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="2"))
        self.push3Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="3"))
        self.push4Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="4"))
        self.push5Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="5"))
        self.push6Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="6"))
        self.push7Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="7"))
        self.push8Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="8"))
        self.push9Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="9"))
        self.push0Button.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="0"))
        self.pushClearButton.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="clear"))
        self.pushDeleteButton.clicked.connect(lambda: numpadButtons(
            label="UserInputMobileLabel", text="delete"))

        # adding action to each of the button in OTP Number Page
        self.push1Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="1"))
        self.push2Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="2"))
        self.push3Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="3"))
        self.push4Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="4"))
        self.push5Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="5"))
        self.push6Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="6"))
        self.push7Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="7"))
        self.push8Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="8"))
        self.push9Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="9"))
        self.push0Button_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="0"))
        self.pushClearButton_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="clear"))
        self.pushDeleteButton_3.clicked.connect(
            lambda: numpadButtons(label="UserInputOtpLabel", text="delete"))

        # NumpadButton Action Methods

        def numpadButtons(label, text):
            """
            Two Labels: 
            Mobile Number Label - UserInputMobileLabel
            OTP Number Label - UserInputOtpLabel
            """
            if label == "UserInputMobileLabel":
                if text == "clear":
                    self.UserInputMobileLabel.setText("")
                elif text == "delete":
                    labelText = self.UserInputMobileLabel.text()
                    self.UserInputMobileLabel.setText(
                        labelText[:len(labelText)-1])
                else:
                    labelText = self.UserInputMobileLabel.text()
                    self.UserInputMobileLabel.setText(f"{labelText+text}")
            if label == "UserInputOtpLabel":
                if text == "clear":
                    self.UserInputOtpLabel.setText("")
                elif text == "delete":
                    labelText = self.UserInputOtpLabel.text()
                    self.UserInputOtpLabel.setText(
                        labelText[:len(labelText)-1])
                else:
                    labelText = self.UserInputOtpLabel.text()
                    self.UserInputOtpLabel.setText(f"{labelText+text}")

    def showMessage(self):
        self.MessageLabel.setText("Currently this service is unavailable")
        QTimer.singleShot(500, self.hideMessage)

    def hideMessage(self):
        self.MessageLabel.setText("")

    def forDelivery(self):
        self.whoCalled = 'delivery'
        self.stackedWidget.setCurrentIndex(2)

    def forTakeaway(self):
        self.whoCalled = 'takeaway'
        self.stackedWidget.setCurrentIndex(2)

    def selectPage(self):
        print(self.whoCalled)
        if self.whoCalled == 'delivery':  # for delivery
            # checking if number is valid
            if self.validateNumber(self.UserInputMobileLabel.text()):
                # go to processing page
                self.ProcessingMessageLabel.setText(
                    f"Please wait checking for locker availability.")
                self.stackedWidget.setCurrentIndex(4)
                # to wait for message to show for 2 seconds
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec_()
                # self.stackedWidget.setCurrentIndex(4)
                # check for locker availability
                available, lockerNumber = self.checkFreeLocker()
                if available:
                    print(f"Empty Locker No. {lockerNumber}")
                    print(f"Please put the package in locker:  {lockerNumber}")
                    self.ProcessingMessageLabel.setText(
                        f"Please put the package in locker:  {lockerNumber}")
                    QApplication.processEvents()
                    # open locker
                    result = self.openLocker(lockerNumber)
                    if not result:
                        # to wait for message to show for 2 seconds
                        print(f"Failed to Open locker.")
                        self.ProcessingMessageLabel.setText(
                            f"Failed to Open locker.")
                        QTimer.singleShot(2000, self.goToHomepage)
                        return
                    # check for its door closed
                    result = self.checkLockerState(lockerNumber)
                    if not result:
                        # to wait for message to show for 2 seconds
                        print(
                            f"Failed to check locker closeure. Please take help of Vamanit Assitance")
                        self.ProcessingMessageLabel.setText(
                            f"Failed to check locker closeure. Please take help of Vamanit Assitance")
                        QTimer.singleShot(2000, self.goToHomepage)
                        return
                    # generate otp
                    otp = self.generateOTP()
                    # save mobile number and otp in database
                    result = self.addMobileNumberAndOTPtoDB(
                        lockerNumber=lockerNumber, mobileNumber=self.UserInputMobileLabel.text(), Otp=otp)
                    if not result:
                        # to wait for message to show for 2 seconds
                        print(
                            f"Failed Save customer details. Please take help of Vamanit Assitance")
                        self.ProcessingMessageLabel.setText(
                            f"Failed Save customer details. Please take help of Vamanit Assitance")
                        QTimer.singleShot(2000, self.goToHomepage)
                        return
                    # send otp to customer
                    result = self.sendMessage(
                        toMobileNumber=self.UserInputMobileLabel.text(), Otp=otp)
                    if not result:
                        # to wait for message to show for 2 seconds
                        print(
                            f"Failed to send message to Customer. Please take help of Vamanit Assitance")
                        self.ProcessingMessageLabel.setText(
                            f"Failed to send message to Customer. Please take help of Vamanit Assitance")
                        QTimer.singleShot(2000, self.goToHomepage)
                        return
                    # completion message
                    self.ProcessingMessageLabel.setText(
                        f"Thank you for deliverying the package.")
                    QApplication.processEvents()
                    QTimer.singleShot(2000, self.goToHomepage)
                else:
                    self.ProcessingMessageLabel.setText(
                        f"No locker is available right now.\nAll lockers are full.")
                    QTimer.singleShot(2000, self.goToHomepage)
            else:
                self.ProcessingMessageLabel.setText(
                    f"Invalid number entered. Please try again.")
                self.stackedWidget.setCurrentIndex(4)
                QTimer.singleShot(2000, self.goToHomepage)
        else:  # for takeaway
            # checking if number is valid
            if self.validateNumber(self.UserInputMobileLabel.text()):
                # check in DB for given mobile number
                result, otp, lockerNumber = self.checkMobileNumberInDBandGetDetails(
                    mobileNumber=self.UserInputMobileLabel.text())
                if not result:
                    # to wait for message to show for 2 seconds
                    print(
                        f"There is no package for this mobile number: {self.UserInputMobileLabel.text()}")
                    self.ProcessingMessageLabel.setText(
                        f"There is no package for this mobile number: {self.UserInputMobileLabel.text()}")
                    self.stackedWidget.setCurrentIndex(4)
                    QTimer.singleShot(2000, self.goToHomepage)
                    return

                # GOTO OTP page
                self.stackedWidget.setCurrentIndex(3)
            else:
                self.ProcessingMessageLabel.setText(
                    f"Invalid number entered. Please try again.")
                self.stackedWidget.setCurrentIndex(4)
                QTimer.singleShot(2000, self.goToHomepage)

    def verifyOTP(self):
        self.ProcessingMessageLabel.setText("Verifying Details Please Wait")
        QApplication.processEvents()
        self.stackedWidget.setCurrentIndex(4)
        result, otp, lockerNumber = self.checkMobileNumberInDBandGetDetails(
            mobileNumber=self.UserInputMobileLabel.text())
        # validate otp
        if otp != self.UserInputOtpLabel.text():
            print(f"Otp is not correct.{otp, self.UserInputOtpLabel.text()}")
            self.ProcessingMessageLabel.setText(f"Otp is not correct.")
            QTimer.singleShot(2000, self.goToHomepage)
            return
        # open locker
        result = self.openLocker(lockerNumber)
        if not result:
            # to wait for message to show for 2 seconds
            print(f"Failed to Open locker.")
            self.ProcessingMessageLabel.setText(f"Failed to Open locker.")
            QTimer.singleShot(2000, self.goToHomepage)
            return
        self.ProcessingMessageLabel.setText(
            f"Please pickup your package in locker:  {lockerNumber}")
        QApplication.processEvents()
        # wait for locker to close
        result = self.checkLockerState(lockerNumber)
        if not result:
            # to wait for message to show for 2 seconds
            print(
                f"Failed to check locker closeure. Please take help of Vamanit Assitance")
            self.ProcessingMessageLabel.setText(
                f"Failed to check locker closeure. Please take help of Vamanit Assitance")
            QTimer.singleShot(2000, self.goToHomepage)
            return
        # remove the details from the locker database
        result = self.removeMobileNumberAndOTPtoDB(lockerNumber=lockerNumber)
        if not result:
            # to wait for message to show for 2 seconds
            print(
                f"Failed to remove customer details. Please take help of Vamanit Assitance")
            self.ProcessingMessageLabel.setText(
                f"Failed to remove customer details. Please take help of Vamanit Assitance")
            QTimer.singleShot(2000, self.goToHomepage)
            return
        # completion message
        self.ProcessingMessageLabel.setText(
            f"Thank you for using Vamanit Locker.")
        QApplication.processEvents()
        QTimer.singleShot(2000, self.goToHomepage)

    def goToHomepage(self):
        self.stackedWidget.setCurrentIndex(0)
        self.clean()

    def sendMessage(self, toMobileNumber, Otp):
        client = Client(self.accountID, self.token)
        toMobileNumber = '+91' + toMobileNumber
        try:
            message = client.messages.create(to=toMobileNumber, from_=self.mobileNumber,
                                             body=f"Hello there! You got a package. To collect your package use the otp {Otp} at vammanit locker")
            print(message)
        except Exception as e:
            print(e)
            return False
        return True

    # check for any locker empty
    def checkFreeLocker(self):
        try:
            freeLocker = False
            conn = sqlite3.connect(self.databasePath)

            cursor = conn.execute("SELECT lockerNumber, occupied from locker")
            for lockerNumber, occupied in cursor:
                # print(lockerNumber, occupied)
                if occupied == 0:
                    freeLocker = lockerNumber
                    break

            conn.close()
            if freeLocker:
                return True, freeLocker
            else:
                return False, None

        except Exception as e:
            print(e)

    def openLocker(self, lockerNumber):
        """
        returns true if locker coil is updated
        else returns false
        """
        UNIT = 0x1
        register = 100 + lockerNumber - 1
        try:
            client = ModbusClient(self.lockerIP, port=self.lockerPort)
            client.connect()
            rq = client.write_coil(register, True, unit=UNIT)
            client.close()
            print(f"rq Error: {rq.isError()}")
            if rq.isError():
                raise Exception("Unable to change coil value")
        except Exception as e:
            print(e)
            return False
        return True

    def checkLockerState(self, lockerNumber):
        UNIT = 0x1
        register = 100 + lockerNumber - 1
        try:
            while True:
                client = ModbusClient(self.lockerIP, port=self.lockerPort)
                client.connect()
                rr = client.read_coils(register, 1, unit=UNIT)
                print(f"rr Error: {rr.isError()}")
                if rr.isError():
                    raise Exception
                if rr.bits[0] == 0:
                    client.close()
                    break
                client.close()
                time.sleep(150)
            # client.close()
        except Exception as e:
            print(e)
            return False
        return True

    def generateOTP(self):
        """
        generate otp between 100000 to 999999 and return it 
        """
        return random.randint(100000, 999999)

    def addMobileNumberAndOTPtoDB(self, lockerNumber, mobileNumber, Otp):
        try:
            conn = sqlite3.connect(self.databasePath)
            cursor = conn.execute(
                f"UPDATE locker set occupied = '1', mobileNumber = '{mobileNumber}', otp = '{Otp}' WHERE lockerNumber = {lockerNumber}")
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False

        return True

    def removeMobileNumberAndOTPtoDB(self, lockerNumber):
        try:
            conn = sqlite3.connect(self.databasePath)
            cursor = conn.execute(
                f"UPDATE locker set occupied = '0', mobileNumber = 'None', otp = 'None' WHERE lockerNumber = {lockerNumber}")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def checkMobileNumberInDBandGetDetails(self, mobileNumber):
        try:
            conn = sqlite3.connect(self.databasePath)
            cursor = conn.execute(
                f"SELECT Otp, lockerNumber from locker WHERE mobileNumber = {mobileNumber}")
            row = cursor.fetchone()
            if row is not None:
                # entry present in locker(True), otp, lockerNumber
                return True, row[0], row[1]
        except Exception as e:
            print(e)

        return False, None, None

    def clean(self):
        """
        Cleans all the User Input Fields
        """
        self.UserInputMobileLabel.setText("")
        self.UserInputOtpLabel.setText("")

    def validateNumber(self, number):
        print(number, len(number))
        # if len(number) == 10 or len(number) == 12:
        if len(number) == 10:
            return True
        else:
            return False

    def getConfiguration(self):
        try:
            config = configparser.ConfigParser()
            config.read('configuration.cfg')
            self.lockerIP = config['LOCKER']['IP']
            self.lockerPort = config['LOCKER']['PORT']
            self.accountID = config['SMS']['ACCOUNT_ID']
            self.token = config['SMS']['TOKEN']
            self.mobileNumber = config['SMS']['MOBILE_NUMBER']
            self.databasePath = config['DATABASE']['PATH']
        except Exception as e:
            print("Error getting configuration")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    UI = AppUI()
    UI.show()
    # make it full screen
    UI.showFullScreen()
    # remove cursor from screen
    UI.setCursor(QCursor(Qt.BlankCursor))
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Windows.')
