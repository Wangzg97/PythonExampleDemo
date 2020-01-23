import itchat
import json
from pyecharts.charts import Geo, Bar, Pie
from pyecharts import options as opts


# 获取微信好友信息
class GetFriends(object):
    def __init__(self):
        self.friends = []  # get_friends()返回一个列表
        self.unknown = 0  # 未知性别的人数
        self.female = 0  # 女性人数
        self.male = 0  # 男性人数

    def login(self):
        itchat.auto_login(hotReload=True)  # 短时间内退出程序不用重新登陆
        self.friends = itchat.get_friends(update=True)

    # 保存到本地
    def save(self):
        with open('friends_info.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.friends, indent=4, ensure_ascii=False))  # indent设置缩进

    # 统计性别数量
    def sex_classify(self):
        for friend in self.friends:
            if friend['Sex'] == 0:
                self.unknown += 1
            elif friend['Sex'] == 1:
                self.female += 1
            else:
                self.male += 1

        labels = ['unknown', 'male', 'female']
        sex_num = [self.unknown, self.female, self.male]
        # 画饼图
        pie = (
            Pie()
            .add(
                "",
                [list(x) for x in zip(labels, sex_num)],
                # radius=["40%", "75%"], # 环形
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="微信好友性别分布"))
        )
        pie.render("sex_num.html")

    # 获取省份信息
    def province_info(self):
        dict_province = dict()
        for friend in self.friends:
            key = friend['Province']
            if key not in dict_province.keys():
                dict_province[key] = 1
            else:
                dict_province[key] += 1
        province_list = []
        num_list = []
        for province, num in dict_province.items():
            if province == "":
                province = "其他地区"
            province_list.append(province)
            num_list.append(num)

        # 画柱状图
        bar = (
            Bar()
            .add_xaxis(province_list)
            .add_yaxis("省份", num_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="好友省份分布", subtitle=""))
        )
        bar.render("province.html")

    # 获取城市信息
    def city_info(self):
        dict_city = dict()
        for friend in self.friends:
            key = friend['City']
            if key not in dict_city.keys():
                dict_city[key] = 1
            else:
                dict_city[key] += 1
        city = []
        # max_num = 0  # 某个城市中最多的人数
        for key, value in dict_city.items():
            # 其他地区
            if len(key) == 0:
                continue
            # 过滤英文等非市级
            if len(key) >= 3:
                continue
            city.append(tuple((key, value)))
            # if value > max_num:
            #     max_num = value

        # 地图标注
        # geo = Geo("微信好友城市分布图", "data from WeChat", title_color="#fff", title_pos="center",
        #           width=1200, height=600, background_color='#404a59')
        # attr, value = geo.cast(city)
        # geo.add("", attr, value, visual_range=[0, 50], visual_text_color="#fff", symbol_size=15, is_visualmap=True)
        # geo.show_config()
        geo = (
            Geo()
            .add_schema(maptype="china")
            .add(
                "人数",
                city
            )
        )
        geo.render("city.html")


if __name__ == '__main__':
    test = GetFriends()
    test.login()
    test.save()
    test.sex_classify()
    test.province_info()
    test.city_info()
