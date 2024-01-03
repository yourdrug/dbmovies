from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from .models import Account
from .serializers import CurrentUserInfoSerializer


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = CurrentUserInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
