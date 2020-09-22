import board
import busio
from digitalio import DigitalInOut
import time

from adafruit_pn532.i2c import PN532_I2C

class Rfid:

    def __init__(self):
        # i2c bus configuration
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # PN532 creation
        self.pn532 = PN532_I2C(self.i2c, debug=False)

        # Configure PN532 to communicate with MiFare cards
        self.pn532.SAM_configuration()

    #return uid in hexa str
    def read_uid(self):
        # Check if a card is available to read with a timeout of 1000 seconds
        uid = self.pn532.read_passive_target(timeout=1000)

        # If we have a card uid
        if uid is not None:
            # We use "".join(array) to create a string using a array and upper() to have uppercase
            return "".join([hex(i) for i in uid][2:]).upper()
        #If we don't have a card uid
        else:
            return False



if __name__ == "__main__":
    rf = Rfid()
    uid = rf.read_uid()
    print(uid)