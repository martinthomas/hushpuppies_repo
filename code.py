# CircuitPython demo - NeoPixel
import time
import board
import neopixel
from digitalio import Direction, Pull, DigitalInOut
import adafruit_dotstar as dotstar

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.1)
dot[0] = (0,0,0)
dot.show()

# magnetic switch on D0(A2)
switch_d0 = DigitalInOut(board.D0)
switch_d0.pull = Pull.UP
 
class Paw(object):
    def __init__(self, pixel_pin, num_pixels, bright=0.7):
        
        # assuming the first two pixels are the paw and the remaining are the claws
        # so pretend only 5 pixels and duplicate 0 and 1 - offset pixel index by 1
        self.neopixels = neopixel.NeoPixel(pixel_pin, num_pixels+1, brightness=bright, auto_write=False)
    
    def show(self):
        self.neopixels.show()
        
    def __setitem__(self, key, value):
        if key ==0:
            self.neopixels[0] = value
            self.neopixels[1] = value
        else:
            self.neopixels[key+1] = value

    def fill(self, color):
        self.neopixels.fill(color)
            
            

pixel_pin = board.A0 # save A1, A2 for I2C
num_pixels = 5
pixels = Paw(pixel_pin, num_pixels)
        
def paw(color, wait):
    for i in range(num_pixels, 0, -1):
        pixels[i-1] = color
        pixels.show()
        time.sleep(wait)
        pixels[i-1] = BLACK
        pixels.show()
    time.sleep(0.5)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

while True:
    while switch_d0.value:
        color_chase(RED, 0.15)
        paw(PURPLE, 0.15)
        color_chase(YELLOW, 0.15)
        paw(PURPLE, 0.15)
        color_chase(RED, 0.15)

        pixels.fill(RED)
        pixels.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(0.5)

        pixels.fill(GREEN)
        pixels.show()
        time.sleep(0.5)

        pixels.fill(PURPLE)
        pixels.show()
        time.sleep(0.5)

        rainbow_cycle(0)  # Increase the number to slow down the rainbow

        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.5)