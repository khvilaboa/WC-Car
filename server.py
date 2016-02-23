import socket, sys, time
import RPi.GPIO as GPIO

PIN_DEL = 23
PIN_ATR = 24
PIN_DER = 17
PIN_IZQ = 27

#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_DEL, GPIO.OUT) 
GPIO.setup(PIN_ATR, GPIO.OUT) 
GPIO.setup(PIN_DER, GPIO.OUT) 
GPIO.setup(PIN_IZQ, GPIO.OUT)

def cleanInputs():
    GPIO.output(PIN_DEL, False)
    GPIO.output(PIN_ATR, False)
    GPIO.output(PIN_DER, False)
    GPIO.output(PIN_IZQ, False)

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("172.19.32.200", 1234)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)
print 'waiting for messages...'


"""
Protocol:
Server reads message like:
forward-back-left-right
1000 (forward)
0101 (backwards, turning right)
"""


while True:
    cmd, addr = sock.recvfrom(1024)
    print 'message from', addr

    if cmd == "1000":
        print "acelerar sin girar"
        GPIO.output(PIN_DEL, True)
        GPIO.output(PIN_ATR, False)
        GPIO.output(PIN_DER, False)
        GPIO.output(PIN_IZQ, False)
    elif cmd == "0100":
        print "marcha atras"
        GPIO.output(PIN_DEL, False)
        GPIO.output(PIN_ATR, True)
        GPIO.output(PIN_DER, False)
        GPIO.output(PIN_IZQ, False)
    elif cmd == "0010":
        print "frenado izquierda"
        GPIO.output(PIN_DEL, False)
        GPIO.output(PIN_ATR, False)
        GPIO.output(PIN_DER, False)
        GPIO.output(PIN_IZQ, True)
    elif cmd == "0001":
        print "frenado derecha"
        GPIO.output(PIN_DEL, False)
        GPIO.output(PIN_ATR, False)
        GPIO.output(PIN_DER, True)
        GPIO.output(PIN_IZQ, False)
    elif cmd == "1001":
        print "acelerando y derecha"
        GPIO.output(PIN_DEL, True)
        GPIO.output(PIN_ATR, False)
        GPIO.output(PIN_DER, True)
        GPIO.output(PIN_IZQ, False)
    elif cmd == "1010":
        print "acelerando e izquierda"
        GPIO.output(PIN_DEL, True)
        GPIO.output(PIN_ATR, False)
        GPIO.output(PIN_DER, False)
        GPIO.output(PIN_IZQ, True)
    elif cmd == "0101":
        print "atras y derecha"
        GPIO.output(PIN_DEL, False)
        GPIO.output(PIN_ATR, True)
        GPIO.output(PIN_DER, True)
        GPIO.output(PIN_IZQ, False)
    elif cmd == "0110":
        print "atras e izquierda"
        GPIO.output(PIN_DEL, False)
        GPIO.output(PIN_ATR, True)
        GPIO.output(PIN_DER, False)
        GPIO.output(PIN_IZQ, True)
    elif cmd == "0000":
        print "quieto parao"
	cleanInputs()
    else:
        print "mi no entender"
    time.sleep(0.05)
GPIO.cleanup()
