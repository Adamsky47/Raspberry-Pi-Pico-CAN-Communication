# The Pico will check this file first to configure the serial communication settings

import usb_cdc
usb_cdc.enable(console=True, data=True)
