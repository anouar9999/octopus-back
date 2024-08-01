from django.contrib import admin
from .models import CustomUser, Company, Member, Project, Task, Comment, ProjectImage, Category, SubCategory, City, Region

from django.contrib import admin
from .models import CustomUser, Member, Company, Project, ProjectImage
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'fullname','is_admin', 'phone', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'fullname', 'phone', 'role')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fullname', 'email', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_admin','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'fullname', 'phone', 'role','is_admin', 'password1', 'password2'),
        }),
    )
    ordering = ('username',)
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('CompanyName', 'CompanyEmail', 'CompanyPhoneNumber')
    search_fields = ('CompanyName', 'CompanyEmail')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('MemberFullName', 'MemberEmail', 'MemberRole', 'company')
    list_filter = ('MemberRole', 'company')
    search_fields = ('MemberFullName', 'MemberEmail')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date', 'progress')
    list_filter = ('company', 'start_date', 'end_date')
    search_fields = ('title', 'description')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'is_done', 'is_fav', 'category')
    list_filter = ('is_done', 'is_fav', 'category', 'project')
    search_fields = ('title', 'project__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'text', 'created_at', 'parent')
    list_filter = ('project', 'created_at')
    search_fields = ('text', 'project__title')

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('get_project_title', 'image')
    search_fields = ('project__title',)

    def get_project_title(self, obj):
        return obj.project.title
    get_project_title.short_description = 'Project'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'description')
    list_filter = ('company',)
    search_fields = ('name', 'description')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category')
    list_filter = ('sub_category',)
    search_fields = ('name',)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)