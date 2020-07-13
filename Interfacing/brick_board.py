
import os
os.environ['BLINKA_FT232H'] = '1'   # board modue needs this variable set

import time
import board
import busio
import binascii

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
print("setup i2c")

fcc_address = 0x50
engine_address = 0x55
gear_address = 0x60

# Verify that everything is communicating as expected
avail = i2c.scan()
print("fcc_address present: {}".format("True" if fcc_address in avail else "False"))
print("engine_address present: {}".format("True" if engine_address in avail else "False"))
print("gear_address present: {}".format("True" if gear_address in avail else "False"))

def write_read(address, command, buf_size=1):
    i2c.writeto(address, command)
    print("wrote to address: 0x{:x}, value: {}".format(address, command))
    if buf_size > 0:
        buf = bytearray(buf_size)
        i2c.readfrom_into(address, buf)
        return buf
    return None

def test_engine_funcionality(engine_address):
    print("*************testing engine functionality")
    speed = write_read(engine_address, [0x10], 1)
    print("engine speed 0x{:x}".format(speed[0]))
    time.sleep(.1)

    # set new speed
    speed = write_read(engine_address, [0x11, 0x03], 1)
    print("set engine speed 0x03 response: 0x{:x}".format(speed[0]))
    time.sleep(.1)

    # set invalid speed
    speed = write_read(engine_address, [0x11, 0x07], 1)
    print("engine speed: 0x{:x}".format(speed[0]))
    time.sleep(.1)

    op_mode = write_read(engine_address, [0x31, 0x01])
    time.sleep(2)
    main_mode = write_read(engine_address, [0x41, 0x01])

    # previous invalid speed is now valid
    speed = write_read(engine_address, [0x11, 0x07], 1)
    print("engine speed: 0x{:x}".format(speed[0]))
    time.sleep(2)

    # previous invalid speed is now valid
    speed = write_read(engine_address, [0x11, 0x00], 1)
    print("engine speed: 0x{:x}".format(speed[0]))
    time.sleep(2)

    write_read(engine_address, [0xFE])
    print("Send RESET command")

    bad_cmd = write_read(engine_address, [0xDA], 1)
    print("bad command response: 0x{:x}".format(bad_cmd[0]))

def test_landing_gear_functionality(gear_address):
    print("*************testing landing gear functionality")
    pos = write_read(gear_address, [0x20], 1)
    print("Gear position: 0x{:x}".format(pos[0]))

    extend = write_read(gear_address, [0x21, 0x00])
    time.sleep(10)

    retract = write_read(gear_address, [0x21, 0x01])
    time.sleep(10)

def test_fcc_functionality(fcc_address):
    print("*************testing fcc functionality")

    op_mode = write_read(fcc_address, [0x31, 0x01])
    time.sleep(2)
    main_mode = write_read(fcc_address, [0x41, 0x01])
    time.sleep(2)

    print("Popping smoke")
    write_read(fcc_address, [0xb5, 0x01])

    write_read(fcc_address, [0xFE])
    print("Send RESET command")

    res = write_read(fcc_address, [0x51, 0x55, 0x80])
    print(res)

#test_engine_funcionality(engine_address)
#print("\n\n")
#test_landing_gear_functionality(gear_address)
#print("\n\n")
test_fcc_functionality(fcc_address)
