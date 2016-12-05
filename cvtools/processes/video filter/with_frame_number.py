import cv2

PARAM_DEFAULT = {
}


def init(cap, param):
    init_input = None
    step_input = None
    return init_input, step_input


def step(i, frame, param, init_input, step_input):
    number_color = param['number_color']
    filtered_frame = cv2.putText(frame, str(i), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, number_color)
    step_input = None
    return filtered_frame, step_input
