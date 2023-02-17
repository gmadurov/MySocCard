import datetime
from purchase.forms import ProductForm
from django.contrib import messages

from users.models import Holder, WalletUpgrades
from purchase.utils import paginateObjects
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Product, Barcycle, Category, Purchase

# Create your views here.
"""This page is for what the bestuur sees it is overview info"""


@login_required(login_url="login")
def showPurchases(request):
    purchases = Purchase.objects.all()
    content = {"purchases": purchases}
    return render(request, "purchase/purchases.html", content)


@login_required(login_url="login")
def showPurchase(request, pk):
    purchase = Purchase.objects.get(id=pk)
    content = {"purchase": purchase}
    return render(request, "purchase/purchase.html", content)


@login_required(login_url="login")
def showProducts(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    #   find how many of each product a request user has bought
    quantity = {
        prod.id: orders.filter(ordered__in=request.user.holder.purchases.all()).filter(product=prod).aggregate(Sum("quantity")).get("quantity__sum") or 0
        for prod in products
    }
    custom_range, products = paginateObjects(request, list(products), 10, "product_page")

    content = {
        "products": products,
        "quantity": quantity,
        "custom_range": custom_range,
    }
    return render(request, "purchase/products.html", content)


@login_required(login_url="login")
def showProductOverviews(request, pk):
    product = Product.objects.get(id=pk)
    start_date = datetime.datetime.strptime(
        request.GET.get("start_date", (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")), "%Y-%m-%dT%H:%M"
    )
    end_date = datetime.datetime.strptime((request.GET.get("end_date", (datetime.datetime.today()).strftime("%Y-%m-%dT%H:%M"))), "%Y-%m-%dT%H:%M")

    #   find how many of each product a request user has bought
    purchases = Purchase.objects.filter(
        created__gte=start_date,
        created__lte=end_date,
    ).filter(orders__product__id=pk)
    content = {
        "product": product,
        "purchases": purchases,
    }
    return render(request, "purchase/product.html", content)


@login_required(login_url="login")
def showProduct(request, pk):
    product = Product.objects.get(id=pk)
    purchases = Purchase.objects.filter(orders__product=product).filter(buyer=request.user.holder)
    content = {
        "product": product,
        "purchases": purchases,
    }
    return render(request, "purchase/product.html", content)


@login_required(login_url="login")
def showOverview(request):
    # get puchased in a certain time period specified by a forms in the request
    start_date = datetime.datetime.strptime(
        request.GET.get("start_date", (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")), "%Y-%m-%dT%H:%M"
    )
    end_date = datetime.datetime.strptime((request.GET.get("end_date", (datetime.datetime.today()).strftime("%Y-%m-%dT%H:%M"))), "%Y-%m-%dT%H:%M")

    purchases = Purchase.objects.filter(
        created__gte=start_date,
        created__lte=end_date,
    )

    #  get all the products that has been bought in the purchases
    products = [prod.product for pur in purchases for prod in pur.orders.all()]
    products_quant = {
        prod: purchases.filter(orders__product=prod).aggregate(Sum("orders__quantity")).get("orders__quantity__sum") or 0 for prod in products
    }.items()

    # get sum of all holder stands
    holder_stands = Holder.objects.all().aggregate(Sum("stand")).get("stand__sum")

    barWinst = sum([pur.total for pur in purchases])
    totalGepind = sum([pur.total for pur in purchases.filter(pin=True)])
    totalGecashed = sum([pur.total for pur in purchases.filter(cash=True)])
    bezoekers_pasen = sum([pur.total for pur in purchases.filter(buyer__user__groups__name__in=["Bezoekers"])])
    handelswaar = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Handelswaar"])])
    happenPin = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Happen"], pin=True)])
    happenCash = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Happen"], cash=True)])
    walletUpgradeQuery = WalletUpgrades.objects.filter(date__gte=start_date, date__lte=end_date)
    walletUpgrades = walletUpgradeQuery.aggregate(Sum("amount")).get("amount__sum")
    refunds = sum([wal.amount for wal in walletUpgradeQuery.filter(refund=True)])
    custom_range_products_quant, products_quant = paginateObjects(request, list(products_quant), 10, "product_page")
    custom_range_purchases, purchases = paginateObjects(request, purchases, 20, "purchase_page")
    content = {
        "purchases": purchases,
        "products_quant": products_quant,
        "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
        "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
        "holder_stands": holder_stands,
        "barWinst": barWinst,
        "walletUpgrades": walletUpgrades,
        "totalGepind": totalGepind,
        "totalGecashed": totalGecashed,
        "bezoekers_pasen": bezoekers_pasen,
        "handelswaar": handelswaar,
        "happenPin": happenPin,
        "happenCash": happenCash,
        "refunds": refunds,
        "custom_range_purchases": custom_range_purchases,
        "custom_range_products_quant": custom_range_products_quant,
    }
    return render(request, "purchase/overview.html", content)


@login_required(login_url="login")
def showBarcycles(request):
    barcycles = Barcycle.objects.all()
    content = {"barcycles": barcycles}
    return render(
        request,
        "purchase/barcycles.html",
        content,
    )


def showBarcycle(request, pk):
    barcycle = Barcycle.objects.get(id=pk)
    purchases = barcycle.purchases
    print(purchases)
    #  get all the products that has been bought in the purchases
    products = [prod.product for pur in purchases for prod in pur.orders.all()]
    products_quant = {
        prod: purchases.filter(orders__product=prod).aggregate(Sum("orders__quantity")).get("orders__quantity__sum") or 0 for prod in products
    }.items()

    # get sum of all holder stands
    holder_stands = Holder.objects.all().aggregate(Sum("stand")).get("stand__sum")
    barWinst = sum([pur.total for pur in purchases])
    totalGepind = sum([pur.total for pur in purchases.filter(pin=True)])
    totalGecashed = sum([pur.total for pur in purchases.filter(cash=True)])
    bezoekers_pasen = sum([pur.total for pur in purchases.filter(buyer__user__groups__name__in=["Bezoekers"])])
    handelswaar = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Handelswaar"])])
    happenPin = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Happen"], pin=True)])
    happenCash = sum([pur.total for pur in purchases.filter(orders__product__cat_products__name__in=["Happen"], cash=True)])
    custom_range_products_quant, products_quant = paginateObjects(request, list(products_quant), 10, "product_page")
    custom_range_purchases, purchases = paginateObjects(request, purchases, 10, "purchase_page")
    content = {
        "purchases": purchases,
        "products_quant": products_quant,
        "holder_stands": holder_stands,
        "barWinst": barWinst,
        "totalGepind": totalGepind,
        "totalGecashed": totalGecashed,
        "bezoekers_pasen": bezoekers_pasen,
        "handelswaar": handelswaar,
        "happenPin": happenPin,
        "happenCash": happenCash,
        "custom_range_purchases": custom_range_purchases,
        "custom_range_products_quant": custom_range_products_quant,
        "barcycle": barcycle,
    }
    return render(request, "purchase/barcycle.html", content)


def showUpgrades(request):
    return redirect("https://expo.dev/accounts/gusmadvol/projects/mamon-gus/builds/ceadb199-b637-4596-b702-a8fba62e1880")


def product_form(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        if request.method == "POST":
            form = ProductForm(data=request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect("product", pk=product.pk)
            else:
                messages.error(request, form.errors)
    else:
        form = ProductForm()
        if request.method == "POST":
            form = ProductForm(data=request.POST)
            if form.is_valid():
                product = form.save()
                return redirect("product", pk=product.pk)
            else:
                messages.error(request, form.errors)
    return render(request, "purchase/product_form.html", {"form": form})


@login_required
def dailyOverview(request):
    mode = request.GET.get("mode", "days")
    category = int(request.GET.get("category", 0))
    start_date = datetime.datetime.strptime(
        request.GET.get("start_date", (datetime.datetime.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")), "%Y-%m-%dT%H:%M"
    )
    end_date = datetime.datetime.strptime((request.GET.get("end_date", (datetime.datetime.today()).strftime("%Y-%m-%dT%H:%M"))), "%Y-%m-%dT%H:%M")

    categories = Category.objects.all()
    purchases = Purchase.objects.filter(
        created__gte=start_date,
        created__lte=end_date,
    )
    products = [prod.product for pur in purchases for prod in pur.orders.all()] if category == 0 else categories.get(id=category).products.all()
    products_quant = {
        prod: purchases.filter(orders__product=prod).aggregate(Sum("orders__quantity")).get("orders__quantity__sum") or 0 for prod in products
    }
    print(mode)
    if mode == "days":
        date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        quantities = {
            prod.id: (
                prod,
                [
                    purchases.filter(orders__product=prod, created__day=day.day, created__month=day.month, created__year=day.year)
                    .aggregate(Sum("orders__quantity"))
                    .get("orders__quantity__sum")
                    or 0
                    for day in date_range
                ],
                products_quant[prod],
            )
            for prod in products
        }.values()
    else:
        # create a date_range for each month between start_date and end_date
        date_range = [
            datetime.datetime(year=year, month=month, day=1)
            for year in range(start_date.year, end_date.year + 1)
            for month in range(start_date.month if year == start_date.year else 1, end_date.month + 1 if year == end_date.year else 13)
        ]
        print(date_range)

        quantities = {
            prod.id: (
                prod,
                [
                    purchases.filter(orders__product=prod, created__month=day.month, created__year=day.year)
                    .aggregate(Sum("orders__quantity"))
                    .get("orders__quantity__sum")
                    or 0
                    for day in date_range
                ],
                products_quant[prod],
            )
            for prod in products
        }.values()

    # for each day in date_range get the total amount of products sold
    content = {
        "purchases": purchases,
        "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
        "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
        "quantities": quantities,
        "date_range": date_range,
        "categories": categories,
        "category": category,
        "mode": mode,
    }
    return render(request, "purchase/daily_overview.html", content)
