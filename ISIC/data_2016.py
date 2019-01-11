import random
import csv
import os
import os.path
from PIL import Image
import glob
import numpy as np
import torch
import torch.utils.data as udata

def preprocess_data(root_dir):
    print('pre-processing data ...\n')
    # training data
    benign    = glob.glob(os.path.join(root_dir, 'Train', 'benign', '*.jpg')); benign.sort()
    malignant = glob.glob(os.path.join(root_dir, 'Train', 'malignant', '*.jpg')); malignant.sort()
    benign_seg    = glob.glob(os.path.join(root_dir, 'Train_Lesion', 'benign', '*.png')); benign_seg.sort()
    malignant_seg = glob.glob(os.path.join(root_dir, 'Train_Lesion', 'malignant', '*.png')); malignant_seg.sort()
    with open('train.csv', 'wt', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for k in range(len(benign)):
            filename = benign[k]
            filename_seg = benign_seg[k]
            writer.writerow([filename] + [filename_seg] + ['0'])
        for k in range(len(malignant)):
            filename = malignant[k]
            filename_seg = malignant_seg[k]
            writer.writerow([filename] + [filename_seg] + ['1'])
    # training data oversample
    benign    = glob.glob(os.path.join(root_dir, 'Train', 'benign', '*.jpg')); benign.sort()
    malignant = glob.glob(os.path.join(root_dir, 'Train', 'malignant', '*.jpg')); malignant.sort()
    benign_seg    = glob.glob(os.path.join(root_dir, 'Train_Lesion', 'benign', '*.png')); benign_seg.sort()
    malignant_seg = glob.glob(os.path.join(root_dir, 'Train_Lesion', 'malignant', '*.png')); malignant_seg.sort()
    with open('train_oversample.csv', 'wt', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for k in range(len(benign)):
            filename = benign[k]
            filename_seg = benign_seg[k]
            writer.writerow([filename] + [filename_seg] + ['0'])
        for i in range(4):
            for k in range(len(malignant)):
                filename = malignant[k]
                filename_seg = malignant_seg[k]
                writer.writerow([filename] + [filename_seg] + ['1'])
    # val data
    benign    = glob.glob(os.path.join(root_dir, 'Val', 'benign', '*.jpg')); benign.sort()
    malignant = glob.glob(os.path.join(root_dir, 'Val', 'malignant', '*.jpg')); malignant.sort()
    benign_seg    = glob.glob(os.path.join(root_dir, 'Val_Lesion', 'benign', '*.png')); benign_seg.sort()
    malignant_seg = glob.glob(os.path.join(root_dir, 'Val_Lesion', 'malignant', '*.png')); malignant_seg.sort()
    with open('val.csv', 'wt', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for k in range(len(benign)):
            filename = benign[k]
            filename_seg = benign_seg[k]
            writer.writerow([filename] + [filename_seg] + ['0'])
        for k in range(len(malignant)):
            filename = malignant[k]
            filename_seg = malignant_seg[k]
            writer.writerow([filename] + [filename_seg] + ['1'])
    # test data
    benign    = glob.glob(os.path.join(root_dir, 'Test', 'benign', '*.jpg')); benign.sort()
    malignant = glob.glob(os.path.join(root_dir, 'Test', 'malignant', '*.jpg')); malignant.sort()
    benign_seg    = glob.glob(os.path.join(root_dir, 'Test_Lesion', 'benign', '*.png')); benign_seg.sort()
    malignant_seg = glob.glob(os.path.join(root_dir, 'Test_Lesion', 'malignant', '*.png')); malignant_seg.sort()
    with open('test.csv', 'wt', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for k in range(len(benign)):
            filename = benign[k]
            filename_seg = benign_seg[k]
            writer.writerow([filename] + [filename_seg] + ['0'])
        for k in range(len(malignant)):
            filename = malignant[k]
            filename_seg = malignant_seg[k]
            writer.writerow([filename] + [filename_seg] + ['1'])

class ISIC(udata.Dataset):
    def __init__(self, csv_file, transform=None):
        file = open(csv_file, newline='')
        reader = csv.reader(file, delimiter=',')
        self.pairs = [row for row in reader]
        self.transform = transform
    def __len__(self):
        return len(self.pairs)
    def  __getitem__(self, idx):
        pair = self.pairs[idx]
        image = Image.open(pair[0])
        image_seg = Image.open(pair[1])
        label = int(pair[2])
        # construct one sample
        sample = {'image': image, 'image_seg': image_seg, 'label': label}
        # transform
        if self.transform:
            sample = self.transform(sample)
        return sample
