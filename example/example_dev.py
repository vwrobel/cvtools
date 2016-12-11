import sys

from cvtools import apply_comp_process_to_video, SelectionWindow, CompTracker, CompFilter


def example():
    # The path of the video you want to work on
    #vid_filepath = './example/vids/aouta/aouta.mp4'
    #vid_filepath = './example/vids/planeur/planeur.mp4'
    vid_filepath = './example/vids/quad/quad_filter_mhi.mp4'

    # The object you want to track (x, y , w, h are ratios between position and frame dimension)
    #selection = SelectionWindow(0.56, 0.66, 0.085, 0.18, 5, (100, 100, 0), 'manual', 'aouta')
    #selection = SelectionWindow(0.72, 0.30, 0.05, 0.12, 0, (0, 0, 150), 'manual', 'planeur')
    selection = SelectionWindow(0.25, 0.066, 0.084, 0.13, 27, (129, 64, 255), 'manual', 'quadcopter')
    selection_list = [selection]


    #{'lower_color_bound': [0.0, 0.0, 20.0], 'upper_color_bound': [255.0, 255.0, 7.0], 'color_channel': [0, 2],
    #'channel_range': [0, 180, 0, 255], 'bin_nb': [10, 10]}


    filter_mhi = CompFilter(
        'filter_mhi',
        ['mhi'],
        [{'sigma_blur': 9, 'threshold': 5, 'kernel_size': 5, 'tau': 10}])

    # The path of the filtered video (.avi for OpenCV writer to work)
    filtered_vid_filepath = vid_filepath.replace('.mp4', '_filter_mhi.avi')

    #apply_comp_process_to_video(vid_filepath, filtered_vid_filepath, filter_mhi)

    # The tracker you want to apply
    tracker = CompTracker(
        'tracker_meanshift',
        ['meanshift'],
        [{
            'lower_color_bound': [0.0, 0.0, 254.0],
            'upper_color_bound': [255.0, 1.0, 255.0],
            'color_channel': [2],
            'channel_range': [0, 255],
            'bin_nb': [20]
        }],
        selection_list)

    # The path of the tracked video
    tracked_vid_filepath = vid_filepath.replace('.mp4', '_tracker_meanshift_mhi.avi')

    apply_comp_process_to_video(vid_filepath, tracked_vid_filepath, tracker)


if __name__ == '__main__':
    example()


# 'lower_color_bound': [0.0, 0.0, 20.0],
# 'upper_color_bound': [255.0, 2.0, 70.0],
# 'color_channel': [2],
# 'channel_range': [0, 255],
# 'bin_nb': [20]

# 'lower_color_bound': [0.0, 0.0, 254.0],
# 'upper_color_bound': [255.0, 1.0, 255.0],
# 'color_channel': [2],
# 'channel_range': [0, 255],
# 'bin_nb': [20]

# 'lower_color_bound': [0.0, 0.0, 20.0],
# 'upper_color_bound': [10.0, 255.0, 70.0],
# 'color_channel': [0, 2],
# 'channel_range': [0, 180, 0, 255],
# 'bin_nb': [10, 20]