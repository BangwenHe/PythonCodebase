import argparse

import cv2
from pathlib import Path
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames_folder", type=str, required=True, help="frames folder")
    parser.add_argument("--output_video_path", type=str, required=True, help="output video path")
    parser.add_argument("--fps", type=int, default=30, help="video fps")
    parser.add_argument("--width", type=int, default=-1, help="video width")
    parser.add_argument("--height", type=int, default=-1, help="video height")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    frames_folder = Path(args.frames_folder)

    output_video_path = args.output_video_path
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    fps = args.fps
    width = args.width
    height = args.height

    image = cv2.imread(str(frames_folder / next(frames_folder.iterdir())))
    if width == -1:
        width = image.shape[1]
    if height == -1:
        height = image.shape[0]

    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), True)

    img_list = sorted(frames_folder.iterdir(), key=lambda x: int(x.name.split("_")[1].split(".")[0]))
    for img_path in tqdm(img_list):
        img = cv2.imread(str(img_path))
        if img.shape[0] != height or img.shape[1] != width:
            img = cv2.resize(img, (width, height))

        video_writer.write(img)
    
    video_writer.release()


if __name__ == "__main__":
    main()
