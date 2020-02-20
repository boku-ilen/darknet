import cv2
import os
import numpy as np


MIN_CONTOUR_AREA = 7.0


# this class create a txt file for the given image, formatted for yolov3 object detection
# object class must be an integer >=0
# position must be given with float values relative to width and height of image
# line format: <object-class> <x_center> <y_center> <width> <height>
class ImageProcessor:

    def __init__(self, conf):
        # text file will be created for each image
        # to save there the label and objects position
        self.text_file = None

        # get configurations
        self.conf = conf
        # label of detected objects
        self.object_class = conf["data"]["label"]
        # hsv color of detected objects
        self.hsv_range = np.array(conf["hsv"]["lower"]), np.array(conf["hsv"]["upper"])
        # data directory path
        self.dir_path = conf["data"]["dir"]

    def save_bboxes(self, file_path):

        # save filename for naming txt file later
        filename = os.path.splitext(os.path.basename(file_path))[0]
        print(filename)

        # replace 2- with 1- at the beginning of the filename
        new_filename = '1-' + filename[2:]
        txt_name = new_filename + ".txt"
        txt_dir = self.dir_path.replace('to_extract', 'to_train')

        # read the image
        image = cv2.imread(file_path)

        # set a mask for the given colour
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.hsv_range[0], self.hsv_range[1])
        # dilate the mask with a small kernel
        kernel = np.ones((2, 2), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

        # find contours in the masked image
        major = cv2.__version__.split('.')[0]
        if major == '3':
            _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        file_opened = False
        # write line in the file
        for contour in contours:

            # compute contour moments, which include area,
            # its centroid, and information about its orientation
            moments_dict = cv2.moments(contour)

            # create a name for txt file if there is
            # at least one contour with minimal accepted area
            if not file_opened and moments_dict["m00"] >= MIN_CONTOUR_AREA:

                    # open the txt file
                    self.text_file = open(txt_dir + txt_name, "w")
                    file_opened = True

            if file_opened:
                # create a bounding box if the area is greater than x
                if moments_dict["m00"] >= MIN_CONTOUR_AREA:
                    # compute the centroid of the contour
                    centroid_x = int((moments_dict["m10"] / moments_dict["m00"]))
                    centroid_y = int((moments_dict["m01"] / moments_dict["m00"]))

                    # x, y point the left upper corner, so centroid must be used
                    x, y, w, h = cv2.boundingRect(contour)
                    self.write_line(centroid_x, centroid_y, w, h, image.shape)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (40, 40, 40), 2)

        #cv2.imshow("mask", mask)
        #cv2.imshow("image", image)
        #cv2.waitKey(0)

        if file_opened:

            # close the file
            self.text_file.close()

    # add line to the file with the object class and its bbox in floats values
    def write_line(self, x, y, w, h, image_shape):
        x_center = float(x / image_shape[1])
        y_center = float(y / image_shape[0])
        width = float(w / image_shape[1])
        height = float(h / image_shape[0])
        self.text_file.write("{} {} {} {} {}\n".format(self.object_class, x_center, y_center, width, height))
