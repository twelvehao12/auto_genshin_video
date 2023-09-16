from moviepy.editor import VideoFileClip
from os.path import realpath, exists
from os import makedirs
from sys import argv
import numpy as np
import cv2

temp_video_path = realpath(r"./temp/Start_temp.mp4")


def get_video_path():
    '''
    处理命令行参数
    '''
    l = len(argv)
    if l == 2:
        return (realpath(argv[1]), realpath(r"./output/output.mp4"))
    elif l == 3:
        return (realpath(argv[1]), realpath(argv[2]+r"/output.mp4"))
    return (realpath(r"./demo/测试视频1.mp4"), realpath(r"./output/output.mp4"))


def set_startvideo_attr(source_video: VideoFileClip):
    '''
    调整视频的分辨率和帧率
    '''
    temp_path = realpath('./temp')
    if not exists(temp_path):
        makedirs(temp_path)

    videoCapture = cv2.VideoCapture('./source/Start.mp4')

    fps = source_video.fps
    size = source_video.size

    videoWriter = cv2.VideoWriter(
        temp_video_path,
        cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),
        fps,
        size
    )

    while True:
        success, frame = videoCapture.read()
        if success:
            img = cv2.resize(frame, size)
            videoWriter.write(img)
        else:
            break
    videoWriter.release()


def get_start_time(source_video_path: str, fps: int):
    '''
    获取白色像素占比大于80%的时刻
    '''
    videoCapture = cv2.VideoCapture(source_video_path)
    i = 0
    while True:
        ret, frame = videoCapture.read()
        if ret:
            grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).T
            ret, gray = cv2.threshold(grayframe, 245, 255, cv2.THRESH_BINARY)

            white_pixels = np.count_nonzero(gray == [255])
            total_pixels = grayframe.shape[0] * grayframe.shape[1]
            white_percentage = white_pixels / total_pixels * 100
            if white_percentage >= 80:
                start_time = (i+1)/fps
                print("找到目标: %d min %.2f s，原神 启动！" %
                      (start_time/60, start_time % 60))
                print()
                return start_time+1
            i += 1
        else:
            break
    return -1
