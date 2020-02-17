import os
import glob
import sys
import json

from BboxExtractor.ImageProcessor import ImageProcessor


# this class creates a text file with object labels
# and position of bounding boxes around objects in given hsv range
# for each image in the configured directory
# set configurations first:
#     "dir" - data directory with / at the end
#     "ext" - files with wanted extension, e.g. "jpg", "png"
#     "label" - integer object number from 0 to (classes-1)
#     "lower" - array with hsv lower range
#     "upper" - array with hsv upper range
#     "name" - txt file name needed for yolov3, e.g. "retour_train.txt"
#     "image_path" - data path needed for yolov3, e.g. "data/retour/"
class BoundingBoxExtractor:

    def __init__(self):

        self.conf = None
        self.data_path = None
        self.image_processor = None

        self.dir_path = None
        self.images_names_file_name = None
        self.image_path = None

    def run(self):

        # load configurations
        with open('config.json') as conf_file:
            self.conf = json.load(conf_file)
        # data directory path
        self.dir_path = self.conf["data"]["dir"]
        # this file will be created once to save there
        # names of all images to train
        # started with 'data/retour/'
        self.images_names_file_name = self.conf["images_names_file"]["name"]
        # this path will be added before each
        # image name saved in the file
        self.image_path = self.conf["images_names_file"]["image_path"]

        # initialize image processing
        self.image_processor = ImageProcessor(self.conf)

        # create a file with names of all images
        images_names_file_dir = self.dir_path.replace('to_extract', 'to_train')
        images_names_file = open(images_names_file_dir + self.images_names_file_name, "w")

        # set file paths
        file_paths = self.set_file_paths()
        for file_path in file_paths:
            # create txt files with the label and bounding boxes for each image
            image_name = self.image_processor.save_bboxes(file_path)
            # write names of all images in the file
            images_names_file.write("{}{}.{}\n".format(self.image_path, image_name, self.conf["data"]["ext"]))

        # close the file with names of all images
        images_names_file.close()

    def set_file_paths(self):

        # set data path for all files with the given extension
        self.data_path = self.conf["data"]["dir"] + '*' + self.conf["data"]["ext"]
        file_paths = glob.glob(self.data_path)
        # check if any files are found
        if not file_paths:
            sys.exit("No files found, check the path")
        return file_paths


if __name__ == '__main__':
    main = BoundingBoxExtractor()
    main.run()

