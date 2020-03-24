import logging.config
import random
import os

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


class DataSplitter:

    def __init__(self, data_path, training_data_path, validation_data_path, image_extension, text_extension):

        # directory path with images and text files which
        # will be used as training and validation sets of data
        self.data_path = data_path
        # directory path where training data will be moved to
        self.training_data_path = training_data_path
        # directory path where validation data will be moved to
        self.validation_data_path = validation_data_path
        # extension of images
        self.image_extension = image_extension
        # extension of text files
        self.text_extension = text_extension

    # images without txt file will remain in the original folder
    def split(self, file_paths, validation_split):

        # shuffle data
        random.shuffle(file_paths)
        # calculate length of the list with file paths
        val_data_length = int(validation_split * len(file_paths))

        # check if folders for validation and training data exist and create if needed
        if not os.path.isdir(self.validation_data_path):
            os.makedirs(self.validation_data_path)
        if not os.path.isdir(self.training_data_path):
            os.makedirs(self.training_data_path)

        # move 20% of data to validation data folder
        for file_path in file_paths[:val_data_length]:
            txt_filename = os.path.basename(file_path)
            filename = os.path.splitext(txt_filename)[0]
            logging.debug('moving {} to the validation data folder: {}'.format(filename, self.validation_data_path))
            image_path = self.data_path + filename + self.image_extension
            # check if an image is available
            if os.path.isfile(image_path):
                os.rename(image_path, self.validation_data_path + filename + self.image_extension)
                os.rename(file_path, self.validation_data_path + txt_filename)
            else:
                logging.warning('an image for the existing file is not available: {}'
                                'files will not be moved to the validation data'.format(filename))

        # move 80% of data to training data folder
        for file_path in file_paths[val_data_length:]:
            txt_filename = os.path.basename(file_path)
            filename = os.path.splitext(txt_filename)[0]
            logging.debug('moving {} to the training data folder: {}'.format(filename, self.training_data_path))
            image_path = self.data_path + filename + self.image_extension
            # check if an image is available
            if os.path.isfile(image_path):
                os.rename(image_path, self.training_data_path + filename + self.image_extension)
                os.rename(file_path, self.training_data_path + txt_filename)
            else:
                logging.warning('an image for the existing file is not available: {}, '
                                'files will not be moved to the training data'.format(filename))
