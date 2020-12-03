from django.db import models


class Category(models.Model):
    """ カテゴリー
    """
    name = models.CharField("カテゴリー名", max_length=32)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ 製品
    """
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="カテゴリー")
    name = models.CharField("商品名", max_length=128)
    price = models.PositiveIntegerField("価格")
    photourl = models.TextField("写真URL",null=True)
