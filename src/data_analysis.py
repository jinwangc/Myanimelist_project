import pandas as pd
import data_preprocessor as dp
import requests
import time
import pyecharts
import numpy as np
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import seaborn as sns
import math
from pyecharts import options as opts
from pyecharts.charts import HeatMap
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
from pyecharts.charts import Bar


# object of anime analysis
class anime_process():
    # read the datafile from local
    def __init__(self):
        self.myanimelist_anime = pd.read_csv("../data/processed_Myanimelist_anime_Data.csv")
        self.myanimelist_manga = pd.read_csv('../data/processed_Myanimelist_manga_Data.csv')
        self.anilist_data = pd.read_csv('../data/processed_Anilist_Data.csv')
        self.manga_sales = pd.read_csv('../data/processed_Wikipedia_manga_sales_Data.csv')
    # get the top data of myanimelist anime
    def get_myani_ani_top(self, n, offset=0):

        myani = []
        columns = self.myanimelist_anime.columns.to_list()

        if n > 10:
            return print('Too big number, you should input a small numebr!')

        for i in range(offset, n + offset):
            myani_dic = {}
            for j in range(8):
                myani_dic[columns[j]] = self.myanimelist_anime[columns[j]][i]
            myani.append(myani_dic)
        #             print(myani)

        return myani
    # get the top data of myanimelist manga
    def get_myani_man_top(self, n, offset=0):
        myani = []
        columns = self.myanimelist_manga.columns.to_list()
        if n > 10:
            return print('Too big number, you should input a small numebr!')
        for i in range(offset, n + offset):
            myani_dic = {}
            for j in range(15):
                myani_dic[columns[j]] = self.myanimelist_manga[columns[j]][i]
            myani.append(myani_dic)
        return myani
    # get the top of anilist anime
    def get_anilist_top(self, n, offset=0):
        myani = []
        columns = self.anilist_data.columns.to_list()
        if n > 10:
            return print('Too big number, you should input a small numebr!')
        for i in range(offset, n + offset):
            ani_dic = {}
            for j in range(11):
                ani_dic[columns[j]] = self.anilist_data[columns[j]][i]
            myani.append(ani_dic)
        return myani
    # used to show the imgs of given image link.
    def show(self, dic, na, img_l):
        name = []
        imgs = []
        for i in dic:
            name.append(i[na])
            imgs.append(i[img_l])

        if len(imgs) == 1:
            while (True):
                try:
                    response = requests.get(imgs[0])
                    break
                except:
                    time.sleep(2)
            image = Image.open(BytesIO(response.content))
            plt.title(name[0])
            plt.axis('off')
            plt.imshow(image)
        elif len(imgs) == 2:
            fig, ax = plt.subplots(1, 2, figsize=(15, 2))
            for i in range(2):
                while (True):
                    try:
                        response = requests.get(imgs[i])
                        break
                    except:
                        time.sleep(2)
                image = Image.open(BytesIO(response.content))
                #             if len(imgs)>5:
                ax[i].imshow(image)
                ax[i].set_title(name[i])
                ax[i].axis('off')

        else:
            height = len(name)
            if height % 2 == 1:
                height += 1
            fig, ax = plt.subplots(nrows=math.ceil(len(name) / 2), ncols=2, figsize=(15, height + 2))
            for i in range(len(imgs)):
                while (True):
                    try:
                        response = requests.get(imgs[i])
                        break
                    except:
                        time.sleep(2)
                image = Image.open(BytesIO(response.content))
                #             if len(imgs)>5:
                ax[i // 2, i % 2].imshow(image)
                ax[i // 2, i % 2].set_title(name[i])
                ax[i // 2, i % 2].axis('off')
            #             else:
            #                 ax[i].imshow(image)
            #                 ax[i].set_title(dic['name'][i],fontsize=2)
            #                 ax[i].axis('off')
            plt.tight_layout()
            plt.axis('off')
            plt.show()

    #get the link of anime stats page
    def get_anime_stats_link(self, dic):
        return [i + '/stats' for i in dic['link']]

    #use pyecharts to plot heatmap
    def heat_map_echart(self, values, columns, name):
        #         value = [[i, j, round(df2.corr(method='spearman').values.tolist()[i][j], 2)] for i in range(11) for j in
        #                  range(11)]
        #         columns = list(df2.columns)
        c = (
            HeatMap()
                .add_xaxis(columns)
                .add_yaxis(
                "series1",
                columns,

                values,
                label_opts=opts.LabelOpts(is_show=True, position="inside"),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=f'Heatmap of {name}'),
                xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
                #set the min=-1 and max=1,to show the range of coefficient
                visualmap_opts=opts.VisualMapOpts(min_=-1, max_=1),

            )
            #     .render("heatmap_with_label_show.html")
        )
        return c.render_notebook()

    #use pyecharts to plot pie
    def plot_pie(self, num, name):
        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(num[:10].index.tolist(), num[:10].tolist())],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 10, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=f"Pie-{name}"),
                # put the legend on the right and in vertical format
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
            )

        )
        return c.render_notebook()
    # get the word cloud
    def word_cloud(self, num, name):
        c = (
            WordCloud()
                .add(series_name="Words Cloud",
                     data_pair=(list(z) for z in zip(num[:].index.tolist(), num[:].tolist())),
                     word_size_range=[6, 100])
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"Words_cloud of {name}", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
            #     .render("basic_wordcloud.html")
        )
        return c.render_notebook()

    # plot bar, if "echarts" is true, use pyecharts to plot else use matplotlib to plot
    def plot_bar(self, name, feature_names, feature_importances, echarts=True, is_show=False):
        if echarts is True:
            c = (
                Bar()
                    .add_xaxis(feature_names)
                    .add_yaxis("importance", [round(i, 2) for i in feature_importances])
                    .reversal_axis()
                    .set_series_opts(
                    label_opts=opts.LabelOpts(
                        is_show=False,
                        position="right"
                        #             formatter=JsCode(
                        #                 "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                        #             ),
                    ))
                    .set_global_opts(
                    tooltip_opts=opts.TooltipOpts(
                        is_show=True, trigger="axis", axis_pointer_type="shadow"
                    ),
                    title_opts=opts.TitleOpts(title=f"Bar-{name}"),
                    datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside"),
                                   opts.DataZoomOpts(orient="vertical")],
                )
                #     .render("bar_datazoom_both.html")
            )
            return c.render_notebook()
        else:
            fea_ = feature_importances
            fea_name = feature_names
            plt.figure(figsize=(10, 10))
            plt.barh(fea_name, fea_, height=0.5)
            plt.title(f'Bar-{name}')











