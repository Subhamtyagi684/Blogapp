from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('login/',views.custlogin,name='login'),
    path('logout/',views.custlogout, name='logout'),
    path('createblog/',views.createblog, name='create-blog'),
    path('myblogs/',views.myblogs, name='my_blogs'),
    path('updateblog/<int:pk>',views.updateblog, name='update_blog'),
    path('deleteblog/<int:pk>',views.deleteblog, name='delete_blog'),
    path('api/register/',views.RegisterApi.as_view(),name='registerapi'),
    path('api/login/',views.LoginApi.as_view(),name='loginapi'),
    path('api/logout/',views.LogoutApi.as_view(), name='logoutapi'),
    path('api/createcat/',views.CreateCat.as_view(),name='create_category'),
    path('api/modifycat/<int:pk>',views.ModifyCat.as_view(),name='modify_category'),
    path('api/createblog/',views.CreateBlog.as_view(),name='create_blog'),
    path('api/modifyblog/<int:pk>',views.ModifyBlog.as_view(),name='modify_blog'),
    path('api/searchblog/<str:cat>',views.SearchBlog.as_view(), name='search_blog')

]
