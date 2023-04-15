from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.parsers import JSONParser
from django.http import Http404, JsonResponse
from .forms import ProductForm, UploadImageForm
from rest_framework import status
from django.contrib.auth.decorators import login_required
import chardet

import json
from user.models import Cart, Product, User, Seller
from user.serializers import UserSerializer, SellerSerializer, ProductSerializer

# Api methods for the user and seller models
# @csrf_exempt 
# def userApi(request, id=0):
#     if request.method == 'GET':     #if the API method is GET 
#         user = User.objects.all()
#         user_serializer = UserSerializer(user, many = True)
#         return JsonResponse(user_serializer.data, safe=False)
#     elif request.method == 'POST':  #If the API method is POST
#         user_data = JSONParser().parse(request) #Get the data from the JSON parser object and return it as a string object
#         user_serializer = UserSerializer(data = user_data) #Then user serializes to convert it into model type object 
#         if user_serializer.is_valid(): #If the model is valid we save into the database
#             user_serializer.save()
#             return JsonResponse("User Added Successfully!!!", safe=False)
#         else:
#             return JsonResponse("Failed to Add User", safe=False)
    
#     elif request.method == "PUT":   #Update the existing user
#         user_data = JSONParser().parse(request)
#         user = User.objects.get(UserId=user_data['UserId'])
#         user_serializer = UserSerializer(user , data = user_data)
#         if user_serializer.is_valid(): #If the model is valid we save into the database
#             user_serializer.save()
#             return JsonResponse("User Updated Successfully!!!", safe=False)
#         else:
#             return JsonResponse("Failed to Update User", safe=False)
    
#     elif request.method == "DELETE":   #Update the existing user
#         user = User.objects.get(UserId=id)
#         user.delete()
#         return JsonResponse("Deleted User Successfully", safe=False) 

# @csrf_exempt
# def seller_api(request, id=0):
#     print(request)
#     if request.method == 'GET':
#         sellers = Seller.objects.all()
#         seller_serializer = SellerSerializer(sellers, many=True)
#         return JsonResponse(seller_serializer.data, safe=False)
#     elif request.method == 'POST':
#         print("in here")
#         seller_data = JSONParser().parse(request)
#         print("\n", seller_data)
#         seller_serializer = SellerSerializer(data=seller_data)
#         print()
#         print(seller_serializer)
#         print()
#         print(seller_serializer.is_valid())
#         if seller_serializer.is_valid():
#             print("valid")
#             seller_serializer.save()
#             return JsonResponse("Seller added successfully!", safe=False)
#         else:
#             print(" not valid")
            
#             return JsonResponse("Failed to add seller", safe=False)
#     elif request.method == 'PUT':
#         seller_data = JSONParser().parse(request)
#         seller = Seller.objects.get(SellerId=seller_data['SellerId'])
#         seller_serializer = SellerSerializer(seller, data=seller_data)
#         if seller_serializer.is_valid():
#             seller_serializer.save()
#             return JsonResponse("Seller updated successfully!", safe=False)
#         else:
#             return JsonResponse("Failed to update seller", safe=False)
#     elif request.method == 'DELETE':
#         seller = Seller.objects.get(SellerId=id)
#         seller.delete()
#         return JsonResponse("Seller deleted successfully!", safe=False)

