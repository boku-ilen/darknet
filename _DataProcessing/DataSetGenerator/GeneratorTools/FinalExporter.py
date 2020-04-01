import logging.config
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


class FinalExporter:

    def __init__(self, image_extension, text_extension):

        # extension of images
        self.image_extension = image_extension
        # extension of text files
        self.text_extension = text_extension

    def export(self, file_paths, data_set_path, export_filename, export_path, export_data_set):

        # create a text file with names of all images
        final_file_path = data_set_path + export_filename + self.text_extension
        final_file = open(final_file_path, "w")
        logging.info('creating a text file with the path: {}'.format(final_file_path))

        string = ""
        for file_path in file_paths:
            filename = os.path.splitext(os.path.basename(file_path))[0]
            logging.debug('saving \'{}\' to the text file'.format(filename))
            image_path = data_set_path + filename + self.image_extension
            # check if an image is available
            if os.path.isfile(image_path):
                # add image path to the string and then to the created text file
                string += "{}{}{}\n".format(export_path, filename, self.image_extension)
            else:
                logging.warning('an image for the \'{}\' file is not available, '
                                'the file will not be saved in the final text file'.format(filename))

        # write the string in file without the last new line
        final_file.write(string[:-1])

        # close the file with names of all images
        final_file.close()

