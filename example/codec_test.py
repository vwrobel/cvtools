import cv2


vid_filepath = './example/vids/aouta/aouta.mp4'
convert_filepath = './example/vids/aouta/aouta_convert.mp4'
cap = cv2.VideoCapture(vid_filepath)

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'avc1')

writer = cv2.VideoWriter(convert_filepath, fourcc, fps,
                             (frame_width, frame_height), True)

for i in range(frame_count):
    _, frame = cap.read()
    writer.write(frame)

cap.release()
writer.release()