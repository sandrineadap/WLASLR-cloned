########################################################
# to predict on different weights, change:
#   num_classes (line 371)
#   root        (line 375)
#   train_split (line 378)
#   weights     (line 382. depending on number of classes)
#   word_list   (line 198)
########################################################

import math
import os
import argparse

import matplotlib.pyplot as plt

import torch
import torch.nn as nn

from torchvision import transforms
import videotransforms

import numpy as np

import torch.nn.functional as F
from pytorch_i3d import InceptionI3d

# from nslt_dataset_all import NSLT as Dataset
# from datasets.nslt_dataset_all import NSLT as Dataset
from datasets.nslt_dataset_all_pred import NSLT as Dataset # sandrine
import cv2


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
parser = argparse.ArgumentParser()
parser.add_argument('-mode', type=str, help='rgb or flow')
parser.add_argument('-save_model', type=str)
parser.add_argument('-root', type=str)

args = parser.parse_args()

# Sandrine added: (do I need this)
def predict_on_video(video_file_path, output_file_path):
    '''
    This program will perform ASL recognition ona video using the I3D model.
    Args:
    video_file_path:    The path of the video stored in the disk on which the action recognition is to be performed.
    output_file_path:   The path where the output word (possible words predicted) will be stored.
    '''

    # Initialize the VideoCapture object to read from the video file.
    video_reader = cv2.VideoCapture(video_file_path)

    # Get the width and height of the video
    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Declare a list to store video frames to extract
    frames = []

    # initialize a variable to store the predicted sign being performed in the video
    predicted_class_name = ''

    # get the number of frames in the video
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

     # Calculate the interval after which frames will be added to the list.
    # skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH),1)

    # iterate until the video is accessed successfully - taken from load_rgb_frames_from_video
    for offset in range(video_frames_count):
        success, img = video_reader.read()

        # Check if frame is not read properly then break the loop.
        if not success:
            break

        # resize the frame to fixed dimensions
        w, h, c = img.shape
        sc = 224 / w
        img = cv2.resize(img, dsize=(0, 0), fx=sc, fy=sc)

        # normalize the resized frame
        img = (img / 255.) * 2 - 1

        # append the pre-processed frame into the frames list
        frames.append(img)

    # pass the pre-processed frames to the model and get the predicted probabilities
    

def load_rgb_frames_from_video(video_path, start=0, num=-1):
    vidcap = cv2.VideoCapture(video_path)
    # vidcap = cv2.VideoCapture('/home/dxli/Desktop/dm_256.mp4')

    frames = []

    vidcap.set(cv2.CAP_PROP_POS_FRAMES, start)
    if num == -1:
        num = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    for offset in range(num):
        success, img = vidcap.read()

        w, h, c = img.shape
        sc = 224 / w
        img = cv2.resize(img, dsize=(0, 0), fx=sc, fy=sc)

        img = (img / 255.) * 2 - 1

        frames.append(img)

    return torch.Tensor(np.asarray(frames, dtype=np.float32))


def run(init_lr=0.1,
        max_steps=64e3,
        mode='rgb',
        root='/ssd/Charades_v1_rgb',
        train_split='charades/charades.json',
        batch_size=3 * 15,
        save_model='',
        weights=None):
    # setup dataset
    test_transforms = transforms.Compose([videotransforms.CenterCrop(224)])

    # val_dataset = Dataset(train_split, 'test', root, mode, test_transforms)
    # val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=1,
    #                                              shuffle=False, num_workers=2,
    #                                              pin_memory=False)

    # dataloaders = {'test': val_dataloader}
    # datasets = {'test': val_dataset}

    pred_dataset = Dataset(train_split, 'test', root, mode, test_transforms)
    pred_dataloader = torch.utils.data.DataLoader(pred_dataset, batch_size=1,
                                                 shuffle=False, num_workers=2,
                                                 pin_memory=False)

    dataloaders = {'pred': pred_dataloader}
    datasets = {'pred': pred_dataset}

    # setup the model
    if mode == 'flow':
        i3d = InceptionI3d(400, in_channels=2)
        i3d.load_state_dict(torch.load('weights/flow_imagenet.pt'))
    else:
        i3d = InceptionI3d(400, in_channels=3)
        i3d.load_state_dict(torch.load('weights/rgb_imagenet.pt'))
    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  # nslt_2000_000700.pt nslt_1000_010800 nslt_300_005100.pt(best_results)  nslt_300_005500.pt(results_reported) nslt_2000_011400
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()

    correct = 0
    correct_5 = 0
    correct_10 = 0

