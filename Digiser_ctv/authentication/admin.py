from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('code', 'phone_no', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone_no', 'is_verified', 'full_name',
         'address', 'qualification', 'identification', 'identification_address', 'note', 'code', 'role', 'status', 'updated_user'
                           )}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Bank', {'fields': ('account_number',
         'bank_name', 'branch', 'owner', 'code_bank')}),
        ('Dates', {'fields': ('last_login', 'date_joined', 'birthday', 'updated_time')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'phone_no', 'password1', 'password2', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email','phone_no','full_name','code')
    ordering = ('code',)


admin.site.register(CustomUser, CustomUserAdmin)
