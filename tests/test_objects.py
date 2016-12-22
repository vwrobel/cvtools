#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scopethis_cvtools
----------------------------------

Tests for `scopethis_cvtools` module.
"""

import os.path
from distutils import dir_util

import pytest
from ..cvtools.objects import SelectionWindow, CompProcess, Vid


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


@pytest.fixture
def vid_dir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the name test_files
    and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir = os.path.join(os.path.dirname(filename), 'test_files')

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_selection_window(vid_dir):
    """Test that SelectionWindow can scale and invert scale
    """
    test_vid_path = str(vid_dir.join('test_vid.mp4'))
    orig_vid = Vid(test_vid_path)
    selection1 = SelectionWindow(0.1, 0.2, 0.3, 0.4, 5, (100, 100, 100), 'manual', 'selection1', ['tag1'])
    scaled_selection1 = selection1.scale(orig_vid.width, orig_vid.height)
    unscaled_selection1 = scaled_selection1.scale(orig_vid.width, orig_vid.height, invert=True)
    assert round(unscaled_selection1.x, 2) == selection1.x
    assert round(unscaled_selection1.y, 2) == selection1.y
    assert round(unscaled_selection1.w, 2) == selection1.w
    assert round(unscaled_selection1.h, 2) == selection1.h


def test_comp_process():
    """Test CompProcess
    """
    name = 'test'
    type = 'video filter'
    process_name_list = ['color_select']
    param_list = [{'lower': [17, 15, 100], 'upper': [50, 56, 200]}]
    comp_process = CompProcess(name, type, process_name_list, param_list)
    comp_process.get_processes_from_names()

    with pytest.raises(Exception) as e_info:
        comp_process_err = CompProcess(name, type + 'err', process_name_list, param_list)
        comp_process_err.get_processes_from_names()

