import serial

mySerial = serial.Serial()
mySerial.baudrate = 115200
mySerial.port="/dev/ttyUSB0"
mySerial.open()

values = b'1'
#bytearray([10,20,30,40,50])
mySerial.write(values)

# total = 0
#
# while total <len(values):
#     print( ord(mySerial.read(1)))
#     total+=1

mySerial.close()