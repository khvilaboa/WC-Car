import socket, pygame, platform, sys, xinput, time
from operator import attrgetter
from pygame.locals import *

# Status variables
delPressed = False
atrPressed = False
derPressed = False
izqPressed = False

# Feeble attempt to compensate for calibration and loose stick.
def stick_center_snap(value, snap=0.7):
    if value >= snap or value <= -snap:
        return value
    else:
        return 0.0

# Get the status of the outputs desired in format: (w)(s)(a)(d)
# Examples: 1000 (forward), 0101 (right and bakguards)
def getStatus():
	res = ""
	for status in [delPressed, atrPressed, izqPressed, derPressed]:
		res += "1" if status else "0"
	return res

pygame.init()
pygame.joystick.init()

joysticks = xinput.XInputJoystick.enumerate_devices()
device_numbers = list(map(attrgetter('device_number'), joysticks))

joystick = None
if not device_numbers:
	print "No se ha detectado ningun mando"
	sys.exit(1)
		
# Print the name of the controller
joystick_name = pygame.joystick.Joystick(device_numbers[0]).get_name().upper()
print "Mando conectado: %s" % joystick_name

# Get controller adapter (xinput) [supports triggers]
joystick = xinput.XInputJoystick(device_numbers[0])

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('172.19.32.200', 1234)  # Server address
print 'connecting to %s port %s' % server_address

try:
	while True:
		joystick.dispatch_events()
		
		for e in pygame.event.get():
			if e.type == JOYAXISMOTION:
				if e.axis == 2: 
					print "LEFT_TRGGER: %f" % e.value
				elif e.axis == 5:
					print "RIGHT_TRGGER: %f" % e.value
				elif e.axis == 1: # Sides
					if stick_center_snap(e.value * -1) <> 0: # Superior a la deadzone
						derPressed = e.value > 0
						izqPressed = not derPressed
					else:
						derPressed = False
						izqPressed = False
					print "Sides:", e.value
			elif e.type == JOYBUTTONDOWN:
				if e.button == 0: # A (gotta go front)
					print "Acelerar apretado"
					delPressed = True
				elif e.button == 1: # B (gotta go back)
					print "Frenar apretado"
					atrPressed = True
			elif e.type == JOYBUTTONUP:
				if e.button == 0: # A (stop going front)
					print "Acelerar soltado"
					delPressed = False
				elif e.button == 1: # B (stop going back)
					print "Frenar soltado"
					atrPressed = False

		status = getStatus()
		print "Status:", status
		sock.sendto(status, server_address)
		time.sleep(0.05)

finally:
    print 'closing socket'
    sock.close()
