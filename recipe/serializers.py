from django.contrib.auth.models import User, Group
from rest_framework import serializers
from recipe.models import Recipe, Menu, Post
from rest_framework.reverse import reverse

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PolymorphicHyperlinkedIdentityField(serializers.HyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(PolymorphicHyperlinkedIdentityField, self).__init__(view_name, **kwargs)

    def use_pk_only_optimization(self):
        # We have the complete object instance already. We don't need
        # to run the 'only get the pk for this relationship' code.
        return False


    def get_url(self, obj, view_name, request, format):

        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}

        return self.reverse("{}-detail".format(obj.kind), kwargs=kwargs, request=request, format=format)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = PolymorphicHyperlinkedIdentityField(view_name='recipe-detail' )

    class Meta:
        model = Post
        fields = ('url', 'title', 'description', 'images', 'updated_at', 'kind')
        read_only_fields = ('title', 'description', 'images', 'updated_at', 'kind')

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'steps',
                  'images', 'portions', 'cost')


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Menu
        fields = ('title', 'description', 'images', 'collaborative',
                  'entries')
