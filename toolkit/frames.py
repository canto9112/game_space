import os


def get_frames(frame_directory):
    frames = []
    for file in os.listdir(f"frames/{frame_directory}"):
        with open(f"frames/{frame_directory}/{file}") as f:
            frames.append(f.read())
    return frames