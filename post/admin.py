from django.contrib import admin
from .models import Author, Category, Post, Comment, Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False 
    verbose_name_plural = 'Accounts'

class  CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)