import logging.config
import os
import sys
import glob


from DataSetGenerator import config
from DataSetGenerator.GeneratorTools.BboxCreator import BboxCreator
from DataSetGenerator.GeneratorTools.BboxDrawer import BboxDrawer
from DataSetGenerator.GeneratorTools.DataSplitter import DataSplitter
from DataSetGenerator.GeneratorTools.FinalExporter import FinalExporter


# configure logging
logger = logging.getLogger('MainLogger')

try:
    logging.config.fileConfig('logging.conf')
    logger.info('logging initialized')
except:
    logging.basicConfig(level=logging.INFO)
    if not os.path.isfile('logging.conf'):
        logging.info('could not find a configuration file: logging.conf')
    else:
        logging.info('could not initialize: logging.conf misconfigured')


# this class contains a set of tools used for creation of training and validation sets of data,
# using supporting images (with objects to label in defined hsv color) and images which will be split
# into training and validation sets of data. See --help to see available arguments.
# See comments in the run definition for commands details.
class DataSetGenerator:

    def __init__(self):

        # parse arguments, for meaning see --help
        parser_arguments = config.parse_arguments()
        logging.info('parsing arguments: {}'.format(parser_arguments))
        self.command = parser_arguments.command
        self.supporting_path = parser_arguments.supporting_path
        self.data_path = parser_arguments.data_path
        self.concatenation_path = parser_arguments.concatenation_path
        self.training_data_path = parser_arguments.training_data_path
        self.validation_data_path = parser_arguments.validation_data_path
        self.image_extension = parser_arguments.image_extension
        self.text_extension = parser_arguments.text_extension
        self.label = parser_arguments.label
        self.split_height = parser_arguments.split_height
        self.hsv_lower = parser_arguments.hsv_lower
        self.hsv_upper = parser_arguments.hsv_upper
        self.validation_split = parser_arguments.validation_split
        self.export_filename = parser_arguments.export_filename
        self.export_path = parser_arguments.export_path
        self.export_data_set = parser_arguments.export_data_set

    def run(self):

        # control whether directories with data exist
        for path in [self.supporting_path, self.data_path]:
            if not os.path.isdir(path):
                logging.error('directory with needed data does not exist: {}'.format(path))
                raise FileNotFoundError('directory with needed data does not exist: {}'.format(path))

        logging.info('command: {}'.format(self.command))

        # saves automatically extracted bounding boxes (using supporting images)
        # in text files, one file per image. Text files are placed in the folder
        # of images which can be later split into training and validation sets of data
        if self.command == 'create':

            # initialize the bounding boxes creator
            bbox_creator = BboxCreator(self.supporting_path, self.data_path, self.text_extension, self.label,
                                       self.split_height, self.hsv_lower, self.hsv_upper)

            # set file paths to all the supporting images
            file_paths = self.set_file_paths(self.supporting_path, self.image_extension)

            # for each image: create txt files
            # with the label and bounding boxes
            for file_path in file_paths:

                # TODO: images should have any name, now they must start with '1-'
                # save a filename without an extension
                filename = os.path.splitext(os.path.basename(file_path))[0]
                # replace 2- with 1- at the beginning of the filename
                new_filename = '1-' + filename[2:]

                # check if image with the same name is available
                if os.path.isfile(self.data_path + new_filename + self.image_extension):
                    bbox_creator.save_bboxes(file_path)
                else:
                    logging.warning('an image {} is not available -> do not create a text file'.format(new_filename))

        # saves concatenated images: images for training/validation
        # with drawn bounding boxes and supporting images
        elif self.command == 'test':

            # initialize the bounding boxes drawer
            bbox_drawer = BboxDrawer(self.supporting_path, self.data_path, self.concatenation_path,
                                     self.image_extension, self.text_extension)

            # set file paths to all the text files
            file_paths = self.set_file_paths(self.data_path, self.text_extension)

            # for each text file except retour_train file
            # and if an image with the same name available:
            # draw bounding boxes and save concatenated images
            for file_path in file_paths:

                # save a filename without an extension
                filename = os.path.splitext(os.path.basename(file_path))[0]

                # check if image with the same name is available
                if os.path.isfile(self.data_path + filename + self.image_extension):
                    # draw bounding boxes for each image
                    bbox_drawer.draw_bboxes(filename)
                else:
                    logging.warning('{} will not be saved, missing an image with the same name'.format(filename))

        # moves images and text files from data set
        # into two folders: for training and validation data.
        # If a text file for the image is missing,
        # the image remains in the original folder
        elif self.command == 'split':

            # initialize the data splitter
            data_splitter = DataSplitter(self.data_path, self.training_data_path, self.validation_data_path,
                                         self.image_extension, self.text_extension)

            # set file paths to all the text files
            file_paths = self.set_file_paths(self.data_path, self.text_extension)

            # split data
            logging.info('splitting {} files into training and validation data'.format(len(file_paths)))
            data_splitter.split(file_paths, self.validation_split)

        # creates a text file with the list of all paths
        # to images which should be used for training or validation.
        # Images paths must not be the same as local,
        # they should fit to the darknet structure
        elif self.command == 'export':

            # set chosen data path
            data_set_path = self.training_data_path
            if self.export_data_set == 'validation':
                data_set_path = self.validation_data_path

            # initialize the final file exporter
            final_exporter = FinalExporter(self.image_extension, self.text_extension)

            # set file paths to all the text files
            file_paths = self.set_file_paths(data_set_path, self.text_extension)

            # export text file with all images paths
            logging.info('exporting a text file: {}'.format(self.export_filename))
            final_exporter.export(file_paths, data_set_path, self.export_filename,
                                  self.export_path, self.export_data_set)

    @staticmethod
    def set_file_paths(path, ext):

        # set data path for all files with the given extension
        data_path = path + ext.replace('.', '*')
        file_paths = glob.glob(data_path)
        # check if any files are found
        if not file_paths:
            sys.exit('No files found, check the path: {}'.format(data_path))
        return file_paths


# execute the main class
if __name__ == '__main__':
    main = DataSetGenerator()
    main.run()
