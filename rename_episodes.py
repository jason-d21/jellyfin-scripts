#!/usr/bin/env python3
# Rename episodes of a season of a TV show compatible with Jellyfin's formats
import os, argparse

# folder_path = ""
# video_ext = ".mkv"
# ep_num_idx = 0 # the index for the episode number in the video name (i.e. where to look for ep number if there are many numbers in the name)
# season_num = "01"

def get_name(filename):
    name, ext = os.path.splitext(filename)
    return name

def get_ext(filename):
    name, ext = os.path.splitext(filename)
    return ext

def get_ep_num(name, ep_num_idx):
    nums =  []
    curr_num = ""
    for c in name:
        if c.isdigit():
            curr_num += c
        elif len(curr_num) > 0:
            nums.append(int(curr_num))
            curr_num = ""
    
    if len(curr_num) > 0:
        nums.append(int(curr_num))
    if len(nums) == 0:
        return -1
    return nums[ep_num_idx]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True, help = "Path of folder with episodes videos to modify")
    parser.add_argument("-e", "--extension", required=True, help = "Extension of videos to modify")
    parser.add_argument("-i", "--index", required=True, type=int, help = "Index for the episode number in the video name (i.e. where to look for ep number if there are many numbers in the name)")
    parser.add_argument("-s", "--season", required=True, type=int, help = "Season number of the TV show")

    return parser.parse_args()

def get_video_names(folder_path, video_ext):
    files = os.listdir(folder_path)
    # get video names with specified video_ext (exclude extension in name) 
    return [get_name(f) for f in files if get_ext(f) == video_ext]

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

if __name__ == "__main__":
    args = parse_args()
    folder_path = args.path
    video_ext = f".{args.extension}"
    ep_num_idx =args.index
    season_num = args.season
    
    video_names = get_video_names(folder_path, video_ext)
    changed_names = []
    for video_name in video_names:
        ep_num = get_ep_num(video_name, ep_num_idx)
        if ep_num >= 0:
            changed_names.append(f"S{season_num:02d}E{ep_num:02d}")
            
    print(f"The following {video_ext} filenames in {folder_path} will be changed:")
    for old, new in zip(video_names, changed_names):
        print(f"{old} --> {new}")
    
    proceed = query_yes_no("Do you want to proceed?")
    if proceed:
        for old, new in zip(video_names, changed_names):
            os.rename(f"{folder_path}/{old}{video_ext}", f"{folder_path}/{new}{video_ext}")
        print("Renaming completed.")
    else:
        print("Renaming cancelled.")
    
