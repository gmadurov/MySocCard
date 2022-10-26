import json
import os

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from purchase.models import Category, Order, Product, Purchase
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Holder

from .serializers import (
    CategorySerializer,
    HolderSerializer,
    ProductSerializer,
    PurchaseSerializer,
)

API_URL = "/api/"


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated:
            if u.groups.filter(name__in=group_names):
                return True
        return False

    return user_passes_test(in_groups, login_url="403")


def safe_json_decode(response):
    if response.status_code == 500:
        raise Exception("500")
    # elif response.status_code == 400:
    #     raise Exception("400")
    # elif response.status_code == 401:
    #     raise Exception("401")
    else:
        try:
            return response, response.json()
        except json.decoder.JSONDecodeError:
            raise Exception("500", "Ledenbase response not readable or empty")


@api_view(["GET", "POST"])
def getRoutes(request):
    routes = [
        {"POST": API_URL + "login/"},
        {"GET": API_URL + "purchase/"},
        {"POST": API_URL + "purchase/"},
        {"GET": API_URL + "purchase/id"},
        {"PUT": API_URL + "purchase/id"},
        {"DELETE": API_URL + "purchase/id"},
        {"GET": API_URL + "product/"},
        {"POST": API_URL + "product/"},
        {"GET": API_URL + "product/id"},
        {"PUT": API_URL + "product/id"},
        {"DELETE": API_URL + "product/id"},
        {"GET": API_URL + "holders/"},
        {"POST": API_URL + "holders/"},
        {"GET": API_URL + "holders/id"},
        {"PUT": API_URL + "holders/id"},
        {"DELETE": API_URL + "holders/id"},
    ]
    return Response(routes)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def showProducts(request):
    data = request.data
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = ProductSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def showProduct(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)
    if request.method == "GET":
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    if request.method == "PUT":
        product.price = data["price"] or None
        product.name = data["name"] or None
        product.save()
    if request.method == "DELETE":
        product.delete()
        return Response()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def showPurchases(request):
    data = request.data
    if request.method == "GET":
        holder = request.user.holder
        purschases = holder.purchases.all()  # Purchase.objects.all()
        user = Holder.objects.get(user=request.user)
        purchases = user.purchases.all()
        serializer = PurchaseSerializer(purschases, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        purchase = Purchase.objects.create(
            buyer=Holder.objects.get(id=data["buyer"]),
            payed=data["payed"] or False,
        )
        if data["orders"]:

            orders = [
                Order.objects.get_or_create(
                    quantity=order["quantity"],
                    product=Product.objects.get(id=order["product"]),
                )
                for order in data["orders"]
            ]
            # print([order[1] for order in orders])
            purchase.orders.set([order[0] for order in orders])
        else:
            purchase.orders.set([])
        purchase.save()
        serializer = PurchaseSerializer(purchase, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def showPurchase(request, pk):
    data = request.data
    purschase = Purchase.objects.get(id=pk)
    if request.method == "GET":
        serializer = PurchaseSerializer(purschase, many=False)
        return Response(serializer.data)
    if request.method == "PUT":
        purschase.buyer = data["buyer"] or None
        purschase.products = data["products"] or None
        purschase.save()
    if request.method == "DELETE":
        purschase.delete()
        return Response()
    serializer = PurchaseSerializer(purschase, many=False)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def showHolders(request):
    data = request.data
    if request.method == "GET":
        if "search" in data.keys():
            search = data["search"]
            users = User.objects.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search)
            ).distinct()
            holders = [user.holder for user in users]
        else:
            holders = Holder.objects.all()
        serializer = HolderSerializer(holders, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        if "search" in data.keys():
            search = data["search"]
            users = (
                User.objects.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search)
                ).distinct()
                if (data["search"])
                else User.objects.all()
            )
            holders = [user.holder for user in users]
            serializer = HolderSerializer(holders, many=True)
        else:
            holder = Holder.objects.create()
            serializer = HolderSerializer(holder, many=False)
        return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def showHolder(request, pk):
    data = request.data
    holder = Holder.objects.get(id=pk)
    if request.method == "GET":
        serializer = HolderSerializer(holder, many=False)
        return Response(serializer.data)
    if request.method == "PUT":
        holder.stand = data["stand"] or None
        holder.save()
    if request.method == "DELETE":
        holder.delete()
        return Response()
    serializer = HolderSerializer(holder, many=False)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def cateories(request):
    data = request.data
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        categorie = Category.objects.create()
        serializer = CategorySerializer(categorie, many=False)
        return Response(serializer.data)


def loginLedenbase(request):
    res, ledenbaseUser = safe_json_decode(
        requests.post(
            os.environ.get("BACKEND_URL") + "/v2/login/",
            json={
                "password": request.data["password"],
                "username": request.data["username"],
            },
        )
    )
    if res.status_code != 200:
        return Response(
            data=ledenbaseUser,
            status=res.status_code,
        )

    user, created = User.objects.get_or_create(
        username=request.data["username"],
        first_name=ledenbaseUser["user"]["first_name"],
        last_name=ledenbaseUser["user"]["last_name"],
        # user purposely doesnt have a password set here to make sure it
    )
    holder, created = Holder.objects.get_or_create(
        user=user,
    )
    holder.ledenbase_id = ledenbaseUser["user"]["id"]
    holder.image_ledenbase = (
        os.environ.get("BACKEND_URL") + ledenbaseUser["user"]["photo_url"]
    )
    holder.save()
    return user


@api_view(["POST"])
def LoginAllUsers(request):
    user1 = User.objects.filter(username=request.data["username"])
    if user1.exists() and user1.filter(holder__ledenbase_id=0).exists():
        # print("user exists and doesnt have ledenbase id")
        user = authenticate(
            password=request.data["password"],
            username=request.data["username"],
        )
    else:
        user = loginLedenbase(request)

    refresh = RefreshToken.for_user(user)
    response = {"refresh": str(refresh), "access": str(refresh.access_token)}

    return Response(response)
