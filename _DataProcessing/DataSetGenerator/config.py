import argparse

HSV_LOWER = [148, 255, 180]
HSV_UPPER = [152, 255, 255]


def parse_arguments():

    # initialize the parser
    parser = argparse.ArgumentParser()

    # add positional arguments
    parser.add_argument('command', help='create: saves automatically extracted bounding boxes (using supporting images)'
                                        'in text files, one file per image. Text files are placed in the folder'
                                        'of images will be split into training and validation sets of data; '
                                        'test: saves concatenated images: images for training/validation with '
                                        'drawn bounding boxes and supporting images; split: moves images and text '
                                        'files from data set into two folders: for training and validation data. '
                                        'If a text file for the image is missing, the image remains in the original '
                                        'folder; export: creates a text file with the list of all paths to images '
                                        'which should be used for training or validation. Images paths must not be '
                                        'the same as local, they should fit to the darknet structure',
                        type=str, choices=['create', 'test', 'split', 'export'])

    # add optional arguments
    parser.add_argument('-s', '--supporting_path',
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
                        help='the size of the validation data split in [0.0, 1.0] range, default: 0.2 '
                             'which means 20 percent validation and 80 percent training data',
                        type=restricted_float, default=0.2)
    parser.add_argument('-e', '--export_filename',
                        help='name of a text file which will be created to list all images for training '
                             'or validation. The file will be saved in the folder where listed images '
                             'are currently placed, default: retour', type=str, default='retour')
    parser.add_argument('-ep', '--export_path',
                        help='path where the images for training or validation will be placed in the darknet '
                             'structure. Remember to set different paths for training and validation data! '
                             'default: data/retour/', type=str, default='data/retour/')
    parser.add_argument('-es', '--export_data_set',
                        help='name of data set for which the final text file should be exporter, '
                             'default: training', type=str, default='training', choices=['training', 'validation'])

    parser_arguments = parser.parse_args()

    # set default hsv value if empty
    if not parser_arguments.hsv_lower:
        parser_arguments.hsv_lower = HSV_LOWER
    if not parser_arguments.hsv_upper:
        parser_arguments.hsv_upper = HSV_UPPER

    return parser_arguments


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError('{} is not a floating-point literal'.format(x))

    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError('{} is not in range [0.0, 1.0]'.format(x))
    return x
