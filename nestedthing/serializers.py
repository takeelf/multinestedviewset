from rest_framework import serializers
from nestedthing.models import NestedThing


class NestedThingSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = NestedThing
        fields = ('id',
                  'user_id',
                  'nested_name')

