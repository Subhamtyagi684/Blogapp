from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BlogSerializer, LoginSerializer, UserSerializer, CategorySerializer
from rest_framework.status import *
from django.contrib.auth import authenticate,login, logout
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Customer, Category, Blog
from django.http import *
from rest_framework import status
from .forms import RegisterationForm, BlogForm
import requests
from django.contrib import messages
from rest_framework.authentication import SessionAuthentication,BaseAuthentication,BasicAuthentication
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    blogs = Blog.objects.all().order_by('-updated_on')
    form = RegisterationForm
    if request.method=='POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            password = request.POST.get('password')
            myobj = {'full_name':full_name,'email':email,'mobile':mobile,'password':password}
            x = requests.post('http://localhost:8000/api/register/',data=myobj)
            if x.status_code>=200 and x.status_code<300:
                messages.add_message(request,messages.SUCCESS,'User created successfully',extra_tags='alert alert-success')
            elif x.status_code>300:
                messages.add_message(request,messages.ERROR,x.text,extra_tags='alert alert-danger')
            return redirect('home')
    return render(request,'home.html' ,{'form':form,'blogs':blogs})


def custlogin(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'You are logged in successfully')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR,'Email or password is not correct')
    return render(request,'login.html')


@login_required(login_url='/login/')
def custlogout(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'You were logged out successfully')
    return redirect('home')


@login_required(login_url='/login/')
def createblog(request):
    form = BlogForm
    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            blog = request.POST.get('blog')
            category = request.POST.get('category')
            newobj = Category.objects.get_or_create(name=category)
            custobj = Customer.objects.get(email=request.user.email)
            myobj = {'title':title,'blog':blog,'author':custobj.id,'category':newobj[0].id}
            x = requests.post('http://localhost:8000/api/createblog/',data=myobj)
            if x.status_code>=200 and x.status_code<300:
                messages.add_message(request,messages.SUCCESS,'User created successfully',extra_tags='alert alert-success')
            elif x.status_code>300:
                messages.add_message(request,messages.ERROR,x.text,extra_tags='alert alert-danger')
    return render(request,'createblog.html',{'form':form})


@login_required(login_url='/login/')
def updateblog(request,pk):
    blogobj = Blog.objects.get(id=pk)
    form = BlogForm(request.POST or None, initial={'title':blogobj.title,'blog':blogobj.blog,'category':blogobj.category})
    try:
        user_id = request.user.id
        userobj = Customer.objects.get(id=user_id)
    except:
        messages.add_message(request,messages.ERROR,'User not found')
        return render('login')
    if request.method=='POST':
        title = request.POST.get('title')
        blog = request.POST.get('blog')
        category = request.POST.get('category')
        newobj = Category.objects.get_or_create(name=category)
        myobj = {'title':title,'blog':blog,'author':userobj.id,'category':newobj[0].id}
        x = requests.post(f'http://localhost:8000/api/modifyblog/{pk}',data=myobj)
        if x.status_code>=200 and x.status_code<300:
                messages.add_message(request,messages.SUCCESS,'User created successfully',extra_tags='alert alert-success')
        elif x.status_code>300:
            messages.add_message(request,messages.ERROR,x.text,extra_tags='alert alert-danger')
    return render(request,'createblog.html',{'form':form})

@login_required(login_url='/login/')
def deleteblog(request,pk):
    try:
        blog = Blog.objects.get(id=pk)
        blog.delete()
        messages.add_message(request,messages.SUCCESS,'Blog deleted successfully')
    except:
        messages.add_message(request,messages.ERROR,'Blog not found')
    return redirect('my_blogs')


@login_required(login_url='/login/')
def myblogs(request):
    user_id = request.user.id
    try:
        userobj = Customer.objects.get(id=user_id)
        blogobj = Blog.objects.filter(author=userobj)
    except:
        messages.add_message(request,messages.ERROR,'User not found')
        return redirect('login')
    return render(request,'myblog.html',{'blogs':blogobj})  


class RegisterApi(APIView):
    serializer_class = UserSerializer
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'User created successfully'},status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


class LoginApi(APIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request,user)
            return Response('You were logged in successfully',status=HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        logout(request)
        return Response('You were logged out successfully')


class CreateBlog(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ModifyBlog(APIView):
    
    serializer_class = BlogSerializer

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Blog = self.get_object(pk)
        serializer = BlogSerializer(Blog)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        Blog = self.get_object(pk)
        serializer = BlogSerializer(Blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        Blog = self.get_object(pk)
        serializer = BlogSerializer(Blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Blog = self.get_object(pk)
        Blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CreateCat(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ModifyCat(APIView):
    
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Category = self.get_object(pk)
        serializer = CategorySerializer(Category)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        Category = self.get_object(pk)
        serializer = CategorySerializer(Category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        Category = self.get_object(pk)
        serializer = CategorySerializer(Category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Category = self.get_object(pk)
        Category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchBlog(APIView):

    def get(self, request,cat):
        catobj = Category.objects.filter(name=cat).first()
        if catobj:
            blogobj = Blog.objects.filter(category=catobj)
            serializer = BlogSerializer(instance=blogobj, many=True)
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response({'detail':'No category found,try another one'},status=HTTP_400_BAD_REQUEST)