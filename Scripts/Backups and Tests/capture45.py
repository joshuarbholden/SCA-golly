from PIL import ImageGrab, Image
import pywinctl

# Capture the entire screen
#screen_image = ImageGrab.grab()


# Find golly window
screen_handle = pywinctl.getWindowsWithTitle("Golly", condition=pywinctl.Re.CONTAINS)[0].getHandle()

# Capture golly window
screen_image = ImageGrab.grab(window=screen_handle)

# rotate
screen_image = screen_image.rotate(-45, expand=True)

# Display the captured images
screen_image.show()
print('Captured the snapshot successfully...')
