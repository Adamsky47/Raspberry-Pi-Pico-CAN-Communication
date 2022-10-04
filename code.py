# Importing required modules
from time import sleep
import board
import busio
import digitalio
from digitalio import DigitalInOut
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN
import usb_cdc


# Define the required pins for the CAN HAT
cs = DigitalInOut(board.GP17)
cs.switch_to_output()
spi = busio.SPI(board.GP18, board.GP19, board.GP16)

# Initialise the CAN transiever on the pico and set it to accept external data
can_bus = CAN(spi, cs, loopback=False, silent=True)
c = 0
x = True

# Set the LED GPIO pins
led = digitalio.DigitalInOut(board.GP28)
led.direction = digitalio.Direction.OUTPUT

# Initialize the USB device
usb_device = usb_cdc.data

# Set the receiver to listening and display the messages and sender ID
while True:
    with can_bus.listen(timeout=1.0) as listener:
        message_count = listener.in_waiting()
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from: ", hex(msg.id))
            # Check if the CAN HAT is trying to write data over the GPIO pins
            if isinstance(msg, Message):
                print("Message data:", msg.data)
                led.value = True
                sleep(0.5)
                led.value = False
                sleep(1)
                x = True
                while x == True:
                    # Write message to serial port
                    usb_device.write(msg.data)
                    sleep(1)
                    x = False
