from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets, filters
from .models import Task, Sprint
from .serializers import TaskSerializer, SprintSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .forms import TaskFilter, SprintFilter


User = get_user_model()


class DefaultMixin(object):
    authentication_class = (
        authentication.BaseAuthentication,
        authentication.TokenAuthentication,
    )
    permissions_classes = (
        permissions.IsAuthenticated
    )
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )


class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    filter_class = SprintFilter
    search_fields = ('name',)
    ordering_fields = ('end', 'name')


class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'order', 'started', 'due', 'completed')


class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = (User.USERNAME_FIELD)
# Create your views here.
