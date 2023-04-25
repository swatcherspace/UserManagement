
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
from UserManagement.settings import PORTFORLIOMGMT
import time
from .utils import get_symbols
NSE_MAPPING= get_symbols("NSE")
NYSE_MAPPING= get_symbols("NYSE")
class GetPortfolioViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPortfolioSerializer
    queryset = UserPortfolio.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)
    
    # def get_stock_from_name(name):
    #     for key, val in NSE_MAPPING[0].items():
            
    
    def create(self, request):
        try:
            id = request.data.get("user_id", None)
            name = request.data.get("name", None)
            if id is None or name is None:
                return Response(data={"data":{},'message':'',"status":400}, status=status.HTTP_400_BAD_REQUEST) 
            try:
                user_obj = User.objects.get(id=id)
            except Exception as e:
                return Response(data={"data": e,'message':"User doesn't exists","status":400}, status=status.HTTP_400_BAD_REQUEST) 
            
            #Create the PortfolioData only in casee when user exists in user table
            UserPortfolio.objects.create(
                user_id = user_obj,
                name = name
            )
            # Serialized data back to caller
            serializer = UserPortfolioSerializer(data = {"user_id": user_obj.id, "name": name})
            if serializer.is_valid():    
                return Response({
                                    'data': serializer.data,
                                    'status': status.HTTP_200_OK,
                                    'message': 'Created User Successfully'
                                }, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
                return Response(data={"data": e,'message':"Something Went Wrong","status":500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def retrieve(self, request, pk=None):
        try:
            
            user_obj = User.objects.filter(id=pk).first()
            user_obj = UserPortfolio.objects.filter(user_id=user_obj.id)
            serialized_data = UserPortfolioSerializer(user_obj, many=True)
            
            return Response({
                                'data': serialized_data.data,
                                'status': status.HTTP_200_OK,
                                'message': 'Created User Successfully'
                            }, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
                return Response(data={"data": e,'message':"Something Went Wrong","status":500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
class UserOnboardingViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)
    
    #Used to create USER with minimum required credentials
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

    

class StockViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)

    # Create stocks based on a particular user_id
    def retrieve(self, request, pk=None):
        try:
            user_obj = UserPortfolio.objects.filter(user_id=pk)
            serialized_data = UserPortfolioSerializer(user_obj, many=True)
            stocks = [user_stocks["name"] for user_stocks in serialized_data.data]
            resp = []
            for stock in stocks:
                url = [PORTFORLIOMGMT+'create-stock?name='+stock,PORTFORLIOMGMT+'/create-fundamentals?name='+stock]
                payload = {}
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                resp.append([requests.post(url, data=payload, headers=headers) for url in url])
            return Response({
                                'data': resp,
                                'status': status.HTTP_200_OK,
                                'message': 'Created User Successfully'
                            }, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
                return Response(data={"data": e,'message':"Something Went Wrong","status":500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    # Retrieve stocks based on names
    def list(self, request):
        try:
            stocks = request.data.get("stocks", None)
            resp = []
            for stock in stocks:
                stock_by_name_url = PORTFORLIOMGMT+'get-stock-by-name?name='+stock
                fundamentals_by_name_url = PORTFORLIOMGMT+'get-fundamentals-by-name?name='+stock
                payload = {}
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                resp.append([requests.get(stock_by_name_url, data=payload, headers=headers).json(),
                             requests.get(fundamentals_by_name_url, data=payload, headers=headers).json()])
            return Response({
                                'data': resp,
                                'status': status.HTTP_200_OK,
                                'message': 'Created User Successfully'
                            }, status=status.HTTP_200_OK, content_type="application/json")

        except Exception as e:
            return Response(data={"data": e,'message':"Something Went Wrong","status":500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

             
              
             
             
        