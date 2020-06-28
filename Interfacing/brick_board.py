import time

import board
import busio


# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
print("setup i2c")

avail = i2c.scan()
print(avail)


def write_read(address, command):
    i2c.writeto(address, command)
    print("wrote to address")
    buf = bytearray(100)
    i2c.readfrom_into(address, buf)
    return buf


write_read(88, [0xAA, 0x00])
write_read(84, [0xAA, 0x00])
write_read(86, [0xAA, 0x00])

time.sleep(3)

write_read(88, [0xAA, 0x01])
write_read(84, [0xAA, 0x01])
write_read(86, [0xAA, 0x01])

# stop - full - stop
for i in range(8):
    write_read(88, [0x23, i])
    time.sleep(.2)

for i in range(7, -1, -1):
    write_read(88, [0x23, i])
    time.sleep(.2)

write_read(86, [0x77, 0x01])
write_read(86, [0x99, 0x01])
