from .models import TypeInfo, GoodsInfo


class GoodsDao(object):
    # 查询商品分类信息
    @staticmethod
    def get_all_type():
        return TypeInfo.objects.all()

    # 查询商品信息
    @staticmethod
    def get_all_goods():
        return GoodsInfo.objects.all()
