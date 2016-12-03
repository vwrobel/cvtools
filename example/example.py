import sys

from ..cvtools import apply_comp_process_to_video, SelectionWindow, CompTracker


def main():
    vid_filepath = './example/vids/aouta/aouta.mp4'
    selection = SelectionWindow(0.72, 0.74, 0.054, 0.19, 0, (100, 100, 0), 'manual', 'aouta')
    selection_list = [selection]

    tracker_camshift = CompTracker(
        'tracker_camshift',
        ['camshift'],
        [{'lower_color_bound': [0.0, 0.0, 0.0],
          'upper_color_bound': [255.0, 255.0, 255.0],
          'color_channel': [2]}],
        selection_list)

    tracked_vid_filepath = vid_filepath.replace('.mp4', '_tracker_camshift.avi')
    apply_comp_process_to_video(vid_filepath, tracked_vid_filepath, tracker_camshift)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
