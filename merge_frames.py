import cv2
from pathlib import Path
from tqdm import tqdm


def main():
    frames_path = "exps/motr_r50_wanderlust/results/20150203_120911_968"
    frames_path = Path(frames_path)

    output_video_path = "exps/motr_r50_wanderlust/result.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (1152, 648), True)

    img_list = sorted(frames_path.iterdir(), key=lambda x: int(x.name.split("_")[1].split(".")[0]))
    for img_path in tqdm(img_list):
        img = cv2.imread(str(img_path))
        video_writer.write(img)
    
    video_writer.release()


if __name__ == "__main__":
    main()