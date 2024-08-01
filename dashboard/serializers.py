# dashboard/serializers.py

from django.contrib.auth import get_user_model
from .models import Company, Member,Project,ProjectImage
from rest_framework import serializers
from .models import Project, Task,CustomUser,Comment
from .models import Category, SubCategory, City, Region,ProjectFile

from .models import Project, ProjectImage,Task,ProjectStage,ProjectImageComment
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'fullname', 'phone', 'role', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            role=validated_data['role'],
            is_admin=validated_data.get('is_admin', False)
        )
        return user


# dashboard/serializers.py

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['MemberFullName', 'MemberPhone', 'MemberRole', 'MemberEmail', 'MemberPassword']



class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_done', 'is_fav', 'is_trash', 'category', 'project_id']

    def create(self, validated_data):
        project = validated_data.pop('project')
        task = Task.objects.create(project=project, **validated_data)
        return task

class TaskIsDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_done']


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    file = serializers.FileField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'project', 'user', 'text', 'created_at', 'parent', 'replies', 'file', 'image']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username
            }
        return None

    def create(self, validated_data):
        user_id = self.context['request'].data.get('user_id')
        user = CustomUser.objects.filter(id=user_id).first() if user_id else None
        
        file = validated_data.pop('file', None)
        image = validated_data.pop('image', None)

        comment = Comment.objects.create(user=user, **validated_data)

        if file:
            comment.file = file
        if image:
            comment.image = image
        
        comment.save()
        return comment


class ProjectImageCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=ProjectImageComment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ProjectImageComment
        fields = ['id', 'project_image', 'username', 'user', 'text', 'image', 'created_at', 'updated_at', 'parent', 'replies']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return ProjectImageCommentSerializer(obj.replies.all(), many=True).data
        return []

    def get_user(self, obj):
        if obj.user:
            return {'id': obj.user.id, 'username': obj.user.username}
        return None

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        user = None
        if username:
            user = CustomUser.objects.filter(id=username).first()
        
        parent = validated_data.pop('parent', None)
        comment = ProjectImageComment.objects.create(user=user, parent=parent, **validated_data)
        return comment

class ProjectImageSerializer(serializers.ModelSerializer):
    comments = ProjectImageCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'info', 'comments']


from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, SubCategory, City, Region, Company

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class CategoryUpdateSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id',"CompanyImage", 'CompanyName', 'CompanyPhoneNumber', 'CompanyEmail', 'CompanyAddress', 'members','project']

    def update(self, instance, validated_data):
        instance.CompanyName = validated_data.get('CompanyName', instance.CompanyName)
        instance.CompanyPhoneNumber = validated_data.get('CompanyPhoneNumber', instance.CompanyPhoneNumber)
        instance.CompanyEmail = validated_data.get('CompanyEmail', instance.CompanyEmail)
        instance.CompanyAddress = validated_data.get('CompanyAddress', instance.CompanyAddress)
        instance.save()
        return instance

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'uploaded_at']



class ProjectStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStage
        fields = ['id', 'project', 'stage', 'completed']
        read_only_fields = ['project', 'stage']















class ProjectCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [ 'id','title', 'lang','lat', 'start_date', 'end_date', 'assign', 'progress']









# //////////////////////////////////////
# serializers.py


# serializers.py
