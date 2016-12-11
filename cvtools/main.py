# -*- coding: utf-8 -*-
'''scopethis_cvtools main'''

import os.path
import cv2
from .common_functions import get_writer


def process_vid(vid_filepath, processed_vid_filepath, comp_process):
    vid_name = os.path.splitext(os.path.basename(vid_filepath))[0]
    processed_vid_name = os.path.splitext(os.path.basename(processed_vid_filepath))[0]
    cap = cv2.VideoCapture(vid_filepath)
    writer = get_writer(cap, processed_vid_filepath)

    res = comp_process.run(cap, writer)

    cap.release()
    writer.release()

    print('your video ' + vid_name + ' has been processed: ' + processed_vid_name + ' is ready.')
    return res
