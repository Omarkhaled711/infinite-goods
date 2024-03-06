'''
Admin model for the users app
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class custom_userAdmin (UserAdmin):
    list_display = ('first_name', 'last_name', 'user_name',
                    'email', 'date_joined', 'last_login', 'is_active')

    list_display_links = ('first_name', 'last_name', 'user_name', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined', )
    # Those variables must be set so that djanog is able to
    # parse the information

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(User, custom_userAdmin)
