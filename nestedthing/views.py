from django.contrib.auth.models import User
from account.views import UserViewSet
from common.viewsets import MultiNestedModelViewSet
from nestedthing.models import NestedThing
from nestedthing.serializers import NestedThingSerializer


class NestedThingViewSet(MultiNestedModelViewSet):
    parent = UserViewSet
    parent_lookup_field = 'user'
    parent_object = User
    queryset = NestedThing.objects.all()
    serializer_class = NestedThingSerializer

