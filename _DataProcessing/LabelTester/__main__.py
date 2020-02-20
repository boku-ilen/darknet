import glob
import json
import sys
import os

from LabelTester.BboxDrawer import BBoxDrawer


class LabelTester:
    def __init__(self):

        self.conf = None
        self.dir_path = None
        self.bbox_drawer = None

        self.images_names_file_name = None
        self.image_path = None

    def run(self):

        # load configurations
        with open('config.json') as conf_file:
            self.conf = json.load(conf_file)
        # data path
        self.dir_path = self.conf["data"]["dir"]
        ext_text = self.conf["data"]["ext_text"]

        # initialize bbox drawing
        self.bbox_drawer = BBoxDrawer(self.conf)

        # set file paths for text files
        file_paths = self.set_file_paths(ext_text)
        for file_path in file_paths:
            if os.path.splitext(os.path.basename(file_path))[0] != "retour_train":
                # create txt files with the label and bounding boxes for each image
                self.bbox_drawer.draw_bboxes(file_path)

    def set_file_paths(self, ext):

        # set data path for all files with the given extension
        self.dir_path = self.conf["data"]["dir"] + '*' + ext
        file_paths = glob.glob(self.dir_path)
        # check if any files are found
        if not file_paths:
            sys.exit("No files found, check the path")
        return file_paths


if __name__ == '__main__':
    main = LabelTester()
    main.run()
