from django.conf.urls import url, include
from rest_framework_nested import routers
from account import views
from nestedthing.views import NestedThingViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

nested_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
nested_router.register(r'nestedthings', NestedThingViewSet, base_name='nestedthing')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(nested_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# drf-nested-routers==0.11.1