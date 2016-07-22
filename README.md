# multinestedviewset
multi nested viewset in django rest framework

### Install drf
 - https://pypi.python.org/pypi/drf-nested-routers


### See common/viewsets.py

```sh
from django.http.response import Http404
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class MultiNestedMixinHelper():
    def get_multi_nested_filter(self, parent, filter_dict, limit_count):
        try:
            if parent.parent_lookup_field or limit_count < 0:
                limit_count = limit_count - 1
                identifier = '{0}_{1}'.format(parent.parent_lookup_field, parent.lookup_field)
                identifier_pk = self.kwargs[identifier]
                parent_object = parent.parent_object.objects.get(**{parent.parent.lookup_field:identifier_pk})
                filter_dict.update({parent.parent_lookup_field:parent_object})
                self.get_multi_nested_filter(parent.parent, filter_dict, limit_count)
            return filter_dict
        except AttributeError:
            return filter_dict
        except:
            raise Http404


class MultiNestedCreateModelMixin(mixins.CreateModelMixin, MultiNestedMixinHelper):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        filter_dict = self.get_multi_nested_filter(self, {}, 20)
        serializer.save(**filter_dict)


class MultiNestedUpdateModelMixin(object, MultiNestedMixinHelper):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        filter_dict = self.get_multi_nested_filter(self, {}, 20)
        pk = kwargs.get('pk', None)
        if pk is not None:
            filter_dict.update({'pk': pk})
        instance = self.filter_queryset(self.get_queryset().filter(**filter_dict))
        if len(instance) < 1:
            raise Http404
        serializer = self.get_serializer(instance[0], data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class MultiNestedListModelMixin(object, MultiNestedMixinHelper):
    def list(self, request, *args, **kwargs):
        filter_dict = self.get_multi_nested_filter(self, {}, 20)
        queryset = self.filter_queryset(self.get_queryset().filter(**filter_dict))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MultiNestedModelViewSet(MultiNestedCreateModelMixin,
                              mixins.RetrieveModelMixin,
                              MultiNestedUpdateModelMixin,
                              MultiNestedListModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    pass
```

