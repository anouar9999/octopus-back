from django.urls import path, include
from rest_framework import routers
from .views import (
    RegisterView, LoginView, CompanyUpdateAPIView, CompanyDeleteAPIView,
    TaskListCreateAPIView, TaskDeleteAPIView, CommentDeleteAPIView, CompanyListAPIView,
     CompanyCreateAPIView, CompanyDetailView, TaskUpdateView, TaskIsDoneUpdateView,
    CommentCreateView, ProjectCreateAPIView2,
    ProjectListAPIView, ProjectDeleteAPIView, ProjectUpdateAPIView, ProjectDetailAPIView, CommentListAPIView,
    ReplyDeleteAPIView, CategoryViewSet, CompanyCategoriesList, SubCategoryViewSet, CityViewSet, RegionViewSet, CategoryDetailAPIView,
    CategoryUpdateAPIView, SubCategoryRetrieveAPIView, SubCategoryUpdateAPIView, CityRetrieveAPIView, CityUpdateAPIView,ProjectImageCommentListCreateView,
    RegionRetrieveAPIView, RegionUpdateAPIView, CompanyCreateAPIView,ProjectImageCommentReplyView,ProjectImageCommentDetailView,ProjectImageCommentListCreateView
)
from .views import (
    ProjectImageCommentListCreateView,ProjectStageUpdateView,
    ProjectImageCommentDetailView,AdminUserListView,
    ProjectImageCommentReplyView,ProjectStageListView,CompanyDetailView,DeleteAdminView
)
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectStageViewSet,ProjectStageFilesViewSet

router = DefaultRouter()
# router.register(r'projects', ProjectViewSet)
router.register(r'stages', ProjectStageViewSet)
project_stage_list = ProjectStageViewSet.as_view({
    'post': 'upload_image',
    'get': 'list_images',
    'delete': 'delete_image'  # Add delete action here
})
project_files_stage_list = ProjectStageFilesViewSet.as_view({
    'post': 'upload_file',
    'get': 'list_files',
    'delete': 'delete_file'  # Add delete action here
})
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('projects/', ProjectListAPIView.as_view(), name='project-list'),
    path('projects/new/', ProjectCreateAPIView2.as_view(), name='project-create'),
    path('projects/delete/<int:pk>/', ProjectDeleteAPIView.as_view(), name='project-delete'),
    path('projects/update/<int:pk>/', ProjectUpdateAPIView.as_view(), name='project-update'),
    path('projects/<int:id>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('companies/', CompanyListAPIView.as_view(), name='company-list'),
    path('companies/create/', CompanyCreateAPIView.as_view(), name='company-create'),
    path('companies/<int:pk>/update/', CompanyUpdateAPIView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete/', CompanyDeleteAPIView.as_view(), name='company-delete'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('projects/<int:project_id>/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/is_done/', TaskIsDoneUpdateView.as_view(), name='task-is-done-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteAPIView.as_view(), name='delete_task'),
    path('projects/<int:project_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('projects/<int:project_id>/comments/add/', CommentCreateView.as_view(), name='comment-create'),
    path('projects/<int:project_id>/comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('projects/<int:project_id>/comments/<int:comment_id>/replies/<int:reply_id>/delete/', ReplyDeleteAPIView.as_view(), name='reply-delete'),
    path('categories/create/', CategoryViewSet.as_view({'post': 'create'}), name='category-create'),
    path('companies/<int:company_id>/categories/', CategoryViewSet.as_view({'post': 'create'}), name='category-create'),
    path('categories/by-company/<int:company_id>/', CategoryViewSet.as_view({'get': 'list_by_company'}), name='category-list-by-company'),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'delete': 'destroy'}), name='category-delete'),
    path('categories/<str:category_name>/subcategories/', SubCategoryViewSet.as_view({'post': 'create', 'get': 'list'}), name='subcategory-list-create'),
    path('categories/<str:category_name>/subcategories/<int:pk>/', SubCategoryViewSet.as_view({'delete': 'destroy'}), name='subcategory-delete'),
    path('subcategories/<str:subcategory_name>/cities/', CityViewSet.as_view({'post': 'create', 'get': 'list'}), name='city-list-create'),
    path('subcategories/<str:subcategory_name>/cities/<int:pk>/', CityViewSet.as_view({'delete': 'destroy'}), name='city-delete'),
    path('cities/<str:city_name>/regions/', RegionViewSet.as_view({'post': 'create', 'get': 'list'}), name='region-list-create'),
    path('cities/<str:city_name>/regions/<int:pk>/', RegionViewSet.as_view({'delete': 'destroy'}), name='region-delete'),
    path('categories/<int:category_id>/detail', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/update', CategoryUpdateAPIView.as_view(), name='category-detail'),
    path('subcategories/<int:subcategory_id>/', SubCategoryRetrieveAPIView.as_view(), name='subcategory-detail'),
    path('subcategories/<int:subcategory_id>/update/', SubCategoryUpdateAPIView.as_view(), name='subcategory-update'),
    path('cities/<int:city_id>/', CityRetrieveAPIView.as_view(), name='city-retrieve'),
    path('cities/<int:city_id>/update/', CityUpdateAPIView.as_view(), name='city-update'),
    path('regions/<int:region_id>/', RegionRetrieveAPIView.as_view(), name='region-retrieve'),
    path('regions/<int:region_id>/update/', RegionUpdateAPIView.as_view(), name='region-update'),
    path('projects/<int:project_pk>/stages/<str:stage_name>/upload_image/', project_stage_list, name='upload-image'),
    path('projects/<int:project_pk>/stages/<str:stage_name>/images/', project_stage_list, name='list-images'),
    path('projects/<int:project_pk>/stages/<str:stage_name>/images/<int:image_pk>/delete/', project_stage_list, name='delete-image'),  # URL for delete action
    path('projects/<int:project_pk>/stages/<str:stage_name>/upload_file/', project_files_stage_list, name='upload-file'),
    path('projects/<int:project_pk>/stages/<str:stage_name>/files/', project_files_stage_list, name='list-files'),
    path('projects/<int:project_pk>/stages/<str:stage_name>/files/<int:file_pk>/delete/', project_files_stage_list, name='delete-file'),  # URL for delete action
    path('project-images/<int:image_id>/comments/', ProjectImageCommentListCreateView.as_view(), name='project-image-comment-list-create'),
    path('project-image-comments/<int:pk>/', ProjectImageCommentDetailView.as_view(), name='project-image-comment-detail'),
    path('project-image-comments/<int:comment_id>/reply/', ProjectImageCommentReplyView.as_view(), name='project-image-comment-reply'),
     path('projects/<int:project_id>/stages/', ProjectStageListView.as_view(), name='project-stage-list'),
    path('projects/<int:project_id>/stages/<str:stage>/', ProjectStageUpdateView.as_view(), name='project-stage-update'),
    path('admin-users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('delete-admin/<int:user_id>/', DeleteAdminView.as_view(), name='delete-admin'),


]
