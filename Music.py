import os
import shutil
import eyed3


def classify_music_by_artist(sourceFolder):
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(sourceFolder):
        if filename.endswith(".mp3"):  # 确保是MP3文件
            file_path = os.path.join(sourceFolder, filename)
            audio_file = eyed3.load(file_path)

            if audio_file and audio_file.tag:  # 确保文件有标签
                artist = audio_file.tag.artist  # 获取歌手名称
                if artist:  # 确保歌手名称不为空
                    # 创建歌手文件夹路径
                    artist_folder = os.path.join(sourceFolder, artist)
                    if not os.path.exists(artist_folder):
                        os.makedirs(artist_folder)  # 创建文件夹

                    # 移动文件到对应的歌手文件夹
                    shutil.move(file_path, os.path.join(artist_folder, filename))
            else:
                print(f"Skipping file: {file_path} - no metadata found.")
        else:
            print(f"Skipping file: {filename} - not an MP3 file.")


# 替换为你的音乐文件夹路径
source_folder = 'D:\\Music'
classify_music_by_artist(source_folder)
