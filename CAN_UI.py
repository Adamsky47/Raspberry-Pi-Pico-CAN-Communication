import functools
from tkinter import *
import serial.tools.list_ports


# List of available ports
portsList = serial.tools.list_ports.comports()

# Blank serial object
srl_Obj = serial.Serial()

# Creating instance of tkinter
root = Tk()
root.config(bg='grey')
root.title('CAN UI')


# Declare function that sends index of button
def initComport(index):
    currentPort = str(portsList[index])
    comPortVar = str(currentPort.split(' ')[0])
    srl_Obj.port = comPortVar
    srl_Obj.baudrate = 115200
    srl_Obj.open()


# Loop through each entry in list and create button
for port in portsList:
    button = Button(root, text=port, font=('Calibri', 13), height=1, width=45,
                    command=functools.partial(initComport, index=portsList.index(port)))
    button.grid(row=portsList.index(port), column=0)

# Create data window
canvas = Canvas(root, width=600, height=400, bg='white')
canvas.grid(row=0, column=1, rowspan=100)

# Create a scroll bar
vsb = Scrollbar(root, orient='vertical', command=canvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')

# Create data Canvas
canvas.config(yscrollcommand=vsb.set)

# Create data frame
frame = Frame(canvas, bg='white')
canvas.create_window((10, 0), window=frame, anchor='nw')


# Function that checks for incoming data
def checkSerialPort():
    if srl_Obj.isOpen() and srl_Obj.inWaiting:
        packet = str(srl_Obj.read(size=8))
        recentPacketString = str(packet.split("'")[1])
        Label(frame, text='Message data: ' + recentPacketString, font=('Calibri', 13), bg='white').pack()


# Main Loop
while True:
    root.update()
    checkSerialPort()
    canvas.config(scrollregion=canvas.bbox('all'))
