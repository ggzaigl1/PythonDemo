import os
import zipfile
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading


# 更新文本框的函数
def update_text(text_widget, text_content):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text_content)
    text_widget.see(tk.END)  # 自动滚动到文本框的底部
    text_widget.config(state=tk.DISABLED)


# 压缩单个文件夹的函数
def zip_folder(folder_path, zip_path, update_callback):
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname=relative_path)
        update_callback(f"已创建的zip文件: {os.path.basename(zip_path)}\n")
    except Exception as e:
        update_callback(f"压缩错误 {folder_path}: {e}\n")


# 压缩所有文件夹的函数
def compress_all_folders(directory, update_callback):
    if not os.path.isdir(directory):
        update_callback(f"选择的路径不是目录: {directory}\n")
        return

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            zip_filename = f"{item}.zip"
            zip_path = os.path.join(directory, zip_filename)
            threading.Thread(target=zip_folder, args=(item_path, zip_path, update_callback)).start()


# 选择文件夹并开始压缩的函数
def select_folder_and_compress(text_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        update_text(text_widget, "选择目录为: " + folder_selected + "\n")
        compress_all_folders(folder_selected, lambda message: update_text(text_widget, message))


# 创建主窗口
root = tk.Tk()
root.title("文件夹压缩")

# 创建按钮，点击时选择文件夹并压缩
compress_button = tk.Button(root, text="请选择要压缩的文件夹", command=lambda: select_folder_and_compress(text))
compress_button.pack(pady=20)

# 创建文本框来显示输出
text = scrolledtext.ScrolledText(root, width=70, height=20, state='disabled')
text.pack(pady=10)

# 运行主循环
root.mainloop()