# sandrine changed  all the np.int to int since apparently it was deprecated/removed
# https://stackoverflow.com/questions/74946845/attributeerror-module-numpy-has-no-attribute-int


    # top1_fp = np.zeros(num_classes, dtype=int)
    # top1_tp = np.zeros(num_classes, dtype=int)

    # top5_fp = np.zeros(num_classes, dtype=int)
    # top5_tp = np.zeros(num_classes, dtype=int)

    # top10_fp = np.zeros(num_classes, dtype=int)
    # top10_tp = np.zeros(num_classes, dtype=int)

    # for data in dataloaders["test"]:
    for data in dataloaders["pred"]:

        # print(type(data)) # sandrine
        # print(data)
        # inputs, labels, video_id = data  # inputs: b, c, t, h, w
        inputs, video_id = data
        # print(type(inputs))
        # print(inputs)

        per_frame_logits = i3d(inputs)

        predictions = torch.max(per_frame_logits, dim=2)[0]
        out_labels = np.argsort(predictions.cpu().detach().numpy()[0])
        # print(out_labels) # sandrine
        # print("hello")
        out_probs = np.sort(predictions.cpu().detach().numpy()[0])
        # print("predictions")
        # print(predictions[0])
        # print("out_probs")
        # print(out_probs[0])

        # print(video_id, torch.argmax(predictions[0]).item()) # sandrine. print what the prediction is

        # display what word the prediction was
        word_list = open("../../wlasl-complete/wlasl_class_list_01.txt") # change here. must refer to the correct word list!!!
        content = word_list.readlines()
        # print(video_id, torch.argmax(predictions[0]).item(), content[torch.argmax(predictions[0]).item()].split("	", 1)[1]) # sandrine. print what the prediction is

        k = 10
        print("Top", k, "predictions:")
        f = open("predictions.txt", "a+")
        f.write("\nTop " + str(k) + " predictions:" + "\n")
        topk_preds = torch.topk(predictions[0], k).indices
        for pred in topk_preds:
            print(video_id, pred.item(), content[pred].split("	", 1)[1]) # get top k predictions
            f.write(str(video_id) + " " + str(pred.item()) + " " + str(content[pred].split("	", 1)[1]))
        f.close()

'''
        if labels[0].item() in out_labels[-5:]:
            correct_5 += 1
            top5_tp[labels[0].item()] += 1
        else:
            top5_fp[labels[0].item()] += 1
        if labels[0].item() in out_labels[-10:]:
            correct_10 += 1
            top10_tp[labels[0].item()] += 1
        else:
            top10_fp[labels[0].item()] += 1
        if torch.argmax(predictions[0]).item() == labels[0].item():
            correct += 1
            top1_tp[labels[0].item()] += 1
        else:
            top1_fp[labels[0].item()] += 1
        print(torch.argmax(predictions[0]).item()) # sandrine. print what the prediction is
        # print(predictions[0][torch.argmax(predictions[0]).item()])
        print(labels[0].item()) # sandrine. print what the label was
        print(video_id, float(correct) / len(dataloaders["test"]), float(correct_5) / len(dataloaders["test"]),
              float(correct_10) / len(dataloaders["test"]))

        # per-class accuracy
    top1_per_class = np.mean(top1_tp / (top1_tp + top1_fp))
    top5_per_class = np.mean(top5_tp / (top5_tp + top5_fp))
    top10_per_class = np.mean(top10_tp / (top10_tp + top10_fp))
    print('top-k average per class acc: {}, {}, {}'.format(top1_per_class, top5_per_class, top10_per_class))
'''

