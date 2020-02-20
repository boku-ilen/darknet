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

        # initialize image processing
        self.image_processor = ImageProcessor(self.conf)

        # set file paths
        file_paths = self.set_file_paths()
        for file_path in file_paths:
            # create txt files with the label and bounding boxes for each image
            self.image_processor.save_bboxes(file_path)

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

