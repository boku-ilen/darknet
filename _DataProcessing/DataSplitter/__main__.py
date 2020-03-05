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
        self.train_dir_path = None

        self.img_ext = None
        self.text_ext = None

    def run(self):

        # load configurations
        with open('config.json') as conf_file:
            self.conf = json.load(conf_file)
        # data directory
        self.dir_path = self.conf["data"]["dir"]
        # future validation data directory
        self.valid_dir_path = self.conf["data"]["valid_dir"]
        # future training data directory
        self.train_dir_path = self.conf["data"]["train_dir"]
        self.img_ext = self.conf["data"]["ext"]
        self.text_ext = self.conf["data"]["text_ext"]

        # set file paths to text files
        file_paths = self.set_file_paths()
        # images without txt file will remain in the original folder
        # shuffle data
        random.shuffle(file_paths)
        # calculate length of the list with file paths
        val_dataset_length = int(0.2 * len(file_paths))

        # move 20% of data to validation data folder
        for file_path in file_paths[:val_dataset_length]:
            txt_file_name = os.path.basename(file_path)
            file_name = os.path.splitext(txt_file_name)[0]
            if file_name != "retour_train":
                os.rename(file_path, self.valid_dir_path + txt_file_name)
                os.rename(self.dir_path + file_name + '.' + self.img_ext,
                          self.valid_dir_path + file_name + '.' + self.img_ext)
        # move 80% of data to training data folder
        for file_path in file_paths[val_dataset_length:]:
            txt_file_name = os.path.basename(file_path)
            file_name = os.path.splitext(txt_file_name)[0]
            if file_name != "retour_train":
                os.rename(file_path, self.train_dir_path + txt_file_name)
                os.rename(self.dir_path + file_name + '.' + self.img_ext,
                          self.train_dir_path + file_name + '.' + self.img_ext)

    def set_file_paths(self):

        # set data path for all files with the given extension
        self.data_path = self.dir_path + '*' + self.text_ext
        file_paths = glob.glob(self.data_path)
        # check if any files are found
        if not file_paths:
            sys.exit("No files found, check the path")
        return file_paths


if __name__ == '__main__':
    main = DataSplitter()
    main.run()
