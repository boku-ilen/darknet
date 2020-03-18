import os
import cv2
import numpy as np


class BBoxDrawer:

    def __init__(self, conf):
        self.ext = conf["data"]["ext"]
        self.dir_path = conf["data"]["dir"]

        self.centroid_x = None
        self.centroid_y = None
        self.width = None
        self.height = None

        self.image_width = None
        self.image_height = None

    def draw_bboxes(self, file_path):

        # save filename for naming txt file later
        filename = os.path.splitext(os.path.basename(file_path))[0]

        image = cv2.imread(self.dir_path + filename + '.' + self.ext)
        print(self.dir_path + filename + '.' + self.ext)
        self.image_height = image.shape[0]
        self.image_width = image.shape[1]

        # open the txt file
        text_file = open(file_path, "r")
        lines = text_file.readlines()
        for line in lines:
            line_elements = line.split(' ')
            if line != "\n":
                self.centroid_x = float(line_elements[1])
                self.centroid_y = float(line_elements[2])
                self.width = float(line_elements[3])
                self.height = float(line_elements[4])

            x_center = int(self.centroid_x * self.image_width)
            y_center = int(self.centroid_y * self.image_height)
            w = int(self.width * self.image_width)
            h = int(self.height * self.image_height)

            x_left = x_center - int(w/2)
            y_top = y_center - int(h/2)
            cv2.rectangle(image, (x_left, y_top), (x_left + w, y_top + h), (0, 0, 255), 2)

        # concatenate labelled images and rosa
        rosa_dir = self.dir_path.replace('to_train', 'to_extract')
        new_filename = '2-' + filename[2:]
        image_rosa = cv2.imread(rosa_dir + new_filename + '.' + self.ext)
        concat_output_image = np.concatenate((image, image_rosa), axis=1)

        # save images with bounding box
        labelled_dir = self.dir_path.replace('to_train', 'labelled_concat')
        if not os.path.exists(labelled_dir):
            print('make a dir {}'.format(labelled_dir))
            os.makedirs(labelled_dir)
        labeled_name = filename + '.' + self.ext
        path = labelled_dir + labeled_name
        cv2.imwrite(path, concat_output_image)
