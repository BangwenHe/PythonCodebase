import argparse
from typing import Union
import os
import json
import glob

from PIL import Image, ImageDraw
import numpy as np
import torch
from torchvision.models.detection.faster_rcnn import fasterrcnn_resnet50_fpn
from torchvision.transforms import transforms as T
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(description='Detection')
    parser.add_argument('--images_dir', type=str, required=True, help='images directory')
    parser.add_argument('--bbox_thres', type=float, default=0.5, help='bbox threshold, default: 0.5')
    parser.add_argument('--output_dir', type=str, default='output', help='output directory, default: output')
    parser.add_argument('--regex_pattern', type=str, default='**/*.jpg', 
        help='regex pattern for extracting images, final pattern will be "{images_dir}/{regex_pattern}", default: **/*.jpg')
    return parser.parse_args()


def postprocess(pred):
    assert len(pred) == 1

    bboxes = pred[0]['boxes'].detach().cpu().numpy()
    scores = pred[0]['scores'].detach().cpu().numpy()
    labels = pred[0]['labels'].detach().cpu().numpy()

    return bboxes, scores, labels


def get_color_map_list(num_classes, custom_color=None):
    """
    Returns the color map for visualizing the segmentation mask,
    which can support arbitrary number of classes.
    Args:
        num_classes (int): Number of classes.
        custom_color (list, optional): Save images with a custom color map. Default: None, use paddleseg's default color map.
    Returns:
        (list). The color map.
    """

    num_classes += 1
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = color_map[3:]

    if custom_color:
        color_map[:len(custom_color)] = custom_color
    return color_map


def visualize(image, bboxes, scores=None, labels=None, colormap=None, labelmap=None):
    n_bboxes = len(bboxes)
    if n_bboxes == 0:
        return
    
    if scores is None:
        scores = np.ones(n_bboxes)
    
    if labels is None:
        labels = np.arange(n_bboxes)
    
    if colormap is None:
        colormap = get_color_map_list(labels.max())
    
    if labelmap is None:
        labelmap_file = os.path.join(os.path.dirname(__file__), 'labels.txt')

        if os.path.exists(labelmap_file):
            with open(labelmap_file, 'r') as f:
                labelmap = f.readlines()
            labelmap = [x.strip() for x in labelmap]
        else:
            labelmap = [str(i.item()) for i in labels]
    
    for i in range(n_bboxes):
        bbox = bboxes[i]
        score = scores[i]
        label = labels[i]
        color = colormap[label]
        
        # use PIL to visualize
        draw = ImageDraw.Draw(image)
        draw.rectangle(bbox, outline=color)
        draw.text(bbox[:2], '{:.2f} {}'.format(score, labelmap[label]), fill=color)
        
        image.save('result.jpg')


def main():
    args = parse_args()
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()
    images_dir = args.images_dir
    bbox_thres = args.bbox_thres
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    pattern = os.path.join(images_dir, args.regex_pattern)
    images_path = glob.glob(pattern)
    transform = T.Compose([T.ToTensor()])

    video_names = os.listdir(images_dir)
    result = {video_name: {} for video_name in video_names}

    cuda = torch.cuda.is_available()
    if cuda:
        model.cuda()

    for image_path in tqdm(images_path):
        image = Image.open(image_path)
        
        inp = transform(image)
        inp = torch.unsqueeze(inp, 0)
        if cuda:
            inp = inp.cuda()

        pred = model(inp)

        # visualize(image, *postprocess(pred))
        video_name = os.path.normpath(image_path).split(os.sep)[1]
        bboxes, scores, labels = postprocess(pred)

        idx = np.where(scores > bbox_thres)
        bboxes = bboxes[idx]
        scores = scores[idx]
        labels = labels[idx]
        result[video_name][image_path] = {'bboxes': bboxes.tolist(), 'scores': scores.tolist(), 'labels': labels.tolist()}

    for key in result:
        res = {i:result[key][i] for i in sorted(result[key])}
        if len(res) == 0:
            continue

        with open(os.path.join(output_dir, key + '.json'), 'w') as f:
            json.dump(res, f, indent=4)


if __name__ == "__main__":
    main()
