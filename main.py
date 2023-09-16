from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from os.path import realpath
from os import remove
from func import *


start_video_path = realpath(r"./source/Start.mp4")
start_audio_path = realpath(r"./source/Start.mp3")

source_video_path, target_video_path = get_video_path()

source_video = VideoFileClip(source_video_path)
start_video = VideoFileClip(start_video_path)
print("输入视频的参数：")
print(source_video.size, ", %d fps" % source_video.fps)

# 寻找视频中白色占比>=80%的帧，获取时间戳
if (start_time := get_start_time(source_video_path, source_video.fps)) == -1:
    print("视频含原量不足，起原引擎启动失败")
    source_video.close()
    start_video.close()
    exit(0)

# 检查两个视频是否具有相同的分辨率与帧率
if source_video.fps != start_video.fps or source_video.size != start_video.size:
    start_audio = AudioFileClip(start_audio_path)
    set_startvideo_attr(source_video)
    start_video.close()
    start_video = VideoFileClip(temp_video_path)
    start_video = start_video.set_audio(start_audio)

# 合并视频
target_video = concatenate_videoclips(
    [source_video.subclip(0, start_time), start_video],
    method='compose'
)
target_video.write_videofile(target_video_path)

print()
print("输出视频的参数：")
print(target_video.size, ", %d fps" % target_video.fps)

print()
print("Success !")
print("视频输出的位置: " + target_video_path)

source_video.close()
start_video.close()
target_video.close()
remove(temp_video_path)
