import logging.config
import os
import sys
import glob

from ParserManager import ParserManager
from GeneratorTools.BboxCreator import BboxCreator


# TODO: repair logging configuration
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


class DataSetGenerator:

    def __init__(self):

        # parse arguments, for meaning see --help
        parser = ParserManager()
        logging.info('Parsing arguments: {}'.format(parser.parser_arguments))
        self.command = parser.parser_arguments.command
        self.supporting_path = parser.parser_arguments.supporting_path
        self.data_path = parser.parser_arguments.data_path
        self.training_data_path = parser.parser_arguments.training_data_path
        self.validation_data_path = parser.parser_arguments.validation_data_path
        self.image_extension = parser.parser_arguments.image_extension
        self.text_extension = parser.parser_arguments.text_extension
        self.label = parser.parser_arguments.label
        self.hsv_lower = parser.parser_arguments.hsv_lower
        self.hsv_upper = parser.parser_arguments.hsv_upper

    def run(self):
        logging.info('Command: {}'.format(self.command))
        if self.command == 'create':

            bbox_creator = BboxCreator(self.supporting_path, self.data_path,
                                       self.text_extension, self.label, self.hsv_lower, self.hsv_upper)

            # set file paths to the supporting images
            file_paths = self.set_file_paths()
            for file_path in file_paths:
                # create txt files with the label and bounding boxes for each image
                bbox_creator.save_bboxes(file_path)

    def set_file_paths(self):

        # set data path for all files with the given extension
        data_path = self.supporting_path + self.image_extension.replace('.', '*')
        file_paths = glob.glob(data_path)
        # check if any files are found
        if not file_paths:
            sys.exit('No files found, check the path: {}'.format(data_path))
        return file_paths


# execute the main class
if __name__ == '__main__':
    main = DataSetGenerator()
    main.run()
