#!/usr/bin/env python3

# import cv2
import neoapi
# import os
# from time import strftime, gmtime

class cameracontrol:
    cmd_CAPTUREIMG_help = "Capture an image from the camera and optionally save it."

    def __init__(self, config):
        # Store references
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # Read configuration parameters from the klipper config file 
        # self.save_path = config.get('save_path', '/tmp')
        # self.camera_features = {
        #     'PixelFormat': config.get('pixel_format', 'RGB8'),
        #     'ExposureTime': config.getfloat('exposure_time', 1000),
        #     'Gain': config.getfloat('gain', 10),
        #     'Gamma': config.getfloat('gamma', 1)
        #     }

        self._connect_cam()
        # self._set_camera_features()

        # Register G-Code command
        # Example usage: `CAPTURE_IMG CAM=mycam SAVE=1`
        self.gcode.register_mux_command('CAPTURE_IMG', 'CAM',
                                        config.get_name().split(' ')[-1],
                                        self.cmd_CAPTUREIMG,
                                        desc=self.cmd_CAPTUREIMG_help)

    def _connect_cam(self):
        """Connect to the camera using neoapi."""
        self.camera = neoapi.Cam()
        self.camera.Connect()
        if not self.camera.IsConnected():
            raise ConnectionError("Failed to connect to the camera")

    # def _set_camera_features(self):
    #     """Set camera features defined in the Klipper config."""
    #     for feature_name, feature_value in self.camera_features.items():
    #         try:
    #             self.camera.SetFeature(feature_name, feature_value)
    #         except Exception as e:
    #             self.gcode.respond_info(
    #                 f"Warning: Failed to set {feature_name} to {feature_value}: {e}"
    #             )

    # def capture_img(self, save=False):
    #     """Capture an image from the camera."""
    #     if not self.camera.IsConnected():
    #         self._connect_cam()

    #     img = self.camera.GetImage().GetNPArray()

    #     # Convert grayscale images to BGR if necessary
    #     if len(img.shape) == 2:  # Grayscale
    #         img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    #     save_path = None
    #     if save:
    #         file_name = f"img_{strftime(r'%d_%m_%y_%H_%M_%S', gmtime())}.bmp"
    #         save_path = os.path.join(self.save_path, file_name)
    #         cv2.imwrite(save_path, img)

    #     return img, save_path

    # def cmd_CAPTUREIMG(self, gcmd):
    #     # Parse arguments from G-Code
    #     save = gcmd.get_bool('SAVE', True)  # default SAVE=0 (not saved)
        
    #     # Capture the image
    #     img, path = self.capture_img(save=save)
        
    #     # Report to the user if the image was saved
    #     if save and path:
    #         self.gcode.respond_info(f"Image captured and saved to {path}")
    #     else:
    #         self.gcode.respond_info("Image captured (not saved).")

def load_config_prefix(config):
    return cameracontrol(config)
