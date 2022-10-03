# The Pico will check this file first to configure the usb settings

import usb_cdc
usb_cdc.enable(console=True, data=True)
