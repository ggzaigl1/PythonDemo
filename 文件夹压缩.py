import os
import zipfile
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import tkinter.messagebox as mbox

# 创建一个全局锁对象
lock = threading.Lock()


# 更新文本框的函数
def update_text(text_widget, text_content):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text_content)
    text_widget.see(tk.END)  # 自动滚动到文本框的底部
    text_widget.config(state=tk.DISABLED)


# 压缩单个文件夹的函数
def zip_folder(folder_path, zip_path, update_callback):
    global thread_count
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
    finally:
        lock.acquire()  # 获取锁
        thread_count -= 1
        if thread_count == 0:
            tk.messagebox.showinfo("完成", "所有文件夹都已压缩完成。")
        lock.release()  # 释放锁


# 压缩所有文件夹的函数
def compress_all_folders(directory, update_callback):
    global thread_count
    if not os.path.isdir(directory):
        update_callback(f"选择的路径不是目录: {directory}\n")
        return

    thread_count = 0  # 重置线程计数

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            zip_filename = f"{item}.zip"
            zip_path = os.path.join(directory, zip_filename)
            thread_count += 1  # 增加活跃线程计数
            threading.Thread(target=zip_folder, args=(item_path, zip_path, update_callback)).start()


# 选择文件夹并开始压缩的函数
def select_folder_and_compress(text_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        update_text(text_widget, "选择目录为: " + folder_selected + "\n")
        global thread_count
        thread_count = 0  # 重置线程计数
        compress_all_folders(folder_selected, lambda message: update_text(text_widget, message))


# 创建主窗口
root = tk.Tk()
root.title("文件夹压缩")
root.maxsize(500, 400)

icon_imager = 'res/py_icon_zip.png'
root.iconphoto(False, tk.PhotoImage(file=icon_imager))

# 创建按钮，点击时选择文件夹并压缩
compress_button = tk.Button(root, text="选择要压缩的文件夹", command=lambda: select_folder_and_compress(text))
compress_button.config(
    bg='#0099FF',  # 按钮背景颜色
    fg='white',  # 按钮字体颜色
    font=('Georgia', 12, 'bold'),  # 按钮字体大小和样式
    relief=tk.RAISED,  # 按钮的边框样式
    borderwidth=2,  # 按钮边框宽度
    padx=10,  # 按钮水平边距
    pady=5,  # 按钮垂直边距
    cursor='hand2'  # 鼠标悬停时的光标样式
)
compress_button.pack(pady=20)

# 创建文本框来显示输出
text = scrolledtext.ScrolledText(root, width=70, height=20, state='disabled')
text.config(
    fg='#FF3399',  # 字体颜色
    bg='#CCCCCC',  # 设置背景颜色和字体颜色
    font=('Helvetica', 12, 'bold'),
    state='disabled',  # 设置文本框的状态
    wrap='word',  # 设置文本的换行方式
    insertbackground='#FF3399',  # 设置插入光标的颜色
    highlightbackground='gray', highlightcolor='black'  # 设置鼠标悬停时的背景颜色和边框颜色
)
text.pack(pady=10)

# 运行主循环
root.mainloop()
