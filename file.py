import sys
import uuid
import cv2
import os
import hashlib

# 视频文件路径
video_path = 'Pad演示视频.mp4'
# 抽取帧的保存路径
base_folder_path = 'CCTV/Pic/'


def get_file_hash(file_path, hash_algorithm='md5'):
    hash_func = getattr(hashlib, hash_algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


if os.path.exists(video_path):
    print("文件存在。")
else:
    print("文件不存在。")
    sys.exit()

# 获取视频文件的哈希值
video_hash = get_file_hash(video_path)
print(f"视频的唯一标识: {video_hash}")

# 拼接完整的文件夹路径
full_folder_path = os.path.join(base_folder_path, video_hash)

# 检查这个路径的文件夹是否存在
if not os.path.exists(full_folder_path):
    # 如果不存在，创建文件夹
    os.makedirs(full_folder_path)
    print(f"文件夹 '{video_hash}' 已成功创建在：{full_folder_path}")
else:
    print(f"文件夹 '{video_hash}' 已存在。")
    sys.exit()

# 创建VideoCapture对象
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 获取视频的FPS帧率
fps = cap.get(cv2.CAP_PROP_FPS)

# 计算每隔多少帧抽取一帧，这里使用1秒作为间隔
interval = int(fps)

frame_count = 0
extracted_count = 1
while True:
    # 读取视频的下一帧
    ret, frame = cap.read()

    # 如果正确读取帧，ret为True
    if not ret:
        print("Finished extracting frames.")
        break

    # 每隔interval帧抽取一帧
    # if frame_count % (2 * fps) == 0:
    if frame_count % interval == 0:
        # 输出帧的文件名
        frame_filename = os.path.join(full_folder_path, f'{video_hash}_{extracted_count:04d}.jpg')

        # 保存帧为图片
        cv2.imwrite(frame_filename, frame)
        print(f'Extracted frame saved as: {frame_filename}')
        extracted_count += 1

    frame_count += 1

# 释放VideoCapture对象
cap.release()
print("Finished extracting frames.")
