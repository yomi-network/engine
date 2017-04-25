from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.core import  serializers
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from recipe.models import Recipe, Menu, Post
from recipe.serializers import (UserSerializer, GroupSerializer,
                                RecipeSerializer, MenuSerializer, PostSerializer)
from recipe.permissions import IsOwnerOrReadOnly, EditOnlyCurrentUserOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    Api endpoint that allows users to be viewed or edited
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UsernameView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    permission_classes = (EditOnlyCurrentUserOrReadOnly,)
    def get_object(self, username):
        try:
            return User.objects.get(username=username.rstrip('/'))
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):

        username = self.kwargs['username']
        user = self.get_object(username)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, format=None):
        user = self.get_object(username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeRecipes(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Recipe.objects.filter(owner__pk = self.request.user.pk)
    serializer_class = RecipeSerializer


class MeMenus(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Menu.objects.filter(owner__pk = self.request.user.pk)
    serializer_class = MenuSerializer


class UserRecipes(generics.ListAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def get_queryset(self):
        username = self.kwargs['username']
        return Recipe.objects.filter(owner__username = username)
    serializer_class = RecipeSerializer


class UserMenus(generics.ListAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def get_queryset(self):
        username = self.kwargs['username']
        return Menu.objects.filter(owner__username = username)
    serializer_class = MenuSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that  allows groups to be viewed or edited
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET'])
def index(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
