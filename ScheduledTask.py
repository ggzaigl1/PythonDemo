import requests
from datetime import datetime
import pytz
import schedule
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
        dt_object = datetime.utcfromtimestamp(timestamp_s)
        dt_object = dt_object.replace(tzinfo=pytz.utc)
        beijing_time = dt_object.astimezone(pytz.timezone('Asia/Shanghai'))
        formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

        print("获取到的时间数据：", time_data)
        print("北京时间: ", formatted_time)
    else:
        print("请求失败，状态码：", response.status_code)


# 每5秒钟执行一次job函数
schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
