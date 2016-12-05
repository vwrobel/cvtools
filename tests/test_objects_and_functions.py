#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_scopethis_cvtools
----------------------------------

Tests for `scopethis_cvtools` module.
"""

import os.path
from distutils import dir_util

import cv2
import pytest
from click.testing import CliRunner
from ..cvtools import cli
from ..cvtools.common_functions import get_vid_details
from ..cvtools.objects import SelectionWindow, CompProcess


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
    Fixture responsible for searching a folder with the name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir = os.path.join(os.path.dirname(filename), 'test_files')

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'scopethis_cvtools.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_SelectionWindow():
    """Test that SelectionWindow can scale and invert scale
    """
    selection1 = SelectionWindow(0.1, 0.2, 0.3, 0.4, 5, (100, 100, 100), 'manual', 'selection1')
    scaled_selection1 = selection1.scale(10, 20)
    assert scaled_selection1.x == 1
    assert scaled_selection1.y == 4
    assert scaled_selection1.w == 3
    assert scaled_selection1.h == 8
    unscaled_selection1 = scaled_selection1.scale(10, 20, invert=True)
    assert round(unscaled_selection1.x, 2) == selection1.x
    assert round(unscaled_selection1.y, 2) == selection1.y
    assert round(unscaled_selection1.w, 2) == selection1.w
    assert round(unscaled_selection1.h, 2) == selection1.h


def test_CompProcess():
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


def test_get_vid_details(vid_dir):
    """Test get_vid_details returns details from cap
    """
    test_vid_path = str(vid_dir.join('test_vid.mp4'))
    cap = cv2.VideoCapture(test_vid_path)
    vid_details = get_vid_details(cap)
    assert vid_details == (8, 29.999999999999996, 758, 426)
