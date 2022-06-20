from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, default='no-category')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/stuff/category/{self.slug}'

    class Meta:
        verbose_name_plural : 'Categories'

class Stuff(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name='제품명')
    image = models.ImageField(upload_to='stuff/images/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    fee = models.IntegerField(verbose_name='대여료')
    desc = models.CharField(max_length=500, verbose_name='설명')

    STUFF_STATUS = (
        ('a', 'available'),
        ('u', 'unavailable'),
    )

    status = models.CharField(
        max_length = 1,
        choices = STUFF_STATUS,
        blank = True,
        default = 'a',
        help_text = 'Stuff availability',
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.author}님께서 등록하신 물건 <{self.name}>'

    def get_absolute_url(self):
        return f'/stuff/{self.pk}/'

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='대여자')
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, verbose_name='제품')
    rental_date = models.DateTimeField(verbose_name='대여일')
    return_date = models.DateTimeField(verbose_name='반납일')
    total_fee = models.IntegerField(verbose_name='대여료 총액')

    RENTAL_STATUS = (
        ('d', 'Default'),
        ('r', 'Request'),
        ('a', 'Accept'),
        ('c', 'Completed'),
    )

    status = models.CharField(
        max_length = 1,
        choices = RENTAL_STATUS,
        blank = True,
        default = 'd',
        help_text = 'Rental availability',
    )

    def __str__(self):
        return f'{self.user}님께서 {self.rental_date}부터 {self.return_date}까지 대여한 <{self.stuff.name}>'