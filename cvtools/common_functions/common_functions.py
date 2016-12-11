import os.path

import cv2
from ffmpy import FFmpeg


def get_vid_details(cap):
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return frame_count, fps, frame_width, frame_height


def get_writer(cap, processed_vid_filepath):
    if not os.path.exists(os.path.dirname(processed_vid_filepath)):
        os.makedirs(os.path.dirname(processed_vid_filepath))
    (nbf, fps, width, height) = get_vid_details(cap)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')

    writer = cv2.VideoWriter(processed_vid_filepath, fourcc, fps,
                             (width, height), True)
    return writer

