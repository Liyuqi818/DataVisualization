# author LYQ
# Date 2021/1/24
import pandas as pd  # 将数据转换成DataFrame格式
import mplfinance as mpf  # 该库可直接实现阴阳烛图，折线图，以上下子图形式呈现
import json  # 对json数据解析

# 定义列表变量
close_list = []   # 收市价
date_list = []    # 日期
open_list = []    # 开市价
high_list = []    # 最高价
low_list = []     # 最低价


# 读取json文件，获取所需数据
def read_file(path):
    f = open(path, encoding='utf-8')   # 打开project1程序生成的json文件，并设置'utf-8'编码
    dict_content = json.load(f)    # 读取json文件数据
    for i in dict_content:   # 遍历dict_content
        if dict_content[i]['Close'] is None or dict_content[i]['Date'] is None:   # 剔除为null的数据，若不剔除将直接报错
            continue
        close_list.append(float(dict_content[i]['Close']))   # 将Close数据保存进close_list
        open_list.append(float(dict_content[i]['Open']))     # 将Open数据保存进open_list
        high_list.append(float(dict_content[i]['High']))     # 将High数据保存进high_list
        low_list.append(float(dict_content[i]['Low']))       # 将Low数据保存进low_list
        date_list.append(pd.to_datetime(dict_content[i]['Date']))  # pd.to_datetime()方法  将date日期进行时间序列化

    all_data = {
        "Open": open_list,
        "High": high_list,
        "Low": low_list,
        "Close": close_list
    }
    return all_data    # 返回字典格式数据


# 1、绘制收市价折线图
# 2、绘制阴阳烛图，上（收市价折线图）下（阴阳烛图）并排的子图
def draw_line_candle(data):
    # 将data转换成DataFrame格式
    df = pd.DataFrame(data, index=date_list)
    # mplfinance 绘制收市价折线图(子图)，panel显示位置优先级设置为0(最优先)，即处于画布的上半部，color设置线条颜色
    add_plot = [mpf.make_addplot(data['Close'], panel=0, color='blue')]
    # 绘制阴阳烛图 ,main_panel设置主图显示位置优先级，
    mpf.plot(df,
             type="candle",  # type可选'line'
             addplot=add_plot,  # 引入子图模块
             main_panel=1,  # type可选'line'、'candle'...
             datetime_format='%Y-%m-%d',  # 设置日期格式
             figratio=(40, 20))   # 绘制出的图片大小


# 主函数调用
if __name__ == "__main__":
    column_data = read_file('AAPL.json')
    draw_line_candle(column_data)
