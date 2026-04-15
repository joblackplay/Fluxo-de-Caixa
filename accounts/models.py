from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.

class MyAccountManage(BaseUserManager):
    def create_user(self,first_name,last_name,username,password=None):
        if not username:
            raise ValueError("Usuario precisa de um 'username' ")
        
        user =self.model(
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,first_name,last_name,username,password):
        user = self.create(
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin=True

        user.save()
        return user


class Account (AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    username = models.CharField(max_length=20)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_admin    = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username','first_name','last_name'] 

    objects = MyAccountManage()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

