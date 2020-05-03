import cv2
import glob
import sys
import os
import numpy as np
from collections import Counter
import pandas as pd

# adapt local project path
LOCAL_PATH = ''
IMAGES_PATH = LOCAL_PATH + 'Results/Screenshots/'
# skip some images at the beginning if needed
SKIP_IMAGES = 0#715
# images can have different sizes,
# but we want to compare only parts of them
# (VR view in the lower right corner)
# which has always the same size (630x430) and are positioned
# 20 pixels from the bottom and 20 pixels from the right side
D = 20
H = 430
W = 630


# create a list with paths to all images
def set_file_paths(path, ext):

    # set data path for all files with the given extension
    data_path = path + ext.replace('.', '*')
    file_paths = glob.glob(data_path)
    # check if any files are found
    if not file_paths:
        sys.exit('no files found, check the path: {}'.format(data_path))
    return file_paths


# count significantly different pixels between two images parts
def compute_diff(img_first, img_second):
    # compute absolute difference
    difference = cv2.absdiff(img_first, img_second)

    # set a threshold to show
    # only significant differences
    # e.g. ignore clouds movement
    th = 100
    imask = difference > th

    # compute a mask for significant differences
    canvas = np.zeros_like(img_second, np.uint8)

    canvas[imask] = True

    # count significantly different pixels
    diff_pixels = Counter(canvas[imask] != 0)[True]
    print('diff pixels: {}'.format(diff_pixels))

    # uncomment to show differences
    #cv2.imshow("img1", img_first)
    #cv2.imshow("img2", img_second)
    #cv2.imshow("difference", difference)
    #cv2.imshow("canvas", canvas)
    #cv2.waitKey()

    # return number of
    # significantly different pixels
    return diff_pixels


# create a list with paths to all images
print('reading paths...')
file_paths = set_file_paths(IMAGES_PATH, '.png')
file_paths_length = len(file_paths)
print('{} images read'.format(file_paths_length))
# TODO: consider saving a sorted list to a file 
# because it can take some time if there are many images
# sort the list of paths by file modification time
print('sorting paths...')
file_paths.sort(key=lambda x: os.path.getmtime(x))

# create an empty data frame with needed columns
df = pd.DataFrame(columns=['list idx', 'first image', 'second image', 'diff pixels', 'same size'])

# compare each two adjacent images (sorted by modification time)
for idx in range(file_paths_length-1):
    # skip first images without changes
    print(idx)
    if idx < SKIP_IMAGES:
		print('skipping first {} images...'.format(SKIP_IMAGES))
    else:
        first = file_paths[idx]
        second = file_paths[idx+1]
        print('comparing {} and {}'.format(os.path.basename(first), os.path.basename(second)))
        try:
            # read gray images
            img_first = cv2.imread(first, 0)
            img_second = cv2.imread(second, 0)

            y1 = img_first.shape[0]
            x1 = img_first.shape[1]
            y2 = img_second.shape[0]
            x2 = img_second.shape[1]

            # check images sizes
            if img_first.shape == img_second.shape:
                same_size = True
            else:
                same_size = False

            # count significantly different pixels between two images parts
            diff_pixels = compute_diff(img_first[y1-H-D:y1-D, x1-W-D:x1-D], img_second[y2-H-D:y2-D, x2-W-D:x2-D])

            # compute data for the next row
            new_row = {'list idx': idx, 'first image': os.path.basename(first), 'second image': os.path.basename(second),
                       'diff pixels': diff_pixels, 'same size': same_size}

            # add row to the data frame
            df = df.append(new_row, ignore_index=True)
        # catch key interrupt to save csv anyway
        except KeyboardInterrupt:
            print('interrupt!')
            break
        except:
            print('Warning, could not compare {} and {}'.format(os.path.basename(first), os.path.basename(second)))


# save data frame as csv
print('saving to csv...')
df.to_csv('diff_pixels.csv')


