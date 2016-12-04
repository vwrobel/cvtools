import importlib

import cv2
from ..common_functions import get_vid_details
from tqdm import tqdm
from copy import copy


class SelectionWindow:
    def __init__(self, x=0, y=0, w=0, h=0, t=0, color=(0, 0, 0), type='manual', name=''):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        self.color = color
        self.type = type
        self.name = name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def scale(self, width, height, invert=False):
        if invert:
            width_factor = 1 / width
            height_factor = 1 / height
            f = lambda x: x
        else:
            width_factor = width
            height_factor = height
            f = lambda x: int(x)
        s = copy(self)
        s.x = f(s.x * width_factor)
        s.y = f(s.y * height_factor)
        s.w = f(s.w * width_factor)
        s.h = f(s.h * height_factor)
        return s


class CompProcess:
    def __init__(self, name, type, process_name_list, param_list):
        self.type = type
        self.name = name
        self.process_name_list = process_name_list
        self.param_list = param_list

    def get_processes_from_names(self):
        processes_list = [importlib.import_module('...processes.' + self.type + '.' + process_name, __name__)
                          for process_name in self.process_name_list]
        return processes_list


class CompFilter(CompProcess):
    def __init__(self, name, process_name_list, param_list):
        CompProcess.__init__(self, name, 'video filter', process_name_list, param_list)

    def run(self, cap, writer):
        process_filters = self.get_processes_from_names()
        (nbf, fps, width, height) = get_vid_details(cap)
        init_res = [process_filter.init(cap, self.param_list[ind])
                    for ind, process_filter in enumerate(process_filters)]
        init_input_list = [init_input for init_input, _ in init_res]
        step_input_list = [step_input for _, step_input in init_res]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, frame = cap.retrieve()
        for i in tqdm(range(nbf)):
            for ind, process_filter in enumerate(process_filters):
                param = self.param_list[ind]
                frame, step_input_list[ind] = process_filter.step(i, frame, param, init_input_list[ind],
                                                                  step_input_list[ind])
            filtered_frame = frame
            _, frame = cap.read()
            writer.write(filtered_frame)
        return


class CompTracker(CompProcess):
    def __init__(self, name, process_name_list, param_list, selection_list):
        CompProcess.__init__(self, name, 'tracker', process_name_list, param_list)
        self.selection_list = selection_list

    def run(self, cap, writer):
        process_trackers = self.get_processes_from_names()
        (nbf, fps, width, height) = get_vid_details(cap)
        scaled_selection_list = [selection.scale(width, height) for selection in self.selection_list]
        init_res = [process_tracker.init(cap, self.param_list[ind], scaled_selection_list[ind])
                    for ind, process_tracker in enumerate(process_trackers)]
        init_input_list = [init_input for init_input, _ in init_res]
        step_input_list = [step_input for _, step_input in init_res]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        computed_selection_list = [[]] * len(self.selection_list)
        _, frame = cap.retrieve()
        for i in tqdm(range(nbf)):
            tracked_frame = frame
            for ind, process_tracker in enumerate(process_trackers):
                param = self.param_list[ind]
                tracked_frame, step_input_list[ind] = process_tracker.step(i, frame, tracked_frame, param,
                                                                           init_input_list[ind], step_input_list[ind])

            computed_selection_list[ind].append(
                step_input_list[ind]['computed_selection'].scale(width, height, invert=True)
            )
            _, frame = cap.read()
            writer.write(tracked_frame)
        return computed_selection_list
