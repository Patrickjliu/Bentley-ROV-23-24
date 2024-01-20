import serial
import struct

ser = serial.Serial('COM3', 9600)

class Joystick:
    def __init__(self, joystick_id):
        self.joystick_id = joystick_id

    def get_position(self):
        return 0, 0

class PacketHandler:
    def handle_packet(self, motor_index, x, y):
        print(f"Motor {motor_index} -> X: {x}, Y: {y}")

class Motor:
    def __init__(self, opcode, x, y):
        self.opcode = opcode
        self.x = x
        self.y = y
    def data(self, x, y):
        return struct.pack('ff', self.x, self.y)
 
handler = PacketHandler()
joystick = Joystick()

def getChangedMotors(joystick):
    motors = []

    joystick_x, joystick_y = joystick.get_position()

    motors.append(Motor(opcode=0, x=joystick_x, y=joystick_y))
    motors.append(Motor(opcode=1, x=joystick_x, y=joystick_y))

    # for i in range(4):
    #     joystick_x, joystick_y = joystick.get_position()
    #     motors.append(Motor(opcode=i, joystick_x=joystick_x, joystick_y=joystick_y))

    return motors

while True:
    
    try:
        motors = getChangedMotors(joystick)

        start_marker = ser.write(len(motors))
        
        for i in motors:
            ser.write(i.opcode)
            ser.write(i.data())

        ser.read(1) == 1
    except KeyboardInterrupt:
        break

ser.close()