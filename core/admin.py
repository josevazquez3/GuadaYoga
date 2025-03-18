from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Video, Contact

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_status')
    
    def get_profile_status(self, obj):
        return obj.profile.is_active
    get_profile_status.short_description = 'Active'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'summary')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'subject', 'created_at')
    search_fields = ('name', 'surname', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
