from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.views import loginAllUsers
from users.models import Card, Holder, Personel, WalletUpgrades
from django.shortcuts import get_object_or_404

from .serializers import CardSerializer, HolderSerializer, WalletUpgradesSerializer

from .views import DatabaseView


class HolderView(DatabaseView):
    model = Holder
    serializer = HolderSerializer
    http_method_names = ["get"]
    search_fields = ["user__first_name__icontains", "user__username__icontains", "user__last_name__icontains", "ledenbase_id", "id"]


# make wallet upgrades api


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def handle_WalletUpgrades(request):
    if request.method == "POST":
        data = request.data
        # print(data, request.user)
        holder = get_object_or_404(Holder, id=int(data.get("holder")["id"]))
        personel = get_object_or_404(Personel, user=request.user)
        serializer = WalletUpgradesSerializer(data=data)
        if serializer.is_valid(True):
            serializer.save(holder=holder, seller=personel)
            return Response(serializer.data)


class WalletUpgradesView(DatabaseView):
    model = WalletUpgrades
    serializer = WalletUpgradesSerializer
    http_method_names = ["get", "post"]

    def post(self, request):
        data = request.data
        if "personel" in data.keys():
            """making a report for a personel"""
            personel = data.pop("personel")
            seller, checked = loginAllUsers(request, username=personel.get("username"), password=personel.get("password"), api=True)
            if seller and checked == 200:
                upgrade = self.serializer(data=dict(**data, personel=seller.personel.id), context={"request": request})
                if upgrade.is_valid(True):
                    upgrade.save()
                    return Response(upgrade.data)
            else:
                return Response(seller, status=checked)
        else:
            """making a report for a holder"""
            upgrade = self.serializer(data=dict(**data, personel=request.user.personel.id), context={"request": request})
            if upgrade.is_valid(True):
                upgrade.save()
                return Response(upgrade.data)


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def handle_WalletUpgradesPassword(request):
#     if request.method == "GET":
#         walletUpgrades = WalletUpgrades.objects.all()
#         serializer = WalletUpgradesSerializer(walletUpgrades, many=True, context={"request": request})
#         return Response(serializer.data)
#     if request.method == "POST":
#         data = request.data
#         seller, checked = loginAllUsers(request, password=request.data.get("password"), username=request.data.get("seller").get("username"), api=True)
#         if seller and checked == 200:
#             holder = get_object_or_404(Holder, id=int(data.get("holder")["id"]))
#             personel = get_object_or_404(Personel, user=seller)
#             wallet_upgrade = WalletUpgradesSerializer(data=data)
#             if wallet_upgrade.is_valid(True):
#                 wallet_upgrade.save(holder=holder, seller=personel)
#                 return Response(wallet_upgrade.data)
#             # wallet_upgrade.save(holder=holder, seller=personel)
#             # serializer = WalletUpgradesSerializer(wallet_upgrade, many=False, context={"request": request})
#             # return Response(serializer.data)
#         return Response({"message": "Seller not found"}, status=501)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def handle_WalletUpgradesCards(request):
    if request.method == "GET":
        walletUpgrades = WalletUpgrades.objects.all()
        serializer = WalletUpgradesSerializer(walletUpgrades, many=True, context={"request": request})
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        seller, checked = loginAllUsers(request, password=request.data.get("password"), username=request.data.get("username"), api=True)
        if seller and checked == 200:
            id = int(data.get("holder")["id"])
            holder = Holder.objects.get(id=id)
            personel = Personel.objects.get(user_holder__card=request.data.get("card"))
            # TODO: check who the card is associated to
            wallet_upgrade = WalletUpgrades.objects.create(holder=holder, amount=data.get("amount"), seller=personel)
            serializer = WalletUpgradesSerializer(wallet_upgrade, many=False, context={"request": request})
            return Response(serializer.data)
        return Response({"message": "Seller not found"}, status=501)


# @api_view(["GET", "POST", "DELETE"])
# @permission_classes([IsAuthenticated])
# def handle_Cards(request):
#     if request.method == "GET":
#         cards = Card.objects.all()
#         serializer = CardSerializer(cards, many=True, context={"request": request})
#         return Response(serializer.data)
#     if request.method == "POST":
#         data = request.data
#         serializer = CardSerializer(data=data, many=False, context={"request": request})
#         if serializer.is_valid(True):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
#     if request.method == "DELETE":
#         card = Card.objects.get(id=data.get("id"))
#         card.delete()
#         return Response()


class CardView(DatabaseView):
    model = Card
    serializer = CardSerializer
    http_method_names = ["get", "post", "delete"]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            card = Card.objects.get(card_id=pk)
            serializer = CardSerializer(card, many=False, context={"request": request})
            return Response(serializer.data)
        return super().get(request, *args, **kwargs)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk:
            card = get_object_or_404(Card, card_id=pk)
            card.delete()
            return Response({"message": "Card deleted successfully!"})


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def handle_Card(request, pk):
    if request.method == "GET":
        card = Card.objects.get(card_id=pk)
        serializer = CardSerializer(card, many=False, context={"request": request})
        return Response(serializer.data)
    if request.method == "PUT":
        data = request.data
        card = Card.objects.get(id=pk)
        card.card_name = data.get("card_name")
        card.save()
        serializer = CardSerializer(card, many=False, context={"request": request})
        return Response(serializer.data)
    if request.method == "DELETE":
        card = Card.objects.get(id=pk)
        card.delete()
        return Response()
