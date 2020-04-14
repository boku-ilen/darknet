import logging.config
import cv2
import os
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


MIN_CONTOUR_AREA = 0.0
# when using dilation 7x7 kernel it is like 3 pixels height
# smaller objects will not be labeled
MIN_HEIGHT = 9.0


# this class create a txt file for the given image, formatted for yolov3 object detection
# object class must be an integer >=0
# position must be given with float values relative to width and height of image
# line format: <object-class> <x_center> <y_center> <width> <height>
class BboxCreator:

    def __init__(self, supporting_path, data_path, text_extension, label, split_height, hsv_lower, hsv_upper):

        # directory path, where images used for
        # bounding boxes creation are placed
        self.supporting_path = supporting_path
        # directory path with images which will be used
        # as training and validation sets of data,
        # where also text files with bounding boxes will be saved
        self.data_path = data_path
        # extension of text files, which will be created
        self.text_extension = text_extension
        # label of detected objects
        self.label = label
        # height for splitting between two classes
        self.split_height = split_height
        # hsv color of detected objects
        self.hsv_range = np.array(hsv_lower), np.array(hsv_upper)

        # text file will be created for each image
        # to save there the label and objects position
        self.text_file = None
        # string to be saved in the text file
        self.string = None

    def save_bboxes(self, file_path):

        # save filename for naming txt file later
        supporting_filename = os.path.splitext(os.path.basename(file_path))[0]
        logging.info('creating bounding boxes for {}'.format(supporting_filename))

        # TODO: images should have any name, now they must start with '1-'
        # replace 2- with 1- at the beginning of the filename
        new_filename = '1-' + supporting_filename[2:]
        text_name = new_filename + self.text_extension

        # read a supporting image
        supporting_image = cv2.imread(file_path)

        # set a mask for the given colour
        image_hsv = cv2.cvtColor(supporting_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, self.hsv_range[0], self.hsv_range[1])
        # dilate the mask with a kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
        mask = cv2.dilate(mask, kernel, iterations=1)

        # find contours in the masked image
        major = cv2.__version__.split('.')[0]
        if major == '3':
            _, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        file_opened = False
        self.string = ""
        # write line in the file
        for contour in contours:

            # compute contour moments, which include area,
            # its centroid, and information about its orientation
            moments_dict = cv2.moments(contour)

            # create a name for text file if there is
            # at least one contour with minimal accepted area
            if not file_opened and moments_dict['m00'] >= MIN_CONTOUR_AREA:

                    # open the text file
                    self.text_file = open(self.data_path + text_name, 'w')
                    file_opened = True

            if file_opened:
                # create a bounding box if the area is greater or equal minimum
                if moments_dict['m00'] >= MIN_CONTOUR_AREA:

                    x, y, w, h = cv2.boundingRect(contour)
                    if h < MIN_HEIGHT:
                        logging.info('dimensions {}x{} to small for a bbox -> do not create'.format(w, h))
                    else:
                        label = self.label
                        color = (0, 0, 255)
                        if h <= self.split_height:
                            label += 1
                            color = (255, 0, 0)
                        # add line to the file
                        self.write_line(label, x, y, w, h, supporting_image.shape)
                        cv2.rectangle(supporting_image, (x, y), (x + w, y + h), color, 1)
                        logging.info('bbox dimensions in {}: {}x{}, label: {}'.format(supporting_filename, w, h, label))

        if file_opened:

            # write the string in file without the last new line
            self.text_file.write(self.string[:-1])
            # close the file
            self.text_file.close()

        else:
            logging.info('No bounding box found for the image: {}, no txt file created'.format(supporting_filename))

        # enables rejecting labeled images with key 'r'
        self.control_images(mask, supporting_image, new_filename, text_name)

    # add line to the file with the object class and its bbox in floats values
    def write_line(self, label, x, y, w, h, image_shape):

        width = float(w / image_shape[1])
        height = float(h / image_shape[0])
        x_center = float(x / image_shape[1]) + float(width/2)
        y_center = float(y / image_shape[0]) + float(height/2)
        self.string += '{} {} {} {} {}\n'.format(label, x_center, y_center, width, height)

    # show a labeled supporting image and its mask
    # reject with key 'r' or accept with an other key
    # if rejected, the txt file will be moved to 'to_correct' folder
    def control_images(self, mask, supporting_image, new_filename, text_name):
        # with r move txt to another folder (if corrections needed)
        cv2.imshow('mask', mask)
        cv2.imshow('bbox', supporting_image)
        key = cv2.waitKey(0)
        if key == 114:  # r=114 for remove
            logging.info('move {}.txt to correct'.format(new_filename))
            # check if folder exists and create if needed
            rejected_folder_name = 'to_correct'
            if not os.path.isdir(self.data_path + rejected_folder_name):
                os.makedirs(self.data_path + rejected_folder_name)
            os.rename(self.data_path + text_name,
                      self.data_path + rejected_folder_name + '/' + text_name)
