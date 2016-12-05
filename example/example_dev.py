import sys

from cvtools import apply_comp_process_to_video, SelectionWindow, CompTracker, CompFilter


def example():
    # The path of the video you want to work on
    vid_filepath = './example/vids/aouta/aouta.mp4'


    # The object you want to track (x, y , w, h are ratios between position and frame dimension)
    selection = SelectionWindow(0.56, 0.66, 0.085, 0.18, 5, (100, 100, 0), 'manual', 'aouta')
    selection_list = [selection]

    # The tracker you want to apply
    tracker_camshift = CompTracker(
        'tracker_camshift',
        ['camshift'],
        [{'lower_color_bound': [0.0, 0.0, 0.0],
          'upper_color_bound': [255.0, 255.0, 255.0],
          'color_channel': [2]}],
        selection_list)

    # The path of the tracked video
    tracked_vid_filepath = vid_filepath.replace('.mp4', '_tracker_camshift.avi')

    apply_comp_process_to_video(vid_filepath, tracked_vid_filepath, tracker_camshift)


if __name__ == '__main__':
    example()