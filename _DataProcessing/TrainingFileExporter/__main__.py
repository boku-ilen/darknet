import json
import glob
import sys
import os


class TrainingFileExporter:

    def __init__(self):

        self.conf = None
        self.data_path = None

        self.dir_path = None
        self.images_names_file_name = None
        self.image_path = None

        self.run()

    def run(self):
        # load configurations
        with open('config.json') as conf_file:
            self.conf = json.load(conf_file)
        # data directory path
        self.dir_path = self.conf["exporter"]["dir"]
        # this file will be created once to save there
        # names of all images to train
        # started with 'data/retour/'
        self.images_names_file_name = self.conf["images_names_file"]["name"]
        # this path will be added before each
        # image name saved in the file
        self.image_path = self.conf["images_names_file"]["image_path"]

        # create a file with names of all images
        images_names_file = open(self.dir_path + self.images_names_file_name, "w")

        # set file paths
        string = ""
        file_paths = self.set_file_paths()
        for file_path in file_paths:
            image_name = os.path.splitext(os.path.basename(file_path))[0]
            # check if txt file with the same name is available
            if os.path.isfile(self.conf["exporter"]["dir"] + image_name + '.txt'):
                # add image name to the string and then to the created txt file
                string += "{}{}.{}\n".format(self.image_path, image_name, self.conf["data"]["ext"])

        # write the string in file without the last new line
        images_names_file.write(string[:-1])

        # close the file with names of all images
        images_names_file.close()

    def set_file_paths(self):

        # set data path for all files with the given extension
        self.data_path = self.conf["exporter"]["dir"] + '*' + self.conf["data"]["ext"]
        file_paths = glob.glob(self.data_path)
        # check if any files are found
        if not file_paths:
            sys.exit("No files found, check the path")
        return file_paths


if __name__ == '__main__':
    main = TrainingFileExporter()
    main.run()