@csrf_exempt
def create_seller(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        seller = Seller(
            SellerName=data['SellerName'],
            SellerEmail=data['SellerEmail'],
            mobileNo=data['mobileNo'],
            password=data['password'],
        )
        seller.save()
        return JsonResponse({'message': 'Seller created successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
def get_sellers(request):
    if request.method == 'GET':
        sellers = Seller.objects.all()
        sellers_list = []
        for seller in sellers:
            seller_dict = {
                'SellerId': seller.SellerId,
                'SellerName': seller.SellerName,
                'SellerEmail': seller.SellerEmail,
                'mobileNo': seller.mobileNo,
                'password': seller.password,
            }
            sellers_list.append(seller_dict)
        return JsonResponse(sellers_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})

@csrf_exempt
def update_seller(request, seller_id):
    try:
        seller = Seller.objects.get(SellerId=seller_id)
    except Seller.DoesNotExist:
        raise Http404("Seller does not exist")

    if request.method == 'PUT':
        data = json.loads(request.body)
        seller.SellerName = data.get('SellerName', seller.SellerName)
        seller.SellerEmail = data.get('SellerEmail', seller.SellerEmail)
        seller.mobileNo = data.get('mobileNo', seller.mobileNo)
        seller.password = data.get('password', seller.password)
        seller.save()
        return JsonResponse({'message': 'Seller updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})

@csrf_exempt
def delete_seller(request, seller_id):
    try:
        seller = Seller.objects.get(SellerId=seller_id)
    except Seller.DoesNotExist:
        raise Http404("Seller does not exist")

    if request.method == 'DELETE':
        seller.delete()
        return JsonResponse({'message': 'Seller deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'})

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok'})
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage



@csrf_exempt
def add_product(request, id):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # check if a file was uploaded
            if 'image' in request.FILES:
                image = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                uploaded_file_url = fs.url(filename)
                seller = Seller.objects.get(SellerId=id)
                # create a new product with the uploaded image and seller ID
                product = Product(
                    ProductName=form.cleaned_data['ProductName'],
                    Description=form.cleaned_data['Description'],
                    Category=form.cleaned_data['Category'],
                    Price=form.cleaned_data['Price'],
                    quantity=form.cleaned_data['quantity'],
                    image=uploaded_file_url,
                    seller=seller,
                    productId=form.cleaned_data['productId'],

                )
                product.save()
                return JsonResponse({'success': True, 'message': 'Product added successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'No file was uploaded.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'success': False, 'message': 'This endpoint only accepts POST requests.'})


# @login_required
@csrf_exempt
def product_list(request, id):
    # seller = request.user.seller
    if request.method == 'GET':
        products = Product.objects.filter(seller=id)
        # products = Product.objects.all()
        product_list = []
        for product in products:
            product_dict = {
                "id": product.id,
                "ProductName": product.ProductName,
                "Description": product.Description,
                "Category": product.Category,
                "Price": product.Price,
                "quantity": product.quantity,
                "image": product.image.url if product.image else None,
                "productId": product.productId,
            }
            product_list.append(product_dict)
        return JsonResponse(product_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})
    

@csrf_exempt
def delete_product(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'})
    
@csrf_exempt
def get_product(request, id):
    try:
        if request.method == 'GET':
            product = Product.objects.get(pk = id)
            product_details = {
                "id": product.id,
                "ProductName": product.ProductName,
                "Description": product.Description,
                "Category": product.Category,
                "Price": product.Price,
                "quantity": product.quantity,
                "image": product.image.url if product.image else None,
                "productId": product.productId,

            }
            return JsonResponse(product_details, status=200, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found.'}, status=404)
    

@csrf_exempt
def update_product(request, id):
    print(request.body)
    try:
        product = Product.objects.get(pk = id)

    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    if request.method == 'PUT':
        data = json.loads(request.body)
        # Detect encoding of request.body bytes
        # try:
        #     data = json.loads(request.body.decode('utf-8', 'replace'))  # Decode request body with 'replace' error handler
        # except json.JSONDecodeError as e:
        #     return JsonResponse({'error': 'Invalid JSON data'})

        # serializer = ProductSerializer(product, data=request.data)

        # input_encoding = chardet.detect(request.body)['encoding']
        # Decode request.body bytes using detected encoding
        # data = json.loads(request.body.decode(input_encoding))
        # print("in here", data)
        product.ProductName = data.get('ProductName', product.ProductName)
        product.Description = data.get('Description', product.Description)
        product.Category = data.get('Category', product.Category)
        product.Price = data.get('Price', product.Price)
        product.quantity = data.get('quantity', product.quantity)
        product.productId = data.get('productId', product.productId)

        # if 'image' in request.FILES:
        #     print("\n\n\n\n\n\n")
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(image=request.FILES['image'])
        # else:
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()

        # if 'image' in request.FILES:
        #     print("in here")
        #     image = request.FILES['image']
        #     fs = FileSystemStorage()
        #     filename = fs.save(image.name, image)
        #     uploaded_file_url = fs.url(filename)
        #     product.image = uploaded_file_url

        # if 'image' in data:
        #     image = data['image']
        #     fs = FileSystemStorage()
        # filename = fs.save(image.name, image)
        # uploaded_file_url = fs.url(filename)
        # product.image = uploaded_file_url

        product.save()

        return JsonResponse({'message': 'Product updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})
    
@csrf_exempt
def all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        # products = Product.objects.all()
        product_list = []
        for product in products:
            product_dict = {
                "id": product.id,
                "ProductName": product.ProductName,
                "Description": product.Description,
                "Category": product.Category,
                "Price": product.Price,
                "quantity": product.quantity,
                "image": product.image.url if product.image else None,
                "productId": product.productId,
            }
            product_list.append(product_dict)
        return JsonResponse(product_list, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})
    
    