def ensemble(mode, root, train_split, weights, num_classes):
    # setup dataset
    test_transforms = transforms.Compose([videotransforms.CenterCrop(224)])
    # test_transforms = transforms.Compose([])

    val_dataset = Dataset(train_split, 'test', root, mode, test_transforms)
    val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=1,
                                                 shuffle=False, num_workers=2,
                                                 pin_memory=False)

    dataloaders = {'test': val_dataloader}
    datasets = {'test': val_dataset}

    # setup the model
    if mode == 'flow':
        i3d = InceptionI3d(400, in_channels=2)
        i3d.load_state_dict(torch.load('weights/flow_imagenet.pt'))
    else:
        i3d = InceptionI3d(400, in_channels=3)
        i3d.load_state_dict(torch.load('weights/rgb_imagenet.pt'))
    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  # nslt_2000_000700.pt nslt_1000_010800 nslt_300_005100.pt(best_results)  nslt_300_005500.pt(results_reported) nslt_2000_011400
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()

    correct = 0
    correct_5 = 0
    correct_10 = 0
    # confusion_matrix = np.zeros((num_classes,num_classes), dtype=np.int)

    # sandrine is changing all the np.int to int since apparently it was deprecated/removed
    # https://stackoverflow.com/questions/74946845/attributeerror-module-numpy-has-no-attribute-int
    top1_fp = np.zeros(num_classes, dtype=int)
    top1_tp = np.zeros(num_classes, dtype=int)

    top5_fp = np.zeros(num_classes, dtype=int)
    top5_tp = np.zeros(num_classes, dtype=int)

    top10_fp = np.zeros(num_classes, dtype=int)
    top10_tp = np.zeros(num_classes, dtype=int)

    for data in dataloaders["test"]:
        inputs, labels, video_id = data  # inputs: b, c, t, h, w

        t = inputs.size(2)
        num = 64
        if t > num:
            num_segments = math.floor(t / num)

            segments = []
            for k in range(num_segments):
                segments.append(inputs[:, :, k*num: (k+1)*num, :, :])

            segments = torch.cat(segments, dim=0)
            per_frame_logits = i3d(segments)

            predictions = torch.mean(per_frame_logits, dim=2)

            if predictions.shape[0] > 1:
                predictions = torch.mean(predictions, dim=0)

        else:
            per_frame_logits = i3d(inputs)
            predictions = torch.mean(per_frame_logits, dim=2)[0]

        out_labels = np.argsort(predictions.cpu().detach().numpy())

        if labels[0].item() in out_labels[-5:]:
            correct_5 += 1
            top5_tp[labels[0].item()] += 1
        else:
            top5_fp[labels[0].item()] += 1
        if labels[0].item() in out_labels[-10:]:
            correct_10 += 1
            top10_tp[labels[0].item()] += 1
        else:
            top10_fp[labels[0].item()] += 1
        if torch.argmax(predictions).item() == labels[0].item():
            correct += 1
            top1_tp[labels[0].item()] += 1
        else:
            top1_fp[labels[0].item()] += 1
        print(video_id, float(correct) / len(dataloaders["test"]), float(correct_5) / len(dataloaders["test"]),
              float(correct_10) / len(dataloaders["test"]))

    top1_per_class = np.mean(top1_tp / (top1_tp + top1_fp))
    top5_per_class = np.mean(top5_tp / (top5_tp + top5_fp))
    top10_per_class = np.mean(top10_tp / (top10_tp + top10_fp))
    print('top-k average per class acc: {}, {}, {}'.format(top1_per_class, top5_per_class, top10_per_class))


def run_on_tensor(weights, ip_tensor, num_classes):
    i3d = InceptionI3d(400, in_channels=3)
    # i3d.load_state_dict(torch.load('models/rgb_imagenet.pt'))

    i3d.replace_logits(num_classes)
    i3d.load_state_dict(torch.load(weights))  # nslt_2000_000700.pt nslt_1000_010800 nslt_300_005100.pt(best_results)  nslt_300_005500.pt(results_reported) nslt_2000_011400
    i3d.cuda()
    i3d = nn.DataParallel(i3d)
    i3d.eval()

    t = ip_tensor.shape[2]
    ip_tensor.cuda()
    per_frame_logits = i3d(ip_tensor)

    predictions = F.upsample(per_frame_logits, t, mode='linear')

    predictions = predictions.transpose(2, 1)
    out_labels = np.argsort(predictions.cpu().detach().numpy()[0])

    arr = predictions.cpu().detach().numpy()[0,:,0].T

    plt.plot(range(len(arr)), F.softmax(torch.from_numpy(arr), dim=0).numpy())
    plt.show()

    return out_labels


def get_slide_windows(frames, window_size, stride=1):
    indices = torch.arange(0, frames.shape[0])
    window_indices = indices.unfold(0, window_size, stride)

    return frames[window_indices, :, :, :].transpose(1, 2)


if __name__ == '__main__':
    # ================== test i3d on a dataset ==============
    # need to add argparse
    mode = 'rgb'
    num_classes = 10 # change here. originally 2000.
    save_model = './checkpoints/'

    # root = '../../data/WLASL2000' # sandrine. for testing the WLASL2000 dataset
    root = '../../data/one_video_test' # change here. This is the directory of the video(s) to be tested

    # train_split = 'preprocess/nslt_{}.json'.format(num_classes) # sandrine. use this for when the train_split name is just a number
    train_split = 'preprocess/nslt_10_01.json'.format(num_classes) # change here

    # weights = 'archived/asl2000/FINAL_nslt_2000_iters=5104_top1=32.48_top5=57.31_top10=66.31.pt' # for 2000 words
    # weights = 'archived/asl100/FINAL_nslt_100_iters=896_top1=65.89_top5=84.11_top10=89.92.pt' # for 100 words
    weights = 'archived/asl10_01/nslt_10_008800_0.812500.pt' # change here. paste best weights from checkpoints here. 

    run(mode=mode, root=root, save_model=save_model, train_split=train_split, weights=weights)
