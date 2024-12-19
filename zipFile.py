import os
import zipfile


def zip_folders_in_directory(directory):
    # 遍历指定目录下的所有项
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # 确保是文件夹而不是文件
        if os.path.isdir(item_path):
            # 创建zip文件名，使用文件夹名和.zip扩展名
            zip_filename = f"{item}.zip"
            zip_path = os.path.join(directory, zip_filename)

            # 创建zip文件并添加文件夹
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 计算zip中的相对路径
                        relative_path = os.path.relpath(file_path, directory)
                        zipf.write(file_path, arcname=relative_path)

            print(f"Created zip file: {zip_path}")


# 调用函数，传入你想要压缩文件的目录
zip_folders_in_directory('D:\\AProject\\Pic')
