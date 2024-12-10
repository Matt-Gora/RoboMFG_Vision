from logging import PlaceHolder
import yaml
import cv2
import neoapi
from time import strftime, gmtime
import os
import numpy as np

class CameraControl:
    def __init__(self, printer_config, cam_config: str) -> None:
        # Load camera configuration from the YAML file
        with open(cam_config, 'r') as config_file:
            self.cam_config = yaml.safe_load(config_file)
        
        # Connect to the camera
        self._connect_cam()

    def _connect_cam(self):
        """Connect to the camera using neoapi."""
        self.camera = neoapi.Cam()
        self.camera.Connect()
        if not self.camera.IsConnected():
            raise ConnectionError("Failed to connect to the camera")
        
        # Optionally set the camera to capture color images
        self.camera.SetFeature('PixelFormat', 'RGB8')  # Adjust this if needed for your camera

    def capture_img(self, save: bool = False):
        """Capture an image from the camera."""
        if not self.camera.IsConnected():
            self._connect_cam()

        img = self.camera.GetImage().GetNPArray()

        # Convert grayscale images to BGR if necessary
        if len(img.shape) == 2:  # Grayscale image has no color channels
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # Save the image if requested
        if save:
            file_name = f"img_{strftime('%d_%m_%y_%H_%M_%S', gmtime())}.bmp"
            save_path = os.path.join(self.cam_config.get('save_path'), file_name)
            cv2.imwrite(save_path, img)
            return img, save_path

        return img

# Initialize the camera controller with a placeholder and config file
placeholder = []
cam = CameraControl(placeholder, 'cam_config.yaml')

# Capture an image
result = cam.capture_img()

# Extract the image if a tuple is returned
img = result if isinstance(result, np.ndarray) else result[0]

# Display the captured image
cv2.imshow('Captured Image', img)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()  # Close all OpenCV windows
