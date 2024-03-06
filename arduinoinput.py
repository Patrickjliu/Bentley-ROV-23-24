import serial
import struct
import pygame
import math

pygame.init()
pygame.joystick.init()

num_controllers = pygame.joystick.get_count()

if num_controllers > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print("Controller connected:", controller.get_name())
else:
    print("No controller detected.")

# To get the number of axes, buttons, and hats on the controller
num_axes = controller.get_numaxes()
num_buttons = controller.get_numbuttons()
num_hats = controller.get_numhats()

# To read the input from the axes
axis_0 = controller.get_axis(0)
axis_1 = controller.get_axis(1)

# To read the input from the buttons (returns 1 if pressed, 0 if not pressed)
button_0 = controller.get_button(0)
button_1 = controller.get_button(1)

# To read the input from the hats (returns a tuple in the form (x, y))
hat_0 = controller.get_hat(0)

ser = serial.Serial('COM3', 9600)
    
def scaleVal(val):
    return math.log(val*10)

class Joystick:
    def __init__(self, joystick_id):
        self.joystick_id = joystick_id
        self.x = 0
        self.y = 0

    def updatex(self, new_x):
        x = scaleVal(new_x)
        return x
    
    def updatey(self, new_y):
        y = scaleVal(new_y)
        
        return y
        
    def get_position(self):
        return self.x, self.y

class PacketHandler:
    def handle_packet(self, motor_index, x, y):
        print(f"Motor {motor_index} -> X: {x}, Y: {y}")

class Motor:
    def __init__(self, opcode, x, y):
        self.opcode = opcode
        self.x = x
        self.y = y
    def data(self):
        return struct.pack('ff', self.x, self.y)
 
handler = PacketHandler()
joystick = Joystick(0)

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

    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.JOYAXISMOTION:
            print("Axis motion:", event.axis, event.value)
            if event.axis == 0:
                print(event.value)
                joystick.updatex(event.value)
            elif event.axis == 1:
                joystick.updatey(event.value)

        elif event.type == pygame.JOYBUTTONDOWN:
            print("Button pressed:", event.button)
    
    try:
        motors = getChangedMotors(joystick)

        packet_str = ""

        # Sending the number of motors as a single byte
        ser.write(bytes([len(motors)]))
        packet_str += f"Num Motors: {bytes([len(motors)]).hex()} "

        for motor in motors:
            ser.write(bytes([motor.opcode]))
            ser.write(motor.data())

            packet_str += f"Opcode: {bytes([motor.opcode]).hex()}, Data: {motor.data().hex()} "

        # Checking if the received byte is equal to the ASCII value of 1
        # if ser.read(1) == b'\x01':
        #     print("Success")
        # else:
        #     print("Failure")
        
        # print(packet_str)
        
    except KeyboardInterrupt:
        break

print("Sucess")

ser.close()