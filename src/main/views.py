from django.shortcuts import redirect, render
from products.models import *
from .models import *
from client.forms import *
from django.contrib import messages
import requests
from django.shortcuts import get_object_or_404
from client.models import Districts

def getSectionAll():
  return {
    'info_company': InfoCompany.objects.all(),
    'address': Address.objects.all(),
    'numbers': Numbers.objects.all(),
    'welcome_section': WelcomeSection.objects.all(),
    'menu_section': MenuSection.objects.all(),
    'category_section': CategorySection.objects.all(),
    'combo_section': ComboSection.objects.all(),
    'work_time': ScheduleTime.objects.all(),
  }

def dictExpand(expandable, expander):
  for prop in expander:
    expandable[prop] = expander[prop]

  return expandable


def thanks(request):
  adress = Address.objects.all()
  numbers = Numbers.objects.all()
  info_company = InfoCompany.objects.all()
  categories = CategoryProduct.objects.all()
  total = request.GET['total']
  self_pickup_status = request.GET['self_pickup']

  context = {
    'address': adress,
    'numbers': numbers,
    'info_company': info_company,
    'categories': categories,
    'total': total,
    'self_pickup_status': self_pickup_status,
  }

  return render(request, 'main/thanks.html', context)

# Controller
def main(request):
  form = OrderForm()
  districts = Districts.objects.all()
  
  if request.method == 'POST':
    post_data = request.POST.copy()
    form = OrderForm(post_data)

    if form.is_valid():
        try:
          if str(post_data['self_pickup']):
            self_pickup = 'true'
        except:
          self_pickup = 'false'
          
        if post_data['payment_method'] == 'card':
          response = requests.post('https://api.monobank.ua/api/merchant/invoice/create', json={"amount": int(post_data['amount']) * 100, "redirectUrl": f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}"}, headers={"X-Token": "mfvrzEkIfEu3vNrKm6DJhjQ",})
          post_data['invoice_id'] = response.json()['invoiceId']
          form = OrderForm(post_data)
          form.save()
          return redirect(response.json()['pageUrl'])
          
        elif post_data['payment_method'] == 'cash':
          post_data['invoice_id'] = '-'
          form = OrderForm(post_data)
          form.save()
          messages.success(request, "Замовлення відправлене, очікуйте на смачну доставку від кур'єра")
          return redirect(f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}")
    else:
        messages.error(request, 'Упс, щось пішло не так... Відправте замовлення повторно')
        return redirect('home')

  categories = CategoryProduct.objects.all()
  products_promo = Product.objects.filter(category__slug = 'promo')

  context = dictExpand({
    'categories': categories,
    'order_form': form,
    'products_promo': products_promo,
    'districts': districts,
  }, getSectionAll())


  return render(request, 'main/index.html', context)

# Controller
def category(request, slug_category):
  form = OrderForm()
  categories = CategoryProduct.objects.all()

  if request.method == 'POST':
    post_data = request.POST.copy()
    form = OrderForm(post_data)

    if form.is_valid():
        try:
          if str(post_data['self_pickup']):
            self_pickup = 'true'
        except:
          self_pickup = 'false'
        
        if post_data['payment_method'] == 'card':
          response = requests.post('https://api.monobank.ua/api/merchant/invoice/create', json={"amount": int(post_data['amount']) * 100, "redirectUrl": f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}"}, headers={"X-Token": "mfvrzEkIfEu3vNrKm6DJhjQ",})
          post_data['invoice_id'] = response.json()['invoiceId']
          form = OrderForm(post_data)
          form.save()
          return redirect(response.json()['pageUrl'])
          
        elif post_data['payment_method'] == 'cash':
          post_data['invoice_id'] = '-'
          form = OrderForm(post_data)
          form.save()
          messages.success(request, "Замовлення відправлене, очікуйте на смачну доставку від кур'єра")
          return redirect(f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}")
    else:
        messages.error(request, 'Упс, щось пішло не так... Відправте замовлення повторно')
        return redirect('home')
        
  category = get_object_or_404(CategoryProduct, slug=slug_category)

  products_category = Product.objects.filter(category_id = category.pk)

  context = dictExpand({
    'category': category,
    'products': products_category,
    'order_form': form,
    'categories': categories,
  }, getSectionAll())

  return render(request, 'main/category.html', context)

# Controller
def combo(request):
  form = OrderForm()
  categories = CategoryProduct.objects.all()

  if request.method == 'POST':
    post_data = request.POST.copy()
    form = OrderForm(post_data)

    if form.is_valid():
        try:
          if str(post_data['self_pickup']):
            self_pickup = 'true'
        except:
          self_pickup = 'false'
        
        if post_data['payment_method'] == 'card':
          response = requests.post('https://api.monobank.ua/api/merchant/invoice/create', json={"amount": int(post_data['amount']) * 100, "redirectUrl": f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}"}, headers={"X-Token": "mfvrzEkIfEu3vNrKm6DJhjQ",})
          post_data['invoice_id'] = response.json()['invoiceId']
          form = OrderForm(post_data)
          form.save()
          return redirect(response.json()['pageUrl'])
          
        elif post_data['payment_method'] == 'cash':
          post_data['invoice_id'] = '-'
          form = OrderForm(post_data)
          form.save()
          messages.success(request, "Замовлення відправлене, очікуйте на смачну доставку від кур'єра")
          return redirect(f"https://georges.com.ua/thanks?total={post_data['amount']}&self_pickup={self_pickup}")
    else:
        messages.error(request, 'Упс, щось пішло не так... Відправте замовлення повторно')
        return redirect('home')
        
  combos = Combo.objects.all()
  products = Product.objects.all()

  context = dictExpand({
    'order_form': form,
    'combos': combos,
    'categories': categories,
  }, getSectionAll())

  return render(request, 'main/combo.html', context)