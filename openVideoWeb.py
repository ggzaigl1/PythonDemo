import tkinter as tk
import webbrowser


def open_website(url):
    webbrowser.open(url, new=2)  # new=2 会打开一个新的浏览器窗口


def center_window(width, height):
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的x和y坐标
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    # 设置窗口的位置
    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


root = tk.Tk()
root.title("网站快速访问")
root.iconbitmap('hourglass')

# 设置窗口居中
center_window(400, 100)  # 调整窗口宽度以适应按钮横向平铺

# 创建一个Frame用于放置按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=10)  # 将Frame放置在窗口中，并设置上下外边距

# 按钮1：打开优酷
youku_button = tk.Button(button_frame, text="打开优酷", command=lambda: open_website("https://www.youku.com/"))
youku_button.pack(side="left", padx=10)  # 使用pack布局管理器，设置按钮横向排列

# 按钮2：打开腾讯
tx_button = tk.Button(button_frame, text="打开腾讯", command=lambda: open_website("https://v.qq.com/"))
tx_button.pack(side="left", padx=10)  # 使用pack布局管理器，设置按钮横向排列

# 按钮3：打开爱奇艺
aiqyi_button = tk.Button(button_frame, text="打开爱奇艺", command=lambda: open_website("https://www.iqiyi.com/"))
aiqyi_button.pack(side="left", padx=10)  # 使用pack布局管理器，设置按钮横向排列

# 按钮3：打开Baidu
mg_button = tk.Button(button_frame, text="打开芒果TV", command=lambda: open_website("https://www.mgtv.com/"))
mg_button.pack(side="left", padx=10)  # 使用pack布局管理器，设置按钮横向排列

root.mainloop()
