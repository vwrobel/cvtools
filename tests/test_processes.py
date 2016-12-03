#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scopethis_cvtools
----------------------------------

Tests for `scopethis_cvtools` module.
"""

import os.path
import os.path
from distutils import dir_util

import pytest
from ..cvtools.main import apply_comp_process_to_video
from ..cvtools.objects import SelectionWindow, CompFilter, CompTracker


@pytest.fixture
def vid_dir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir = os.path.join(os.path.dirname(filename), 'test_files')

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


filter_color_select = ('filter_color_select', {
    'name': 'filter_color_select',
    'process_name_list': ['color_select'],
    'param_list': [{'lower': [17, 15, 100], 'upper': [50, 56, 200]}]
})
filter_mhi = ('filter_mhi', {
    'name': 'filter_mhi',
    'process_name_list': ['mhi'],
    'param_list': [{'sigma_blur': 9, 'threshold': 5, 'kernel_size': 5, 'tau': 200}]
})
filter_optical_flow = ('filter_optical_flow', {
    'name': 'filter_optical_flow',
    'process_name_list': ['optical_flow'],
    'param_list': [{'pyr_scale': 0.5, 'levels': 3, 'win_size': 15, 'iterations': 3, 'poly_n': 5, 'poly_sigma': 1.1}]
})
filter_with_frame_number = ('filter_with_frame_number', {
    'name': 'filter_with_frame_number',
    'process_name_list': ['with_frame_number'],
    'param_list': [{'number_color': (0, 0, 0)}]
})


class TestFilters:
    scenarios = [
        filter_color_select,
        filter_mhi,
        filter_optical_flow,
        filter_with_frame_number
    ]

    def test_apply_comp_filter_to_video(self, vid_dir, name, process_name_list, param_list):
        """Test apply_comp_process_to_video for all filters
        """
        comp_filter = CompFilter(name, process_name_list, param_list)
        test_vid_path = str(vid_dir.join('test_vid.mp4'))
        filtered_test_vid_path = str(vid_dir.join(name + '_test_vid.avi'))
        apply_comp_process_to_video(test_vid_path, filtered_test_vid_path, comp_filter)


selection1 = SelectionWindow(0.1, 0.2, 0.3, 0.4, 0, (100, 100, 0), 'manual', 'selection1')
selection2 = SelectionWindow(0.4, 0.3, 0.2, 0.1, 0, (0, 100, 0), 'manual', 'selection2')
selection_list = [selection1, selection2]

tracker_meanshift = ('tracker_meanshift', {
    'name': 'tracker_meanshift',
    'process_name_list': ['meanshift'] * len(selection_list),
    'param_list': [{
        'lower_color_bound': [0.0, 0.0, 0.0],
        'upper_color_bound': [255.0, 255.0, 255.0],
        'color_channel': [2]
    }] * len(selection_list),
    'selection_list': selection_list
})

tracker_camshift = ('tracker_camshift', {
    'name': 'tracker_camshift',
    'process_name_list': ['camshift'] * len(selection_list),
    'param_list': [{
        'lower_color_bound': [0.0, 0.0, 0.0],
        'upper_color_bound': [255.0, 255.0, 255.0],
        'color_channel': [2]
    }] * len(selection_list),
    'selection_list': selection_list
})


class TestTrackers:
    scenarios = [
        tracker_meanshift,
        tracker_camshift
    ]

    def test_apply_comp_tracker_to_video(self, vid_dir, name, process_name_list, param_list, selection_list):
        """Test apply_comp_process_to_video for all trackers
        """
        comp_tracker = CompTracker(name, process_name_list, param_list, selection_list)
        test_vid_path = str(vid_dir.join('test_vid.mp4'))
        tracked_test_vid_path = str(vid_dir.join(name + '_test_vid.avi'))
        computed_selection_list = apply_comp_process_to_video(test_vid_path, tracked_test_vid_path, comp_tracker)
        assert len(computed_selection_list) > 0
