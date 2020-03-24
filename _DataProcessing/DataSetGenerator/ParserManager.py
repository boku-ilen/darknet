import argparse

HSV_LOWER = [148, 255, 180]
HSV_UPPER = [152, 255, 255]


class ParserManager:

    def __init__(self):

        self.parser_arguments = self.parse()

    @staticmethod
    def parse():

        # initialize the parser
        parser = argparse.ArgumentParser()

        # add positional arguments
        parser.add_argument('command', help='', type=str, choices=['create', 'test', 'split', 'export'])

        # add optional arguments
        parser.add_argument('-s,', '--supporting_path',
                            help='absolute or relative path to your folder with supporting images, '
                                 'which are used to extract the bounding boxes',
                            type=str, default='_test_data/supporting_data/')
        parser.add_argument('-d', '--data_path',
                            help='absolute or relative path to your folder with images for your set of data, they '
                                 'will be later split into training and validation data sets',
                            type=str, default='_test_data/data/')
        parser.add_argument('-c', '--concatenation_path',
                            help='absolute or relative path to your folder where concatenated images will be saved',
                            type=str, default='_test_data/concatenated/')
        parser.add_argument('-t', '--training_data_path',
                            help='absolute or relative path to your folder where your images '
                                 'for training data sets will be moved to',
                            type=str, default='_test_data/data/training/')
        parser.add_argument('-v', '--validation_data_path',
                            help='absolute or relative path to your folder where your images '
                                 'for validation data sets will be moved to',
                            type=str, default='_test_data/data/validation/')
        parser.add_argument('-i', '--image_extension',
                            help='extension of your images, default: .png', type=str, default='.png')
        parser.add_argument('-x', '--text_extension',
                            help='extension of your text files, default: .txt', type=str, default='.txt')
        parser.add_argument('-l', '--label',
                            help='label which will be given the bounding boxes, default: 0', type=int, default=0)
        parser.add_argument('-hl', '--hsv_lower',
                            help='lower border of hsv values, which will be accepted as blobs for bounding boxes, '
                                 'default: {}'.format(HSV_LOWER), nargs='+', type=int)
        parser.add_argument('-hu', '--hsv_upper',
                            help='lower border of hsv values, which will be accepted as blobs for bounding boxes, '
                                 'default: {}'.format(HSV_UPPER), nargs='+', type=int)
        parser.add_argument('-vs', '--validation_split',
                            help='the size of the validation data split, default: 0.2 '
                                 'which means 20% validation and 80% training data', type=float, default=0.2)
        parser.add_argument('-e', '--export_filename',
                            help='name of a text file which will be created to list all images for training '
                                 'or validation. The file will be saved in the folder where listed images '
                                 'are currently placed. default=retour', type=str, default='retour')
        parser.add_argument('-ep', '--export_path',
                            help='path where the images for training or validation will be placed in the darknet '
                                 'structure. Remember to set different paths for training and validation data! '
                                 'default=data/retour/', type=str, default='data/retour/')
        parser.add_argument('-es', '--export_data_set',
                            help='name of data set for which the final text file should be exporter, '
                                 'default=training', type=str, default='training', choices=['training', 'validation'])

        parser_arguments = parser.parse_args()

        # set default hsv value if empty
        if not parser_arguments.hsv_lower:
            parser_arguments.hsv_lower = HSV_LOWER
        if not parser_arguments.hsv_upper:
            parser_arguments.hsv_upper = HSV_UPPER

        return parser_arguments
