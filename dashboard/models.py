# dashboard/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from django.conf import settings



class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=50)
    is_admin = models.BooleanField(max_length=50,default=False)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',  # Custom related_name
        related_query_name='user',
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',  # Custom related_name
        related_query_name='user',
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username




# dashboard/models.py





class Member(models.Model):
    MemberFullName = models.CharField(max_length=100,blank=True)
    MemberPhone = models.CharField(max_length=20)
    MemberRole = models.CharField(max_length=100)
    MemberEmail = models.EmailField()
    MemberPassword = models.CharField(max_length=100)
    company = models.ForeignKey('Company', related_name='members', on_delete=models.CASCADE)

from django.db import models
class Company(models.Model):
    CompanyImage = models.ImageField(upload_to='companies_images/',null=True)
    CompanyName = models.CharField(max_length=100, blank=True)
    CompanyPhoneNumber = models.CharField(max_length=20, blank=True)
    CompanyEmail = models.EmailField()
    CompanyAddress = models.CharField(max_length=255)

    def __str__(self):
        return self.CompanyName

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='categories', on_delete=models.CASCADE,null=True)
class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    sub_category = models.ForeignKey(SubCategory, related_name='cities', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='city_images/', blank=True, null=True)  # Define ImageField for city images

    def __str__(self):
        return self.name
        
class Region(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name='regions', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    company = models.ForeignKey(Company, related_name='projects', on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, related_name='projects', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)  # New field for location
    start_date = models.DateField()
    end_date = models.DateField()
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.title
        

def comment_file_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/comments/<project_id>/<filename>
    return f'comments/{instance.project.id}/{filename}'


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_files/', null=True, blank=True)
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)

    def __str__(self):
        return self.text[:20] + '...'
class Task(models.Model):   
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    is_fav = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    category = models.CharField(max_length=50, default='low')
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title







# ///////////////////////////////////////

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProjectStage(models.Model):
    STAGE_CHOICES = [
        ('reperage', 'Reperage'),
        ('maquette', 'Maquette'),
        ('dessins_technique', 'Dessins Technique'),
        ('simulation', 'Simulation'),
        ('realisation', 'Realisation'),
    ]

    project = models.ForeignKey(Project, related_name='stages', on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['project', 'stage']

    def __str__(self):
        return f"{self.project.title} - {self.get_stage_display()}"

@receiver(post_save, sender=Project)
def create_project_stages(sender, instance, created, **kwargs):
    if created:
        for stage_choice, _ in ProjectStage.STAGE_CHOICES:
            ProjectStage.objects.create(project=instance, stage=stage_choice)

class ProjectFile(models.Model):
    stage = models.ForeignKey(ProjectStage, related_name='files', on_delete=models.CASCADE,null=True)
    file = models.FileField(upload_to='project_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ProjectImage(models.Model):
    stage = models.ForeignKey(ProjectStage, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='project_images/')
    info = models.CharField(max_length=255, null=True)  # Changed from 'name' to 'info'
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.info if self.info else "No info provided"


class ProjectImageComment(models.Model):
    project_image = models.ForeignKey(ProjectImage, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user or 'Anonymous'} on {self.project_image}"

    class Meta:
        ordering = ['-created_at']