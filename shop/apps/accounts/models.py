from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import UploadFile

#===========================================================================================================
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,name='',family='',email='',active_code=None,gender=None,password=None):
        if not mobile_number:
            raise('لطفا شماره موبایل را وارد کنید')
        
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,mobile_number,email,name,family,password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        
        user.save(using=self._db)
        return user
#===========================================================================================================
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,verbose_name='شماره تلفن',unique=True)
    name=models.CharField(max_length=50,verbose_name='نام',blank=True)
    family=models.CharField(max_length=50,verbose_name='نام خانوادگی',blank=True)
    email=models.EmailField(max_length=200,verbose_name='ایمیل',blank=True)
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=50,choices=GENDER_CHOICES,default="True",null=True,blank=True,verbose_name='جنسیت')
    file_upload=UploadFile('images','customuser')
    image_name=models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True,verbose_name='عکس پروفایل')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    active_code=models.CharField(max_length=100,verbose_name='کد فعالسازی',null=True,blank=True)
    is_admin=models.BooleanField(default=False,verbose_name='ادمین')
    
    objects=CustomUserManager()
    
    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS=['name','family','email']
    
    def __str__(self):
        return f'{self.name} {self.family}'
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'
#===========================================================================================================
class Customer(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='user')
    mobile_number=models.CharField(max_length=11,verbose_name='شماره تلفن')
    address=models.TextField(verbose_name='آدرس')
    
    def __str__(self):
        return self.user.name
    
    class Meta:
        verbose_name="مشتری"
        verbose_name_plural='مشتری ها'
#===========================================================================================================
