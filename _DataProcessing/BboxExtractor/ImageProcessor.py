import cv2
import os
import numpy as np


# this class create a txt file for the given image, formatted for yolov3 object detection
# object class must be an integer >=0
# position must be given with float values relative to width and height of image
# line format: <object-class> <x_center> <y_center> <width> <height>
class ImageProcessor:

    def __init__(self, conf):
        self.conf = conf
        self.text_file = None

        # get configurations
        self.object_class = self.conf["data"]["label"]
        self.hsv_range = np.array(self.conf["hsv"]["lower"]), np.array(self.conf["hsv"]["upper"])
        self.dir_path = self.conf["data"]["dir"]

    def save_bboxes(self, file_path):

        # save filename for naming txt file later
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # read the image
        image = cv2.imread(file_path)
        blurred = cv2.GaussianBlur(image, (11, 11), 0)

        # set a mask for the given colour
        image_hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.hsv_range[0], self.hsv_range[1])

        # find contours in the masked image
        major = cv2.__version__.split('.')[0]
        if major == '3':
            _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # open the file
        output_name = filename + ".txt"
        self.text_file = open(self.dir_path + output_name, "w")

        # write line in the file
        for contour in contours:
            # create a bounding box if the area is greater than zero
            if cv2.contourArea(contour) > 0:
                x, y, w, h = cv2.boundingRect(contour)
                self.write_line(x, y, w, h, image.shape)

        # TODO: remove the last new line if needed
        # close the file
        self.text_file.close()

    # add line to the file with the object class and its bbox in floats values
    def write_line(self, x, y, w, h, image_shape):
        x_center = float(x / image_shape[1])
        y_center = float(y / image_shape[0])
        width = float(w / image_shape[1])
        height = float(h / image_shape[0])
        self.text_file.write("{} {} {} {} {}\n".format(self.object_class, x_center, y_center, width, height))
