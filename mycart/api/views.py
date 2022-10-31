from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserProfileSerializer, UserRegistrationSerializer,UserLoginSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,CustomerSerializer,ProductSerializer,CartSerializer,OrderPlacedSerializer
from app.models import Customer,Product,Cart,OrderPlaced
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Check your email and tap on link to change your password'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed successfully'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# app views
class CustomerAPI(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            customer=Customer.objects.get(id=id)
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        customer=Customer.objects.all()
        serializer=CustomerSerializer(customer,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        id=pk
        customer=Customer.objects.get(pk=id)
        serializer=CustomerSerializer(customer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk,format=None):
        id=pk
        customer=Customer.objects.get(pk=id)
        serializer=CustomerSerializer(customer,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial_Data_Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        id=pk
        customer=Customer.objects.get(pk=id)
        customer.delete()
        return Response({'msg':'Data Deleted'})

class ProductAPI(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if pk is not None:
            product=Product.objects.get(id=id)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        product=Product.objects.all()
        serializer=ProductSerializer(product,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data_Created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        id=pk
        product=Product.objects.get(pk=id)
        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data_Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk,format=None):
        id=pk
        product=Product.objects.get(pk=id)
        serializer=ProductSerializer(product,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial_Data_Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        id=pk
        product=Product.objects.get(pk=id)
        product.delete()
        return Response({'msg':'Data_Deleted'},status=status.HTTP_200_OK)

class CartAPI(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None,format=None):
        id=pk
        if pk is not None:
            cart=Cart.objects.get(id=id)
            serializer=CartSerializer(cart)
            return Response(serializer.data)
        cart=Cart.objects.all()
        serializer=CartSerializer(cart,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk,format=None):
        id=pk
        print("id:",id)
        cart=Cart.objects.get(pk=id)
        serializer=CartSerializer(cart,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk,format=None):
        id=pk
        cart=Cart.objects.get(pk=id)
        serializer=CartSerializer(cart,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        id=pk
        cart=Cart.objects.get(pk=id)
        cart.delete()
        return Response({'msg':'data Deleted'},status=status.HTTP_200_OK)

class OrderPlacedAPI(APIView):
    def get(self,request,pk=None,format=None):
        id=pk
        if pk is not None:
            order=OrderPlaced.objects.get(id=id)
            serializer=OrderPlacedSerializer(order)
            return Response(serializer.data)
        order=OrderPlaced.objects.all()
        serializer=OrderPlacedSerializer(order,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer=OrderPlacedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk,format=None):
        id=pk
        order=OrderPlaced.objects.get(pk=id)
        serializer=OrderPlacedSerializer(order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk,format=None):
        id=pk
        order=OrderPlaced.objects.get(pk=id)
        serializer=OrderPlacedSerializer(order,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Partial Data Updated'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        id=pk
        order=OrderPlaced.objects.get(pk=id)
        order.delete()
        return Response({'msg':'Data Deleted'},status=status.HTTP_200_OK)