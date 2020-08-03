from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GoodsInfo(models.Model):
    title = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='goods')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    describe = models.CharField(max_length=200)
    stored = models.IntegerField(default=100)
    content = HTMLField()
    type = models.ForeignKey('TypeInfo')

    def __str__(self):
        return self.title
