from rest_framework import serializers

class PolymorphicHyperlinkedIdentityField(serializers.HyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(PolymorphicHyperlinkedIdentityField, self).__init__(view_name, **kwargs)

    def use_pk_only_optimization(self):
        return False


    def get_url(self, obj, view_name, request, format):

        if hasattr(obj, 'pk') and obj.pk in (None, ''):
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}

        return self.reverse("{}-detail".format(obj.kind), kwargs=kwargs, request=request, format=format)

