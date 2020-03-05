import glob
import sys
import json
import random
import os


class DataSplitter:

    def __init__(self):

        self.conf = None
        self.data_path = None

        self.dir_path = None
        self.valid_dir_path = None

    def run(self):

        # load configurations
        with open('config.json') as conf_file:
            self.conf = json.load(conf_file)
        # data directory path
        self.dir_path = self.conf["data"]["dir"]
        # future validation data directory
        self.valid_dir_path = self.conf["data"]["valid_dir"]

        # set file paths
        file_paths = self.set_file_paths()
        random.shuffle(file_paths)
        val_dataset_length = int(0.2 * len(file_paths))
        for file_path in file_paths[:val_dataset_length]:
            file_name = os.path.basename(file_path)
            os.rename(file_path, self.valid_dir_path + file_name)

    def set_file_paths(self):

        # set data path for all files with the given extension
        self.data_path = self.conf["data"]["dir"] + '*' + self.conf["data"]["ext"]
        file_paths = glob.glob(self.data_path)
        # check if any files are found
        if not file_paths:
            sys.exit("No files found, check the path")
        return file_paths


if __name__ == '__main__':
    main = DataSplitter()
    main.run()
