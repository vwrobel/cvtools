import importlib
import cv2
import numpy as np
from tqdm import tqdm
from copy import copy
import os.path


class Vid:
    def __init__(self, filepath, orig=True):
        self.filepath = filepath
        self.name = os.path.splitext(os.path.basename(filepath))[0]
        self.orig = orig
        self.cap = None
        self.nbf = None
        self.fps = None
        self.width = None
        self.height = None
        if self.orig:
            self.get_cap()

    def get_cap(self):
        self.cap = cv2.VideoCapture(self.filepath)
        self.nbf = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_samples(self, selections, positive=True):
        samples_dir = os.path.join(os.path.dirname(self.filepath), 'samples')
        if positive:
            positive_samples_dir = os.path.join(samples_dir, 'positive')
            if not os.path.exists(positive_samples_dir):
                os.makedirs(positive_samples_dir)
            for i, sel in enumerate(selections):
                roi = sel.get_roi(self)
                roi_path = os.path.join(positive_samples_dir, str(i) + '.png')
                cv2.imwrite(roi_path, roi)


class ProcessedVid(Vid):
    def __init__(self, filepath, orig_vid, process):
        Vid.__init__(self, filepath, orig=False)
        self.orig_vid = orig_vid
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        fourcc = cv2.VideoWriter_fourcc(*'avc1')

        self.writer = cv2.VideoWriter(filepath, fourcc, self.orig_vid.fps,
                                      (self.orig_vid.width, self.orig_vid.height), True)
        self.process = process

    def release(self):
        self.orig_vid.cap.release()
        self.writer.release()


class Processing:
    def __init__(self, orig_filepath, processed_filepath, process):
        self.orig_vid = Vid(orig_filepath)
        self.processed_vid = ProcessedVid(processed_filepath, self.orig_vid, process)

    def run(self):
        res = self.processed_vid.process.run(self.processed_vid)
        self.processed_vid.release()
        print('your video ' + self.orig_vid.name + ' has been processed: ' + self.processed_vid.name + ' is ready.')
        return res


class SelectionWindow:
    def __init__(self, x=0, y=0, w=0, h=0, t=0, color=(0, 0, 0), type='manual', name='', tags=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        self.color = color
        self.type = type
        self.name = name
        self.tags = tags

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

    def get_window(self):
        return self.x, self.y, self.w, self.h

    def get_roi(self, vid_or_frame):
        # the selection has to be scaled before
        if isinstance(vid_or_frame, Vid):
            vid = vid_or_frame
            cap = vid.cap
            cap.set(cv2.CAP_PROP_POS_FRAMES, s.t)
            _, frame = cap.read()
        elif isinstance(vid_or_frame, (np.ndarray, np.generic)):
            frame = vid_or_frame
        else:
            return
        roi = frame[self.y: self.y + self.h, self.x:self.x + self.w, :]
        return roi


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

    def complete_param_list(self):
        processes = self.get_processes_from_names()
        for ind, process in enumerate(processes):
            self.param_list[ind].update(process.PARAM_DEFAULT)


class CompFilter(CompProcess):
    def __init__(self, name, process_name_list, param_list):
        CompProcess.__init__(self, name, 'video filter', process_name_list, param_list)

    def run(self, processed_vid):
        self.complete_param_list()
        process_filters = self.get_processes_from_names()
        cap = processed_vid.orig_vid.cap
        writer = processed_vid.writer
        init_res = [process_filter.init(cap, self.param_list[ind])
                    for ind, process_filter in enumerate(process_filters)]
        init_input_list = [init_input for init_input, _ in init_res]
        step_input_list = [step_input for _, step_input in init_res]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        for i in tqdm(range(processed_vid.orig_vid.nbf)):
            ret, frame = cap.read()
            if not ret:
                break
            for ind, process_filter in enumerate(process_filters):
                param = self.param_list[ind]
                frame, step_input_list[ind] = process_filter.step(i, frame, param, init_input_list[ind],
                                                                  step_input_list[ind])
            filtered_frame = frame
            writer.write(filtered_frame)

        return


class CompTracker(CompProcess):
    def __init__(self, name, process_name_list, param_list, selection_list):
        CompProcess.__init__(self, name, 'tracker', process_name_list, param_list)
        self.selection_list = selection_list

    def run(self, processed_vid):
        self.complete_param_list()
        process_trackers = self.get_processes_from_names()
        orig_vid = processed_vid.orig_vid
        cap = orig_vid.cap
        writer = processed_vid.writer
        linked_selection_list = copy(self.selection_list)
        scaled_selection_list = [selection.scale(orig_vid.width, orig_vid.height) for selection in linked_selection_list]
        init_res = [process_tracker.init(cap, self.param_list[ind], scaled_selection_list[ind])
                    for ind, process_tracker in enumerate(process_trackers)]
        init_input_list = [init_input for init_input, _ in init_res]
        step_input_list = [step_input for _, step_input in init_res]
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        computed_selection_list = [[]] * len(self.selection_list)
        for i in tqdm(range(processed_vid.orig_vid.nbf)):
            ret, frame = cap.read()
            if not ret:
                break
            tracked_frame = frame
            for ind, process_tracker in enumerate(process_trackers):
                param = self.param_list[ind]
                tracked_frame, step_input_list[ind] = process_tracker.step(i, frame, tracked_frame, param,
                                                                           init_input_list[ind], step_input_list[ind])

            if step_input_list[ind]['track_started']:
                computed_selection_list[ind].append(
                    step_input_list[ind]['computed_selection'].scale(orig_vid.width, orig_vid.height, invert=True)
                )
            writer.write(tracked_frame)

        return computed_selection_list
