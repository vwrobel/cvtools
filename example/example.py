from cvtools import process_vid, SelectionWindow, CompTracker, CompFilter


def example():
    # The path of the video you want to work on
    vid_filepath = './example/vids/aouta/aouta.mp4'

    # The filter you want to apply
    filter_color_select = CompFilter(
        'filter_color_select',
        ['color_select'],
        [{'lower': [17, 15, 100], 'upper': [50, 56, 200]}])

    filtered_vid_filepath = vid_filepath.replace('.mp4', '_filter_color_select.mp4')

    process_vid(vid_filepath, filtered_vid_filepath, filter_color_select)

    # The object you want to track (x, y , w, h are ratios between position and frame dimension)
    selection = SelectionWindow(0.72, 0.74, 0.054, 0.19, 0, (100, 100, 0), 'manual', 'aouta')
    selection_list = [selection]

    # The tracker you want to apply
    tracker_camshift = CompTracker(
        'tracker_camshift',
        ['camshift'],
        [{'lower_color_bound': [0.0, 0.0, 0.0],
          'upper_color_bound': [255.0, 255.0, 255.0],
          'color_channel': [2],
          'channel_range': [40.0, 120.0],
          'bin_nb': [180]
          }],
        selection_list)

    # The path of the tracked video
    tracked_vid_filepath = vid_filepath.replace('.mp4', '_tracker_camshift.mp4')

    process_vid(filtered_vid_filepath, tracked_vid_filepath, tracker_camshift)


if __name__ == '__main__':
    example()
