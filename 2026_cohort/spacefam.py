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
   

a = (153, 50, 204)
b = (255, 255, 0)
c = (51, 153, 255)
d = (0, 0, 0)
e = (255, 255, 255)  # white/empty

for i in range(3):
    rgb = sense.color # get the colour from the sensor
    b = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
 
    image = [
      c, b, b, b, b, b, b, a,
      b, c, a, c, a, c, a, b,
      b, a, c, a, c, a, c, b,
      b, c, a, c, a, c, a, b,
      b, a, c, a, c, a, c, b,
      b, c, a, c, a, c, a, b,
      b, a, c, a, c, a, c, b,
      a, b, b, b, b, b, b, c
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)

for i in range(3):
    rgb = sense.color # get the colour from the sensor
    
    a = (153, 50, 204)
    b = (255, 255, 0)
    c = (51, 153, 255)
    d = (0, 0, 0)
    e = (255, 255, 255)  # white/empty

    b = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
 
    image = [
      e, c, e, e, c, e, e, e,
      e, e, e, c, e, c, e, c,
      c, e, a, a, a, a, e, e,
      e, e, a, a, a, d, b, c,
      e, c, a, a, a, a, e, e,
      c, e, c, e, c, e, e, c,
      e, e, e, e, e, e, c, e,
      c, e, c, e, e, c, e, e
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)

for i in range(3):
    rgb = sense.color # get the colour from the sensor
    
    						
    a = (153, 50, 204)
    b = (255, 255, 0)
    c = (51, 153, 255)
    d = (0, 0, 0)
    e = (165, 133, 255)
    f = (96, 0, 128)
    g = (67, 210, 45)
    h = (255, 255, 255)  # white/empty

    b = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
 
    image = [
      f, g, g, c, c, g, a, f,
      a, g, c, c, g, c, g, a,
      c, g, g, c, g, g, g, c,
      c, g, c, c, g, c, g, c,
      c, c, c, c, c, c, c, c,
      c, c, c, g, c, g, c, c,
      a, c, g, c, g, c, g, a,
      f, a, g, c, c, c, g, f
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)
    
sense.show_message("How's life in the stars, sausage?", text_colour=[255, 0, 0], scroll_speed=0.05)
sense.clear()
