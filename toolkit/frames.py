import os


def get_frames(frame_directory):
    frames = []
    for file in os.listdir(frame_directory):
        with open(f"{frame_directory}/{file}") as f:
            frames.append(f.read())
    return frames


def get_frame(folder, filename):
    with open(f'{folder}/{filename}', "r") as file:
        frame = file.read()
    return frame
