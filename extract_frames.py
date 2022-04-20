"""
multi thread decoding video into image
"""

import argparse
import cv2
import os
from pathlib import Path
from multiprocessing import Process, Queue


def parse_args():
    parser = argparse.ArgumentParser(description="extract frames from videos using multiprocessing")
    parser.add_argument("--src_dir", type=str, help="the directory of the video files")
    parser.add_argument("--dst_dir", type=str, help="the directory of the extracted frames")
    parser.add_argument("--num_process", type=int, default=4, help="the number of processes")
    parser.add_argument("--num_frames", type=int, default=-1, help="the number of frames to extract")
    parser.add_argument("--pattern", type=str, default="*.mp4", help="the pattern of the video files in glob format")
    return parser.parse_args()


def extract_frames(path: Path, dst_dir: Path, num_frames: int):
    video_cap = cv2.VideoCapture(str(path))
    video_dst_dir = dst_dir / path.name.split(".")[0]
    video_dst_dir.mkdir(parents=True, exist_ok=True)

    if num_frames < 0:
        num_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_frames = min(num_frames, int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT)))

    for i in range(num_frames):
        ret, image = video_cap.read()
        if not ret:
            print(f"{path} proccessed.")
            break

        cv2.imwrite(str(video_dst_dir / f"frame_{i:06d}.jpg"), image)


def multi_process(queue: Queue, dst_dir: Path, num_frames: int):
    while not queue.empty():
        path = queue.get()
        extract_frames(path, dst_dir, num_frames)


args = parse_args()

src_dir = args.src_dir
dst_dir = args.dst_dir
num_process = args.num_process
pattern = args.pattern
num_frames = args.num_frames

assert src_dir.exists(), f"{src_dir} does not exist"
dst_dir.mkdir(parents=True, exist_ok=True)
src_dir = Path(src_dir)
dst_dir = Path(dst_dir)

queue = Queue()
for video_path in src_dir.glob(pattern):
    queue.put(video_path)

processes = []
for i in range(num_process):
    p = Process(target=multi_process, args=(queue, dst_dir, num_frames))
    p.start()
    processes.append(p)

for p in processes:
    p.join()
