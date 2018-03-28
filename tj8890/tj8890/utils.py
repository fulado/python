"""
常用工具
"""
from django.core.paginator import Paginator


# 分页工具类
class MyPaginator(object):
    def __init__(self):
        self.page_range = []        # 页码范围
        self.show_begin = False     # 显示首页
        self.show_end = False       # 显示伟业
        self.object_list = []       # 当前页数据
        self.current_num = 0        # 当前页码
        self.total_objects = 0      # 共计多少条数据
        self.total_pages = 0        # 共计多少页

    def paginate(self, item_list, item_num, user_num):
        """
        :param item_list: 分页数据列表
        :param item_num: 每页显示几条数据
        :param user_num: 用户给定页码
        :return:
        """
        self.total_objects = len(item_list)

        p = Paginator(item_list, item_num)

        # 共计多少页
        self.total_pages = p.num_pages

        # 防止当用户给出的page_num超出分页范围
        if int(user_num) < 1:
            user_num = 1
        elif int(user_num) > p.num_pages:
            user_num = p.num_pages
        self.current_num = user_num

        # 计算显示的起始页码和结束页码
        begin_page = int(user_num) - 2
        end_page = int(user_num) + 2
        if begin_page < 1:
            begin_page = 1
        if end_page > p.num_pages:
            end_page = p.num_pages

        self.page_range = range(begin_page, end_page + 1)

        # 是否显示首尾页标识
        if begin_page > 1:
            self.show_begin = True
        else:
            self.show_begin = False

        if end_page < p.num_pages:
            self.show_end = True
        else:
            self.show_end = False

        # 返回的当页数据
        self.object_list = p.page(user_num)


if __name__ == '__main__':
    my_list = range(1, 11)
    mp = MyPaginator()
    mp.paginate(my_list, 3, 2)
    for i in my_list:
        print(i, end=',')
    print()
    for i in mp.object_list:
        print(i)
    print(mp.page_range)
    print(mp.current_num)
    print(mp.show_begin)
    print(mp.show_end)
