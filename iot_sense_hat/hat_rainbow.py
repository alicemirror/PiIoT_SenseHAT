import time
from iot_sense_hat import SenseHat

'''
SenseHAT general purpose rainbow generator class
'''
class HatRainbow():

    def __init__(self):
        # RGB Array representing the state of the pixels colour
        self.pixels = [
            [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
            [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
            [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
            [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
            [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
            [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
            [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
            [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
        ]

        # Milleseconds sleeper
        self.msleep = lambda x: time.sleep(x / 1000.0)
        # SenseHAT class instance
        self.sense = SenseHat()

    def next_colour(self, pix):
        '''
        Dynamic next colour calculation for the pixels.
        :param pix: current involved pixel color values
        '''
        r = pix[0]
        g = pix[1]
        b = pix[2]

        if (r == 255 and g < 255 and b == 0):
            g += 1

        if (g == 255 and r > 0 and b == 0):
            r -= 1

        if (g == 255 and b < 255 and r == 0):
            b += 1

        if (b == 255 and g > 0 and r == 0):
            g -= 1

        if (b == 255 and r < 255 and g == 0):
            r += 1

        if (r == 255 and b > 0 and g == 0):
            b -= 1

        pix[0] = r
        pix[1] = g
        pix[2] = b


    def rainbow(self):
        '''
        Generate the rainbow screen calculating the next pixel colour for every pixel
        Note that changing the order of the pixels array visiting the rainbow direction changes
        :return:
        '''
        for pix in self.pixels:
            self.next_colour(pix)

        self.sense.set_pixels(self.pixels)
        self.msleep(1)
