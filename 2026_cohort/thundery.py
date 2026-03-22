# Import the libraries
from sense_hat import SenseHat
from time import sleep

# Set up the Sense HAT
sense = SenseHat()
sense.set_rotation(270, False)

# Set up the colour sensor
sense.color.gain = 60 # Set the sensitivity of the sensor
sense.color.integration_cycles = 64 # The interval at which the reading will be taken

# Add colour variables and image
a = (255, 255, 255)
b = (0, 0, 0)
c = (255, 9, 5)
d = (29, 0, 250)
e = (247, 255, 5)
f = (20, 168, 0)

for i in range(8):

    rgb = sense.color # get the colour from the sensor
    b = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
    
    image = [
      d, d, d, c, c, d, d, b,
      b, d, b, c, b, d, b, b,
      b, d, b, c, c, d, d, b,
      b, d, b, b, c, b, d, b,
      d, d, d, c, c, d, d, b,
      b, b, b, b, b, b, b, b,
      b, b, b, b, b, b, b, b,
      b, b, b, b, b, b, b, b
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)
    
for i in range(8):

    rgb = sense.color # get the colour from the sensor
    
    a = (153, 50, 204)
    b = (255, 255, 0)
    c = (51, 153, 255)
    d = (0, 0, 0)
    e = (20, 168, 0)
    f = (247, 8, 8)
    g = (255, 255, 255)  # white/empty

    d = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
   
    image = [
      d, d, e, c, e, d, d, d,
      d, e, e, e, e, c, d, d,
      c, c, c, e, e, c, c, d,
      c, c, c, c, c, c, e, d,
      e, c, c, c, c, c, c, d,
      d, c, c, e, e, e, d, d,
      d, d, c, e, e, d, d, d,
      d, d, d, d, d, d, d, d
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)

for i in range(9):
    
    a = (153, 50, 204)
    b = (255, 255, 0)
    c = (51, 153, 255)
    d = (0, 0, 0)
    e = (255, 255, 255)  # white/empty
    
    image = [
      d, d, d, d, d, d, c, c,
      d, d, d, b, b, d, c, c,
      d, d, b, b, b, b, d, d,
      d, b, b, b, b, b, b, d,
      d, b, b, b, b, b, b, d,
      d, d, b, b, b, b, d, d,
      d, d, d, b, b, d, d, d,
      d, d, d, d, d, d, d, d
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)
    
sense.clear()