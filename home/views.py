from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

# Create your views here.

class Operation1(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if(serializer.is_valid()):
            email=serializer.validated_data['email']
            if(User.objects.filter(email=email).exists()):
                return Response("Already Existed", status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Operation2(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        try:
            user1=User.objects.get(username=username)
            if(user1.check_password(password)):
                refresh = RefreshToken.for_user(user1)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            return Response("Invalid Password", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        
class Operation3(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=InventorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Operation4(APIView):
    permission_classes=[IsAuthenticated]

    def patch(self,request,pk):
        try:
            item=Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response("Invalid Product",status=status.HTTP_404_NOT_FOUND)
        serializer=InventorySerializer(item,data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            item=Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response("deleted",status=status.HTTP_204_NO_CONTENT)
    
    def get(self,request,pk):
        try:
            item=Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        serializer=InventorySerializer(item)
        return Response(serializer.data,status=status.HTTP_200_OK)