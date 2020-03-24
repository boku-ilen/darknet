import logging.config
import os
import cv2
import numpy as np

# configure logging
logger = logging.getLogger('MainLogger')

try:
    logging.config.fileConfig('logging.conf')
    logger.info('Logging initialized')
except:
    logging.basicConfig(level=logging.INFO)
    if not os.path.isfile('logging.conf'):
        logging.info('Could not find a configuration file: logging.conf')
    else:
        logging.info('Could not initialize: logging.conf misconfigured')


class BboxDrawer:

    def __init__(self, supporting_path, data_path, concatenation_path, image_extension, text_extension):

        # extension of images
        self.image_extension = image_extension
        # extension of text files
        self.text_extension = text_extension
        # directory path where images used for
        # bounding boxes creation are placed
        self.supporting_path = supporting_path
        # directory path with images and text files which
        # will be used as training and validation sets of data
        self.data_path = data_path
        # directory path where concatenated images will be saved
        self.concatenation_path = concatenation_path

        self.centroid_x = None
        self.centroid_y = None
        self.width = None
        self.height = None

        self.image_width = None
        self.image_height = None

    def draw_bboxes(self, filename):

        image = cv2.imread(self.data_path + filename + self.image_extension)
        logging.info('drawing bounding boxes for {}'.format(filename))
        self.image_height = image.shape[0]
        self.image_width = image.shape[1]

        # open the txt file
        text_file = open(self.data_path + filename + self.text_extension, "r")
        lines = text_file.readlines()
        for line in lines:
            line_elements = line.split(' ')
            if len(line_elements) != 5:
                logging.error('incorrect number of elements saved in the text file: {}'.format(filename))
            else:
                self.centroid_x = float(line_elements[1])
                self.centroid_y = float(line_elements[2])
                self.width = float(line_elements[3])
                self.height = float(line_elements[4])

            x_center = int(self.centroid_x * self.image_width)
            y_center = int(self.centroid_y * self.image_height)
            w = int(self.width * self.image_width)
            h = int(self.height * self.image_height)

            x_left = x_center - int(w/2)
            y_top = y_center - int(h/2)
            cv2.rectangle(image, (x_left, y_top), (x_left + w, y_top + h), (0, 0, 255), 2)

        # concatenate images for training/validation with drawn bounding boxes and supporting images
        supporting_filename = '2-' + filename[2:]

        # check if supporting image is available
        supporting_image_path = self.supporting_path + supporting_filename + self.image_extension
        if os.path.isfile(supporting_image_path):
            # concatenate images
            supporting_image = cv2.imread(supporting_image_path)
            concat_output_image = np.concatenate((image, supporting_image), axis=1)
        else:
            # save only one image with bounding boxes, without concatenation
            logging.warning('supporting image is not available, skipping concatenation for: {}'.format(filename))
            concat_output_image = image

        # save concatenated images
        if not os.path.exists(self.concatenation_path):
            logging.info('making a directory for concatenated images: {}'.format(self.concatenation_path))
            os.makedirs(self.concatenation_path)
        labeled_name = filename + self.image_extension
        path = self.concatenation_path + labeled_name
        cv2.imwrite(path, concat_output_image)
