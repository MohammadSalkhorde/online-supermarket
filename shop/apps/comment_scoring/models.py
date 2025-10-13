from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator

#=======================================================================================
class Scoring(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='scoring_product')
    scoring_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر امتیاز دهنده',related_name='scoring_user')
    score=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name='امتیاز')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت امتیاز')
    
    def __str__(self):
        return f'{self.user} {self.product}'
    
    class Meta:
        verbose_name='امتیاز'
        verbose_name_plural='امتیازات'
#=======================================================================================
class Comment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='کالا',related_name='comments_product')
    commenting_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر نظر دهنده',related_name='comments_user1')
    approving_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر تایید کننده نظر',related_name='comments_user2',null=True,blank=True)
    comment_text=models.TextField(verbose_name='متن نظر')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت نظر')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    comment_parent=models.ForeignKey('Comment',on_delete=models.CASCADE,verbose_name='والد نظر',related_name='comments_child',null=True,blank=True)
    
    def __str__(self):
        return f'{self.product} - {self.commenting_user} - {self.comment_text}'
    
    class Meta:
        verbose_name='نظر'
        verbose_name_plural='نظرات'
#=======================================================================================