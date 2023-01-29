
from django_filters import rest_framework as filters
from django.db.models import Q, F
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
import requests
import json
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import traceback
# custom packages
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import *
from .models import *

class GetPortfolioViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPortfolioSerializer
    queryset = UserPortfolio.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)

    def create(self, request):
        id = request.data.get("user_id", None)
        name = request.data.get("name", None)
        if id is None or name is None:
            return Response(data={"data":{},'message':'',"status":400}, status=status.HTTP_400_BAD_REQUEST) 
        
        user_obj = User.objects.get(id=id)
        print(id,user_obj)
        #Create the PortfolioData
        UserPortfolio.objects.create(
            stock_id = user_obj,
            name = request.data.get("name", None)
        )
        serializer = UserPortfolioSerializer(data = {"stock_id": user_obj.id, "name": request.data.get("name", None)})
        if serializer.is_valid():    
            return Response({
                                'data': serializer.data,
                                'status': status.HTTP_200_OK,
                                'message': 'Created User Successfully'
                            }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user_obj = User.objects.filter(id=pk).first()
        user_obj = UserPortfolio.objects.filter(stock_id=user_obj.id)
        serialized_data = UserPortfolioSerializer(user_obj, many=True)
        return Response({
                            'data': serialized_data.data,
                            'status': status.HTTP_200_OK,
                            'message': 'Created User Successfully'
                        }, status=status.HTTP_200_OK)

class UserOnboardingViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)
    
    #Used to create USER
    def create(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.email_id = request.data.get("email_id", None)
                serializer.is_active = request.data.get('is_active', None)
                serializer.staff = request.data.get('staff', None)
                serializer.admin = request.data.get('admin', None)
                obj = serializer.save()
                return Response({
                                'data': obj.id,
                                'status': status.HTTP_200_OK,
                                'message': 'Created User Successfully'
                            }, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(data={"data":{},'message':e,"status":400}, status=status.HTTP_400_BAD_REQUEST)

    

