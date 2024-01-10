from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from movies_database.permissions import IsOwnerOrStaffOrReadOnly
from .models import Account
from .serializers import CurrentUserInfoSerializer


class UsersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = CurrentUserInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    pagination_class = UsersPagination

    def get_queryset(self):
        exclude_users_arr = []
        try:
            exclude_users = self.request.query_params.get('exclude')
            if exclude_users:
                user_ids = exclude_users.split(',')
                for user_id in user_ids:
                    exclude_users_arr.append(int(user_id))
        except:
            return []
        queryset = super().get_queryset().exclude(id__in=exclude_users_arr)
        return queryset
