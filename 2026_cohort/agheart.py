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

sense.show_message("AGHeart", 
                   text_colour=[255,0,0],
                  scroll_speed=0.05)

for i in range(18):
    b = (0, 0, 0)
    c = (255, 0, 0)
    
    rgb = sense.color # get the colour from the sensor
    c = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
    e = (rgb.red, rgb.green, rgb.blue) # use the sensed colour
    
    image = [
      b, b, b, b, b, b, b, b,
      b, b, c, b, c, b, b, b,
      b, c, c, c, c, c, b, b,
      b, c, c, c, c, c, b, b,
      b, b, c, c, c, b, b, b,
      b, b, b, c, b, b, b, b,
      b, b, b, b, b, b, b, b,
      b, b, b, b, b, b, b, b
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)

    b = (0, 0, 0)
    c = (255, 0, 0)
    d = (144, 96, 96)
    
    image = [
      e, e, e, e, e, e, e, e,
      e, e, d, e, d, e, e, e,
      e, d, c, d, c, d, e, e,
      d, c, c, c, c, c, d, e,
      e, d, c, c, c, d, e, e,
      e, e, d, c, d, e, e, e,
      e, e, e, d, e, e, e, e,
      e, e, e, e, e, e, e, e
    ]
    # Display the image
    sense.set_pixels(image)
    sleep(1)
    
x = (173, 39, 245)  # choose your own red, green, blue values between 0 - 255
sense.clear(x)