from django.shortcuts import render
from rest_framework import generics, permissions

from accounts.models import User
from accounts.api.serializers import UserSerializer

class UserListCreateView(generics.ListCreateAPIView):
    '''API view to list and create users'''

    permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''API view to retrieve, update, or delete a user'''

    permission_classes = [permissions.IsAdminUser]

    serializer_class = UserSerializer

    def get_queryset(self):
        '''Return the queryset for the user detail view'''

        return User.objects.filter(username=self.kwargs['username'])
    
    lookup_field = 'username'
    lookup_url_kwarg = 'username'