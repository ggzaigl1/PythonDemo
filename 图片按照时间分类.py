import os
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import filedialog, scrolledtext
import threading
from datetime import datetime


# 更新文本框的函数
def update_text(text_content):
    text.config(state=tk.NORMAL)
    text.insert(tk.END, text_content)
    text.see(tk.END)  # 自动滚动到文本框的底部
    text.config(state=tk.DISABLED)


# 根据创建时间分类图片的函数
def classify_images(folder_path):
    # 图片文件扩展名列表
    image_extensions = ['.png', '.jpg', '.jpeg', 'gif']
    # 获取文件夹中所有文件的数量
    total_files = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])
    processed_files = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 检查是否是文件以及是否是图片格式
        if os.path.isfile(file_path) and filename.lower().endswith(tuple(image_extensions)):
            modification_time = os.path.getmtime(file_path)
            creation_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')
            modification_date = os.path.join(folder_path, creation_date)
            if not os.path.exists(modification_date):
                os.makedirs(modification_date)
            dest_file_path = os.path.join(modification_date, filename)
            os.rename(file_path, dest_file_path)
            update_text(f"移动 {filename} 到 {modification_date}\n")
            processed_files += 1  # 处理的文件数量加一

            # 如果处理的文件数量等于总文件数量，则所有任务完成
            if processed_files == total_files:
                root.after(0, mbox.showinfo, "创建完成", "所有图片分类任务已完成。")


# 在后台线程中执行分类操作
def start_classify_images(folder_selected):
    threading.Thread(target=classify_images, args=(folder_selected,)).start()


# 选择文件夹并开始分类的函数
def select_folder_and_classify():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        update_text("选定的目录: " + folder_selected + "\n")
        start_classify_images(folder_selected)


# 创建主窗口
root = tk.Tk()
root.title("按照时间对图像进行分类")
root.maxsize(500, 400)
# error
# gray12
# gray25
# gray50
# gray75
# hourglass
# info
# questhead
# question
# warning
icon_path = 'res/py_icon_pic.png'  # 相对于当前工作目录的路径
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# 创建按钮，点击时选择文件夹并分类
classify_button = tk.Button(root, text="选择需要分类的文件夹", command=select_folder_and_classify)
classify_button.config(
    bg='#3399FF',  # 按钮背景颜色
    fg='white',  # 按钮字体颜色
    font=('Helvetica', 12, 'bold'),  # 按钮字体大小和样式
    relief=tk.RAISED,  # 按钮的边框样式
    borderwidth=2,  # 按钮边框宽度
    padx=10,  # 按钮水平边距
    pady=5,  # 按钮垂直边距
    cursor='hand2'  # 鼠标悬停时的光标样式
)
classify_button.pack(pady=20)

# 创建文本框来显示输出
text = scrolledtext.ScrolledText(root, width=70, height=40, state='disabled')
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
