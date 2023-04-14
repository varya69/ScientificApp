from rest_framework.views import APIView
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from user import models
from user.models import Product, User, Seller
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from user.serializers import CustomTokenObtainPairSerializer, ProductSerializer

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]

#     def login(self, request, format=None):
#         content = {'message': 'This is a protected endpoint.'}
#         return Response(content)


@csrf_exempt
def sellerLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data\n")
        print(data)
        seller = Seller.objects.filter(SellerEmail=data['SellerEmail'], password=data['password']).first()
        if seller is not None:
            # create a session to keep the user logged in
            # request.session['seller_id'] = seller.id
            return JsonResponse({'message': 'Login successful', 'SellerName': seller.SellerName, 'SellerId': seller.SellerId})
        else:
            return JsonResponse({'error': 'Invalid login credentials'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
def userLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("data\n")
        print(data)
        user = User.objects.filter(UserEmail=data['UserEmail'], password=data['password']).first()
        print("\nuser:", user)
        if user is not None:
            # create a session to keep the user logged in
            # request.session['seller_id'] = seller.id
            return JsonResponse({'message': 'Login successful', 'UserName': user.UserName, 'UserId': user.UserId})
        else:
            return JsonResponse({'error': 'Invalid login credentials'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})



@require_GET
def search(request):
    if request.method == 'GET':
        search_term = request.GET.get('search')
        products = Product.objects.filter(
            Q(ProductName__icontains=search_term) | Q(Description__icontains=search_term)
        )
        results = []
        for product in products:
            result = {
                "id": product.id,
                "ProductName": product.ProductName,
                "Description": product.Description,
                "Category": product.Category,
                "Price": product.Price,
                "quantity": product.quantity,
                "image": product.image.url if product.image else None
                }
            results.append(result)

        return JsonResponse({ 'results': results })

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User(
            UserName=data['UserName'],
            UserEmail=data['UserEmail'],
            mobileNo=data['mobileNo'],
            password=data['password'],
        )
        user.save()
        return JsonResponse({'message': 'User created successfully', 'UserName': user.UserName, 'UserId': user.UserId})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_list = []
        for user in users:
            user_dict = {
                'UserId': user.UserId,
                'UserName': user.UserName,
                'UserEmail': user.UserEmail,
                'mobileNo': user.mobileNo,
                'password': user.password,
            }
            users_list.append(user_dict)
        return JsonResponse(users_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})

@csrf_exempt
def update_user(request, user_id):
    try:
        user = User.objects.get(UserId=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    if request.method == 'PUT':
        data = json.loads(request.body)
        user.UserName = data.get('SellerName', user.UserName)
        user.UserEmail = data.get('SellerEmail', user.UserEmail)
        user.mobileNo = data.get('mobileNo', user.mobileNo)
        user.password = data.get('password', user.password)
        user.save()
        return JsonResponse({'message': 'User updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})
