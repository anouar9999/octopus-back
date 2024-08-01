from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from dashboard.serializers import UserSerializer,MemberSerializer,ProjectCardSerializer,TaskSerializer,TaskIsDoneSerializer,CommentSerializer,CompanySerializer,CategorySerializer
from dashboard.models import CustomUser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Company,ProjectImage,Task
from .serializers import CompanySerializer,ProjectImageSerializer,TaskSerializer,ProjectImageCommentSerializer
import logging

from .models import Member,Comment,ProjectImageComment
from .models import Project
from .serializers import ProjectSerializer
import json
from rest_framework.parsers import MultiPartParser, FormParser

from django.http import HttpResponse
import os
User = get_user_model()
logger = logging.getLogger(__name__)
from rest_framework import generics, permissions
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        logger.debug("Received registration request: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            logger.debug("User created successfully: %s", user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Error in registration: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch companies where the user is a member
        companies = Company.objects.filter(members__MemberEmail=user.email).distinct()

        user_data = UserSerializer(user).data
        company_data = CompanySerializer(companies, many=True).data

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': user_data,
            'companies': company_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'status': status.HTTP_200_OK,
        })
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import logging



logger = logging.getLogger(__name__)

class ProjectCreateAPIView2(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        logger.info(f"Received POST request: {request.data}")
        data = request.data.copy()

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not start_date:
            logger.error("start_date is required but not provided.")
            return Response({"start_date": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        if not end_date:
            logger.error("end_date is required but not provided.")
            return Response({"end_date": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the 'assign' field
        assign_data = data.get('assign')
        if isinstance(assign_data, dict):
            assign_label = assign_data.get('label', '')
        else:
            assign_label = assign_data

        data['assign'] = assign_label

        # Convert 'region_name' to the corresponding Region object
        region_name = data.get('region_name')
        if region_name:
            try:
                region = Region.objects.get(name=region_name)
                data['region'] = region.id  # Set the region's ID in the data
            except Region.DoesNotExist:
                logger.error(f"Region with name '{region_name}' does not exist.")
                return Response({"region_name": ["Invalid region name."]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("region_name is required but not provided.")
            return Response({"region_name": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()
            logger.info(f"Project created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Project creation failed with errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        region_name = self.request.query_params.get('region_name', None)

        if region_name:
            try:
                region = Region.objects.get(name=region_name)
                queryset = queryset.filter(region=region)
            except Region.DoesNotExist:
                return Project.objects.none()  # Return an empty queryset if region not found

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

class ProjectDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectCardSerializer
    lookup_url_kwarg = 'pk'  # Specify the name of the URL pattern variable to use for object lookup

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
class ProjectUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
class ProjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'


class CompanyListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)  # This removes the authorization requirement
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer, MemberSerializer
from django.db import transaction

import json
import os
from django.utils.crypto import get_random_string
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer, MemberSerializer
import uuid
from django.contrib.auth.hashers import make_password

class CompanyCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            company = serializer.save()
            
            # Handle file upload and rename the file
            if 'CompanyImage' in request.FILES:
                file = request.FILES['CompanyImage']
                filename, file_extension = os.path.splitext(file.name)
                new_filename = f"{get_random_string(20)}{file_extension}"
                file.name = new_filename
                company.CompanyImage = file
                company.save()

            # Handle members
            members_data = json.loads(request.data.get('members', '[]'))
            for member_data in members_data:
                member_serializer = MemberSerializer(data=member_data)
                if member_serializer.is_valid():
                    member_serializer.save(company=company)
                else:
                    return Response({'error': member_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompanyUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Handle company data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Handle members data
        members_data = request.data.get('members')
        if members_data:
            try:
                members_data = json.loads(members_data)
            except json.JSONDecodeError:
                return Response({"error": "Invalid JSON for members data"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete existing members and associated CustomUser instances
            member_emails = instance.members.values_list('MemberEmail', flat=True)
            CustomUser.objects.filter(email__in=member_emails).delete()
            instance.members.all().delete()

            # Create new members and CustomUser instances
            for member_data in members_data:
                member_serializer = MemberSerializer(data=member_data)
                if member_serializer.is_valid():
                    member = member_serializer.save(company=instance)
                    
                    # Generate a unique username
                    username = f"{member.MemberFullName.replace(' ', '_')}"
                    
                    # Create or update CustomUser
                    user, created = CustomUser.objects.update_or_create(
                        email=member.MemberEmail,
                        defaults={
                            'username': username,
                            'fullname': member.MemberFullName,
                            'phone': member.MemberPhone,
                            'role': member.MemberRole,
                        }
                    )
                    
                    # Set password securely
                    if member.MemberPassword:
                        user.password = make_password(member.MemberPassword)
                        user.save()
                else:
                    return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CompanyDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Company.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Delete associated CustomUser instances
        member_emails = instance.members.values_list('MemberEmail', flat=True)
        CustomUser.objects.filter(email__in=member_emails).delete()

        # The deletion of members will be handled by the on_delete=models.CASCADE on the Member model
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics, permissions
from .models import Company, Project
from .serializers import CompanySerializer

class CompanyDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Company.objects.prefetch_related('projects')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Fetch related projects
        projects = Project.objects.filter(company=instance)
        data['projects'] = ProjectSerializer(projects, many=True).data

        return Response(data)
class CompanyCategoriesList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        try:
            company = Company.objects.get(pk=company_id)
            return company.categories.all()  # Fetch categories associated with the company
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

from django.shortcuts import get_object_or_404

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Task.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)

class TaskUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'

class TaskIsDoneUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskIsDoneSerializer
    lookup_field = 'pk'

class TaskDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_url_kwarg = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(project=project)

class CommentListAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Comment.objects.filter(project_id=project_id, parent=None)


class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReplyDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        reply_id = kwargs.get('reply_id')
        reply = instance.replies.filter(id=reply_id).first()
        if reply:
            reply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




# :::::::::::::::::::::::::::::::::::::::
# views.py
from rest_framework import viewsets
from .models import Category, SubCategory, City, Region
from .serializers import CategorySerializer, SubCategorySerializer, CitySerializer, RegionSerializer



from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request, *args, **kwargs):
        company_id = request.data.get('company_id')
        if not company_id:
            return Response({"error": "company_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='by-company/(?P<company_id>[^/.]+)')
    def list_by_company(self, request, company_id=None):
        categories = self.queryset.filter(company_id=company_id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, category_id, format=None):
        try:
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
   
class CategoryUpdateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_id, format=None):
        category = self.get_object(category_id)
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, category_id, format=None):
        category = self.get_object(category_id)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        # Filter subcategories based on category name if provided in the URL
        category_name = self.kwargs.get('category_name')
        if category_name:
            return SubCategory.objects.filter(category__name=category_name)
        return super().get_queryset()

    # Allow GET, POST, and DELETE methods
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        # Extract category_name from URL
        category_name = self.kwargs.get('category_name')
        if not category_name:
            return Response({"error": "category_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the category object
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Make a mutable copy of request.data
        data = request.data.copy()
        # Set the category_id in the request data
        data['category'] = category.id

        # Create a new serializer instance with the modified data
        serializer = self.get_serializer(data=data)
        # Validate and save the new subcategory
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return the response with the newly created subcategory
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()

class SubCategoryRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, subcategory_id):
        try:
            return SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return None

    def get(self, request, subcategory_id, format=None):
        subcategory = self.get_object(subcategory_id)
        if subcategory:
            serializer = SubCategorySerializer(subcategory)
            return Response(serializer.data)
        else:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

class SubCategoryUpdateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, subcategory_id):
        try:
            return SubCategory.objects.get(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return None

    def put(self, request, subcategory_id, format=None):
        subcategory = self.get_object(subcategory_id)
        if subcategory:
            serializer = SubCategorySerializer(subcategory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, subcategory_id, format=None):
        subcategory = self.get_object(subcategory_id)
        if subcategory:
            serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)




from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import City
from .serializers import CitySerializer
from .models import SubCategory  # Import your SubCategory model

class CityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        # Filter cities based on subcategory name if provided in the URL
        subcategory_name = self.kwargs.get('subcategory_name')
        if subcategory_name:
            return City.objects.filter(sub_category__name=subcategory_name)
        return super().get_queryset()

    # Allow GET, POST, PUT, and DELETE methods
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        subcategory_name = self.kwargs.get('subcategory_name')
        if not subcategory_name:
            return Response({"error": "subcategory_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = get_object_or_404(SubCategory, name=subcategory_name)
        except SubCategory.DoesNotExist:
            return Response({"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['sub_category'] = subcategory.id  # Set the subcategory_id in the request data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Handle image upload
        image_file = request.data.get('image')
        if image_file:
            serializer.validated_data['image'] = image_file

        serializer.save(sub_category=subcategory)  # Save the serializer with the subcategory instance
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Handle image upload
        image_file = request.data.get('image')
        if image_file:
            serializer.validated_data['image'] = image_file

        serializer.save()  # Save the serializer
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except City.DoesNotExist:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()

class CityRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, city_id):
        try:
            return City.objects.get(id=city_id)
        except City.DoesNotExist:
            return None

    def get(self, request, city_id, format=None):
        city = self.get_object(city_id)
        if city:
            serializer = CitySerializer(city)
            return Response(serializer.data)
        else:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

class CityUpdateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, city_id):
        try:
            return City.objects.get(id=city_id)
        except City.DoesNotExist:
            return None

    def put(self, request, city_id, format=None):
        city = self.get_object(city_id)
        if not city:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the request contains a file
        if 'image' in request.FILES:
            # Update the image field separately
            city.image = request.FILES['image']

        serializer = CitySerializer(city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        # Filter regions based on city name if provided in the URL
        city_name = self.kwargs.get('city_name')
        if city_name:
            return Region.objects.filter(city__name=city_name)
        return super().get_queryset()

    # Allow GET, POST, and DELETE methods
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        # Extract city_name from URL
        city_name = self.kwargs.get('city_name')
        if not city_name:
            return Response({"error": "city_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the city object
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

        # Make a mutable copy of request.data
        data = request.data.copy()
        # Set the city_id in the request data
        data['city'] = city.id

        # Create a new serializer instance with the modified data
        serializer = self.get_serializer(data=data)
        # Validate and save the new region
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return the response with the newly created region
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Region.DoesNotExist:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()


class RegionRetrieveAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_object(self, region_id):
        try:
            return Region.objects.get(id=region_id)
        except Region.DoesNotExist:
            return None

    def get(self, request, region_id, format=None):
        region = self.get_object(region_id)
        if region:
            serializer = RegionSerializer(region)
            return Response(serializer.data)
        else:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

class RegionUpdateAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, region_id):
        try:
            return Region.objects.get(id=region_id)
        except Region.DoesNotExist:
            return None

    def put(self, request, region_id, format=None):
        region = self.get_object(region_id)
        if region is None:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RegionSerializer(region, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, ProjectStage
from .serializers import ProjectSerializer, ProjectStageSerializer, ProjectFileSerializer, ProjectImageSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def stages(self, request, pk=None):
        project = self.get_object()
        stages = project.stages.all()
        serializer = ProjectStageSerializer(stages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stage(self, request, pk=None):
        project = self.get_object()
        stage_name = request.query_params.get('stage', None)
        if stage_name is None:
            return Response({"error": "Stage parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stage = project.stages.get(stage=stage_name)
            serializer = ProjectStageSerializer(stage)
            return Response(serializer.data)
        except ProjectStage.DoesNotExist:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import ProjectStage, ProjectImage
from .serializers import ProjectStageSerializer, ProjectImageSerializer

class ProjectStageViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_stage(self, project_pk, stage_name):
        try:
            return ProjectStage.objects.get(project_id=project_pk, stage=stage_name)
        except ProjectStage.DoesNotExist:
            return None

    @action(detail=True, methods=['post'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/upload_image')
    def upload_image(self, request, project_pk=None, stage_name=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        image_serializer = ProjectImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save(stage=stage)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/images')
    def list_images(self, request, project_pk=None, stage_name=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        images = stage.images.all()
        serializer = ProjectImageSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/images/(?P<image_pk>[^/.]+)/delete')
    def delete_image(self, request, project_pk=None, stage_name=None, image_pk=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            image = stage.images.get(pk=image_pk)
        except ProjectImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        image.delete()
        return Response({"message": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ProjectImageCommentListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectImageCommentSerializer

    def get_queryset(self):
        return ProjectImageComment.objects.filter(project_image_id=self.kwargs['image_id'], parent=None)

    def perform_create(self, serializer):
        project_image_id = self.kwargs['image_id']
        project_image = ProjectImage.objects.get(id=project_image_id)
        serializer.save(project_image=project_image)

class ProjectImageCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = ProjectImageComment.objects.all()
    serializer_class = ProjectImageCommentSerializer
class ProjectImageCommentReplyView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectImageCommentSerializer

    def perform_create(self, serializer):
        parent_comment = ProjectImageComment.objects.get(id=self.kwargs['comment_id'])
        project_image = parent_comment.project_image
        serializer.save(project_image=project_image, parent=parent_comment)
class ProjectStageFilesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_stage(self, project_pk, stage_name):
        try:
            return ProjectStage.objects.get(project_id=project_pk, stage=stage_name)
        except ProjectStage.DoesNotExist:
            return None

    @action(detail=False, methods=['post'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/upload_file')
    def upload_file(self, request, project_pk=None, stage_name=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        file_serializer = ProjectFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(stage=stage)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/files')
    def list_files(self, request, project_pk=None, stage_name=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)
        
        files = stage.files.all()
        serializer = ProjectFileSerializer(files, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='projects/(?P<project_pk>[^/.]+)/stages/(?P<stage_name>[^/.]+)/files/(?P<file_pk>[^/.]+)')
    def delete_file(self, request, project_pk=None, stage_name=None, file_pk=None):
        stage = self.get_stage(project_pk, stage_name)
        if stage is None:
            return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            file = stage.files.get(pk=file_pk)
        except ProjectFile.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        file.delete()
        return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics, status
from rest_framework.response import Response
from .models import ProjectStage
from .serializers import ProjectStageSerializer

class ProjectStageListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectStageSerializer

    def get_queryset(self):
        return ProjectStage.objects.filter(project_id=self.kwargs['project_id'])

class ProjectStageUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectStageSerializer
    lookup_field = 'stage'

    def get_queryset(self):
        return ProjectStage.objects.filter(project_id=self.kwargs['project_id'])

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.completed = request.data.get('completed', instance.completed)
        instance.save()
        return Response(self.get_serializer(instance).data)


class AdminUserListView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        admin_users = CustomUser.objects.filter(is_admin=True)
        serializer = UserSerializer(admin_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteAdminView(APIView):
    permission_classes = (permissions.AllowAny,)

    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id, is_admin=True)
        if user == request.user:
            return Response({"error": "You cannot delete your own admin account."}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"message": "Admin user deleted successfully."}, status=status.HTTP_200_OK)