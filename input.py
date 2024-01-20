import pygame

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

running = True

while running:
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            print("Axis motion:", event.axis, event.value)
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Button pressed:", event.button)

pygame.quit()