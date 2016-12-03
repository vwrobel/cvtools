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
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = cv2.VideoWriter(processed_vid_filepath, fourcc, fps,
                             (width, height), True)
    return writer


def convert_from_avi(vid_filepath):
    mp4_vid_filepath = vid_filepath.replace('.avi', '.mp4')
    if os.path.exists(mp4_vid_filepath):
        os.remove(mp4_vid_filepath)
    ffmpegpath = '/usr/local/Cellar/ffmpeg/3.1.2/bin/ffmpeg' # TODO: Use an env var
    ff = FFmpeg(
        executable=ffmpegpath,
        inputs={vid_filepath: None},
        outputs={mp4_vid_filepath: None}
    )
    ff.run()
    os.remove(vid_filepath)
