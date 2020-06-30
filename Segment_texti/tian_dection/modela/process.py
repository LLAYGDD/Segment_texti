from __future__ import print_function



import os
import numpy as np

import cv2
import os.path
from skimage.io import imsave, imread

data_path = 'D:/DeepLearning/Semantic-segmentation-of-remote-sensing-images-master/tian_dection/fagnzhi_data/'
save_path='D:/DeepLearning/Semantic-segmentation-of-remote-sensing-images-master/tian_dection/fagnzhi_data/preds'

img_train_path = os.path.join(save_path, 'imgs_train.npy')
img_train_mask_path = os.path.join(save_path, 'imgs_mask_train.npy')


image_rows = 256
image_cols = 256
mask_name='_mask.bmp'


def load_train_data():
    print ('Loading train data from %s and %s' % (img_train_path, img_train_mask_path))
    imgs_train = np.load(img_train_path)
    imgs_mask_train = np.load(img_train_mask_path)
    return imgs_train, imgs_mask_train


def create_train_data():
    train_data_path = os.path.join(data_path, 'train/image')
    train_data_Label_path = os.path.join(data_path, 'train/labels')
    images = os.listdir(train_data_path)
    total = len(images)
    print(total)

    imgs=np.ndarray((total,image_rows,image_cols),dtype=np.uint8)
    imgs_mask=np.ndarray((total,image_rows,image_cols),dtype=np.uint8)
    i = 0

    print('Creating training images...')
    img_patients=np.ndarray((total,),dtype=np.uint8)

    for image_name in images:

        if 'mask' in image_name:
            continue

        imgs_mask_name=image_name.split('.')[0]+mask_name
        patient_num = image_name.split('_')[0]
        print(patient_num)
        img =cv2.imread(os.path.join(train_data_path, image_name),cv2.IMREAD_GRAYSCALE)
        img_mask = cv2.imread(os.path.join(train_data_Label_path, imgs_mask_name),cv2.IMREAD_GRAYSCALE)
        img = np.array([img])
        img_mask = np.array([img_mask])
        # print(imgs_mask)

        imgs[i] = img
        # print(imgs[i])
        imgs_mask[i] = img_mask


        if i % 100 == 0:
            print('Done: {0}/{1} images'.format(i, total))
        i += 1
    print('Loading done.')

    np.save(img_train_path, imgs)
    np.save(img_train_mask_path, imgs_mask)
    print('Training Saving to .npy files done.')



if __name__=='__main__':
    create_train_data()




