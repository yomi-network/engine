from django.contrib.auth.models import User, Group
from rest_framework import serializers
from recipe.models import Recipe, Menu, Post
from recipe.fields import PolymorphicHyperlinkedIdentityField
from rest_framework.reverse import reverse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-detail'
    )

    menus = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='menu-detail'
    )


    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'recipes', 'menus')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = PolymorphicHyperlinkedIdentityField(view_name='recipe-detail' )
    owner = serializers.ReadOnlyField(source='my_lord.username')

    class Meta:
        model = Post
        fields = ('url', 'title', 'description', 'images', 'updated_at', 'kind', 'owner')
        read_only_fields = ('title', 'description', 'images', 'updated_at', 'kind')


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        owner = serializers.ReadOnlyField(source='owner.username')
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'steps',
                  'images', 'portions', 'cost', 'owner')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Menu
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('title', 'description', 'images', 'collaborative',
                  'entries', 'owner')
