from __future__ import print_function

import os
import numpy as np

import cv2
import os.path
from skimage.io import imsave, imread

data_path = 'D:/DeepLearning/Semantic-segmentation-of-remote-sensing-images-master/tian_dection/fagnzhi_data/'
save_path='D:/DeepLearning/Semantic-segmentation-of-remote-sensing-images-master/tian_dection/fagnzhi_data/preds'


img_test_path = os.path.join(save_path, 'imgs_test.npy')
img_test_id_path = os.path.join(save_path, 'imgs_id_test.npy')


image_rows = 256
image_cols = 256

def load_test_data():
    print ('Loading test data from %s' % img_test_path)
    imgs_test = np.load(img_test_path)
    return imgs_test

def load_test_ids():
    print ('Loading test ids from %s' % img_test_id_path)
    imgs_id = np.load(img_test_id_path)
    return imgs_id


def create_test_data():

    test_data_path = os.path.join(data_path, 'test/image')

    images_test = os.listdir(test_data_path)
    total_test = len(images_test)

    imgs_test = np.ndarray((total_test, 1, image_rows, image_cols), dtype=np.uint8)
    imgs_id = np.ndarray((total_test, ), dtype=np.int32)

    j=0
    print('Creating test images...')
    for image_name_test in images_test:

        img_id = int(image_name_test.split('.')[0])
        img_test = cv2.imread(os.path.join(test_data_path, image_name_test), cv2.IMREAD_GRAYSCALE)

        imgs_test[j] = img_test
        imgs_id[j] = img_id

        if j % 100 == 0:
            print('Test Done: {0}/{1} images'.format(j, total_test))
        j += 1
    print('Loading done.')

    np.save(img_test_path, imgs_test)
    np.save(img_test_id_path, imgs_id)
    print('Testing Saving to .npy files done.')


if __name__=='__main__':
    create_test_data()