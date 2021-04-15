from django.db import models


class Product(models.Model):
    #поле Id создается автоматически
    title = models.CharField(max_length=100) # Наименование # String
    amount = models.FloatField() # Количество
    unit = models.CharField(max_length=100) # Единица измерения # String
    price = models.FloatField() # Цена за у.е. # Real
    date = models.DateField() # Дата последнего поступления # Date

