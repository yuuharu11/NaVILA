import multiprocessing.dummy as mp
import os
import re
import subprocess
from os import listdir, makedirs


def extract_frames(videopath, dest, fps=1):

    try:
        makedirs(dest)
        print("creating " + dest + " subdirectory")
    except:
        print(dest + " subdirectory already exists")

    output = subprocess.call(
        [
            "ffmpeg",
            "-i",
            videopath,
            "-vf",
            "fps=" + str(fps),
            dest + "/%04d.jpg",
        ]
    )
    if output:
        print("Failed to extract frames")


def extract_all_frames():
    try:
        makedirs("/work/NaVILA-Dataset/Human/raw_frames", exist_ok=True)
        print("creating frames subdirectory")
    except:
        print("frames subdirectory already exists")
    videos = listdir("/work/NaVILA-Dataset/Human/videos")

    def eaf(vid):
        vid_id = re.match("(.*).mp4", vid)[1]
        subdir = "/work/NaVILA-Dataset/Human/raw_frames/" + vid_id
        try:
            makedirs(subdir)
            extract_frames("/work/NaVILA-Dataset/Human/videos/" + vid, subdir, fps=1)
        except FileExistsError:
            print(f"skipping {vid}")

    vids = [vid for vid in videos]
    p = mp.Pool(processes=8)
    p.map(eaf, vids)
    p.close()
    p.join()


def remove_empty_dirs(root_dir):
    # Remove empty directories bottom-up so partially extracted videos can be retried cleanly.
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                print(f"removed empty directory: {dirpath}")
            except OSError:
                pass


if __name__ == "__main__":
    extract_all_frames()
    remove_empty_dirs("/work/NaVILA-Dataset/Human/raw_frames")