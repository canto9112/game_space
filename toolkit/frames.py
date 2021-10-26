import os


def get_frames(frame_directory):
    frames = []
    for file in os.listdir(f"frames/{frame_directory}"):
        with open(f"frames/{frame_directory}/{file}") as f:
            frames.append(f.read())
    return frames


def get_garbage_frame(garbage):
    with open(f'frames/garbage/{garbage}', "r") as garbage_file:
        frame = garbage_file.read()
    return frame


def get_game_over_frame(garbage):
    with open(f'frames/game_over/{garbage}', "r") as garbage_file:
        frame = garbage_file.read()
    return frame