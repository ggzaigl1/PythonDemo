import os
import shutil

from PIL import Image
from datetime import datetime, timedelta

# 指定您的图片文件夹路径
source_folder = 'D:\\AProject\\Pic'


# 创建一个函数来获取图片的创建时间
def get_creation_date(path):
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()
            # 36867是创建时间的EXIF标签
            creation_time = exif_data[36867]
            return datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error getting creation date for {path}: {e}")
        return None


# 创建一个函数来创建基于日期的文件夹
def create_folder_based_on_date(date, base_folder):
    year = date.year
    month = date.strftime('%B')  # Full month name
    folder_path = os.path.join(base_folder, f'{year} {month}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        file_path = os.path.join(source_folder, filename)
        creation_date = get_creation_date(file_path)

        if creation_date:
            # 创建基于日期的文件夹
            folder_path = create_folder_based_on_date(creation_date, source_folder)
            # 移动文件到新的文件夹
            shutil.move(file_path, os.path.join(folder_path, filename))
        else:
            print(f"Skipping {filename}, could not determine creation date.")