import tkinter as tk
import requests
import datetime
import pytz
import threading
import time


def job():
    # 这里替换成你要调用的接口
    url = 'http://192.168.8.214:10043/api/v1/sxls/test/getTimeData'
    response = requests.get(url)

    if response.status_code == 200:
        # 获取时间数据
        time_data = response.json()
        # 打包数据，这里只是简单地打印出来，你可以根据需要进行打包
        timestamp_ms = time_data.get('content')
        # 将毫秒转换为秒
        timestamp_s = timestamp_ms / 1000.0
        # 将Unix时间戳转换为datetime对象
        dt_object = datetime.datetime.utcfromtimestamp(timestamp_s)
        dt_object = dt_object.replace(tzinfo=pytz.utc)
        beijing_time = dt_object.astimezone(pytz.timezone('Asia/Shanghai'))
        formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

        print("获取到的时间数据：", time_data)
        print("北京时间: ", formatted_time)
        text_box.insert(tk.END, "北京时间: {}\n".format(formatted_time))
    else:
        print("请求失败，状态码：", response.status_code)


def start_polling():
    while polling:
        job()
        time.sleep(1)  # 使用正确的time.sleep()


def on_start_click():
    global polling
    polling = True
    threading.Thread(target=start_polling).start()


def on_stop_click():
    global polling
    polling = False


def on_folder_path_change(*args):
    # 获取输入框的内容
    folder_path = folder_path_entry.get()
    # 打印内容，或者在这里执行其他操作
    print("输入的文件夹路径是:", folder_path)


root = tk.Tk()
root.title("我的第一个Tkinter程序")

# 设置窗口的宽度和高度
root.geometry("400x300")
root.maxsize(500, 400)
root.config(bg="#CD5C5C")
root.iconbitmap('hourglass')
# 创建一个frame作为按钮和输入框的容器
button_frame = tk.Frame(root)
button_frame.pack(expand=True, fill='both')  # 使button_frame在root中居中并填充

# 创建一个frame用于放置输入框
input_frame = tk.Frame(button_frame)
input_frame.pack(side="top", fill='x')

# 创建一个StringVar变量来跟踪输入框的内容变化
folder_path_var = tk.StringVar()

# 输入框，与StringVar变量关联
folder_path_entry = tk.Entry(input_frame, textvariable=folder_path_var)
folder_path_entry.pack(side="left", fill='x', expand=True, padx=10, pady=10)

# 添加追踪器，监听StringVar变量内容的变化
folder_path_var.trace("w", on_folder_path_change)

# 创建一个Text组件用于显示输出
text_box = tk.Text(root, height=10)
text_box.pack(expand=True, fill='both', padx=10, pady=10)

# 按钮点击时执行on_start_click函数
start_button = tk.Button(button_frame, text="开始轮询", command=on_start_click)
start_button.pack(side="left", padx=10, pady=10)  # 使按钮在button_frame中居左

# 按钮点击时执行on_stop_click函数
stop_button = tk.Button(button_frame, text="停止轮询", command=on_stop_click)
stop_button.pack(side="right", padx=10, pady=10)  # 使按钮在button_frame中居右

polling = False  # 初始化轮询标志为False

root.mainloop()
