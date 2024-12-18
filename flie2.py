import os
import glob
import cv2
import hashlib
import time

from file import cap

# 指定的文件夹路径
folder_path = 'D:\\AProject\\Video'

# 定义视频文件的扩展名
video_extensions = ('*.mp4', '*.mov', '*.avi', '*.mkv')

# 存储已处理视频的哈希值，用于跳过重复的视频
processed_videos = {}


# 抽帧函数
def extract_frames(video_path, output_folder, fps, interval):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % (interval * fps) == 0:
            frame_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_{extracted_count:04d}.jpg"
            frame_filepath = os.path.join(output_folder, frame_filename)
            cv2.imwrite(frame_filepath, frame)
            print(f'Extracted frame saved as: {frame_filepath}')
            extracted_count += 1
        frame_count += 1
    cap.release()


# 轮询并处理视频
def poll_and_process_videos(interval=10):
    global processed_videos
    while True:
        for ext in video_extensions:
            for video_path in glob.glob(os.path.join(folder_path, ext)):
                # 计算视频文件的哈希值
                video_hash = hashlib.md5(open(video_path, 'rb').read()).hexdigest()

                # 检查视频是否已处理
                if video_hash in processed_videos:
                    print(f"Skipping processed video: {video_path}")
                    continue

                print(f"Processing new video: {video_path}")
                # 定义输出文件夹
                output_folder = os.path.join(folder_path, 'extracted_frames')
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                # 视频帧率（假设已知）
                fps = cap.get(cv2.CAP_PROP_FPS)
                # 抽取帧的时间间隔（2秒）
                extract_frames(video_path, output_folder, fps, 2)

                # 标记为已处理
                processed_videos[video_hash] = True
                print(f"Finished processing video: {video_path}")

        time.sleep(interval)


# 调用轮询并处理视频函数
if __name__ == "__main__":
    poll_and_process_videos()