from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
import time
import os
from itertools import izip_longest
from numpy import array

def main():
    while True:
        os.system('clear')
        print(vertStrings(bcd(time.strftime('%H%M%S'))))
        print(str(time.strftime("%H:%M:%S", time.gmtime())))
        time.sleep(.2)

# bcd :: iterable(characters '0'-'9') -> [str]
def bcd(digits):
    'Convert a string of decimal digits to binary-coded-decimal.'
    def bcdigit(d):
        'Convert a decimal digit to BCD (4 bits wide).'
        # [2:] strips the '0b' prefix added by bin().
        return bin(d)[2:].rjust(4, '0')
    return (bcdigit(int(d)) for d in digits)

# VertStrings, converts BCD to vertical collumns of text
def vertStrings(strings):
    'Orient an iterable of strings vertically: one string per column.'
    iters = [iter(s) for s in strings]
    concat = ''.join
    return '\n'.join(map(concat, izip_longest(*iters, fillvalue=' ')))

#TODO: Define method for translating the vertical string into tuple on and off states for tuples containing coordinates.
#Add the individual led states to a two dimensional array consisting of tuples []
#def drawClock(draw):
#    iters = [iter(s) for s in draw]
#    for ledstate in iters



while True:
    main()

