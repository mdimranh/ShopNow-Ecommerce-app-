from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View
from .models import Profile, AddressBook
from setting.models import Slider, Banner, TeamInfo, Aboutus, ContactMessage
from product.models import Category, Product
from order.models import ShopCart
from datetime import datetime
from django.contrib.auth.models import User, Group, auth
from django.contrib import messages

from region.models import Country, Region, City, Area
from accounts.models import AddressBook, Profile

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render

from .models import EmailConfirmed

from django.contrib import messages

from setting.models import SiteConfiguration
siteinfo = SiteConfiguration.objects.get()

# def Account(request):
#     if request.method == "POST":
#         if 'first_name' in request.POST:
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             email = request.POST['email']
#             password = request.POST['password']

#             user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
#             user.set_password(password)
#             user.save()
#             Profile.objects.create(user = user)
#             return JsonResponse({'msg': "Account create successfully. please login first", 'success': 'yes'})
#         else:
#             email = request.POST['email']
#             password = request.POST['password']
#             user = auth.authenticate(username=email, password=password)

#             if user is not None:
#                 auth.login(request, user)
#                 pro = Profile.objects.get(user = user)
#                 pro.online = True
#                 pro.save()
#                 cart = ShopCart.objects.filter(user = user).order_by('created_at')
#                 total_cost = 0
#                 cart_serialize = []
#                 cs={}
#                 for item in cart:
#                     price = item.product.main_price - (item.product.main_price * item.product.discount / 100)
#                     cost = price*item.quantity
#                     total_cost += cost
#                     cs = {
#                         "id": item.id,
#                         "category": item.product.category.name,
#                         "title": item.product.title,
#                         "image": item.product.image,
#                         "main_price": str(item.product.main_price),
#                         "price": str(item.product.main_price - (item.product.main_price * item.product.discount / 100)),
#                         "discount": str(item.product.discount),
#                         "amount": item.quantity
#                     }
#                     cart_serialize.append(cs)


#                 for item in cart[:1]:
#                     if item.coupon:
#                         if item.coupon.discount_type == 'fixed':
#                             total_cost -= item.coupon.value
#                         else:
#                             total_cost = total_cost - (total_cost * item.coupon.value / 100)
#                 item = cart.count()
#                 context = {
#                     'item':item,
#                     'cost':total_cost,
#                     'msg': 'Login Successfull',
#                     'cart': cart_serialize,
#                     'name': user.first_name+" "+user.last_name
#                 }
#                 return JsonResponse(context)
#             else:
#                 msg = 'Invalid username or password!'
#                 return JsonResponse({'msg': msg})
#         return HttpResponse({"msg": 'Something is wrong'})
#     return render(request, "account/login.html")


def Account(request):
	if request.method == "POST":
		if 'signup-first-name' in request.POST:
			first_name = request.POST['signup-first-name']
			last_name = request.POST['signup-last-name']
			email = request.POST['signup-email']
			password = request.POST['signup-password']

			if User.objects.filter(email=email).exists():
				messages.info(request,'This email is already exist.')
				return redirect(request.path_info)

			else:
				user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
				user.is_active = False
				user.save()
				euser = EmailConfirmed.objects.get(user = user)
				site = get_current_site(request)
				email = user.email
				email_body = render_to_string(
					'account/verify.html',
					{
						'email': email,
						'domain': site.domain,
						'activation_key': euser.activation_key,
						'site_name': siteinfo.name,
					}
				)
				send_mail(
					subject='Email Confirmation',
					message=email_body,
					from_email='mdimranh.cse@gmail.com',
					recipient_list=[email],
					fail_silently=True
				)
				messages.success(request, "Account created successfull. We will send you a link in your email for active your account. Please active your account by click the link.")
				return redirect('login')

			user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
			user.set_password(password)
			user.save()
			Profile.objects.create(user = user)
			return redirect(request.path_info)
		elif 'recover-email' in request.POST:
			if not User.objects.filter(email = request.POST['recover-email']).exists():
				messages.error(request,"Don't have any account with this email")
				return redirect(request.path_info)
			else:
				usr = User.objects.get(email = request.POST['recover-email'])
				usr.is_active = False
				usr.save()
				euser = EmailConfirmed.objects.get(user = usr)
				site = get_current_site(request)
				email_body = render_to_string(
					'account/recover.html',
					{
						'email': usr.email,
						'domain': site.domain,
						'activation_key': euser.activation_key,
						'site_name': siteinfo.name,
					}
				)
				send_mail(
					subject='Password Recover',
					message=email_body,
					from_email='mdimranh.cse@gmail.com',
					recipient_list=[usr.email],
					fail_silently=True
				)
				messages.success(request, "We will send you a link in your email for recover your password. Please set new password by click the link.")
				return redirect(request.path_info)
		else:
			email = request.POST['signin-email']
			password = request.POST['signin-password']
			user = auth.authenticate(username=email, password=password)

			if user is not None:
				auth.login(request, user)
				response = HttpResponseRedirect('/profile')
				ucart, create = ShopCart.objects.get_or_create(user=request.user, on_order=False)
				gcart, create = ShopCart.objects.get_or_create(device=request.COOKIES['device'], on_order=False)
				set_cart = 'ucart' if ucart.carts.all().count() > gcart.carts.all().count() else 'gcart'
				response.set_cookie('cart', set_cart)
				return response
			else:
				messages.error(request, "User name or password don't match!!")
				return redirect(request.path_info)
		messages.add_message(request, messages.error, 'Something is wrong!')
		return redirect(request.path_info)
	if request.user.is_authenticated:
		return redirect('home')
	else:
		return render(request, "account/login.html")

def emailConfirm(request, activation_key):
	euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
	if euser is not None:
	   euser.email_confirmd = True
	   euser.save()
	   
	   user1 = User.objects.get(email = euser)
	   user1.is_active = True
	   user1.save()
	   return render(request, 'account/success.html')

def passwordRecover(request, activation_key):
	if request.method == 'POST':
		if 'new-password' in request.POST:
			user = User.objects.get(email = request.POST['user_email'])
			user.set_password(request.POST['new-password'])
			user.save()
			messages.success(request, 'Password set successfully. Please login..')
			return redirect('/auth/')
	else:
		euser = get_object_or_404(EmailConfirmed, activation_key = activation_key)
		if euser is not None:
			euser.email_confirmd = True
			euser.save()
			user1 = User.objects.get(email = euser)
			user1.is_active = True
			user1.save()
			return render(request, 'account/newpass.html', {'user_email': euser})

class DeleteUser(View):
	def post(self, request):
		total_user = len(request.POST["users"].split(','))
		for user_id in request.POST["users"].split(','):
			User.objects.get(id = user_id).delete()
		context = {
			'total' : total_user
		}
		return JsonResponse(context)

class DeleteGroup(View):
	def post(self, request):
		total_group = len(request.POST["groups"].split(','))
		for group_id in request.POST["groups"].split(','):
			Group.objects.get(id = group_id).delete()
		context = {
			'total' : total_group
		}
		return JsonResponse(context)

def ProfileView(request):
	if request.method == 'POST':
		if 'ab-name' in request.POST:
			if request.POST.get('default') == 'on':
				default = True
				for ab in AddressBook.objects.filter(default = 'True'):
					ab.default = False
					ab.save()
			else: default = False
			user = request.user
			name = request.POST['ab-name']
			phone = request.POST['ab-phone']
			if request.POST['ab-country'] != 'null':
				country = Country.objects.get(id = request.POST['ab-country'])
			else: country = None
			if request.POST['ab-region'] != 'null':
				region = Region.objects.get(id = request.POST['ab-region'])
			else: region = None
			if request.POST['ab-city'] != 'null':
				city = City.objects.get(id = request.POST['ab-city'])
			else: city = None
			if request.POST['ab-area'] != 'null':
				area = Area.objects.get(id = request.POST['ab-area'])
			else: area = None
			address = request.POST['ab-address']
			address_book = AddressBook(
				user=user, name=name, phone=phone, country=country, region=region, city=city, area=area, address=address, default=default
			)
			address_book.save()
			return redirect(request.path_info)
		if 'id' in request.POST:
			ab = AddressBook.objects.get(id = request.POST['id'])
			ab.name = request.POST['name']
			ab.phone = request.POST['phone']
			ab.address = request.POST['address']
			ab.country = Country.objects.get(id = request.POST['country'])
			ab.region = Region.objects.get(id = request.POST['region'])
			ab.city = City.objects.get(id = request.POST['city'])
			ab.area = Area.objects.get(id = request.POST['area'])
			ab.save()
			return redirect(request.path_info)
		if 'birthday' in request.POST:
			usr = request.user
			usr.first_name = request.POST['fname']
			usr.last_name = request.POST['lname']
			usr.save()
			pro, create = Profile.objects.get_or_create(user = usr)
			pro.birthday = request.POST['birthday']
			pro.phone = request.POST['phone']
			pro.gender = request.POST['gender']
			pro.save()
			return redirect(request.path_info)
	total_cost = 0
	item = 0
	countrys = Country.objects.all()
	address_book = AddressBook.objects.filter(user = request.user)
	context = {
		'address_book': address_book,
		'countrys': countrys
	}
	return render(request, 'account/profile.html', context)

def Logout(request):
	auth.logout(request)
	return redirect('/')

import json
# def GetCity(request):
#     id = request.POST['id']
#     city = []
#     f = open('bd-districts.json', 'r', encoding='utf-8')
#     data = json.load(f)
#     for i in data['districts']:
#         if i['division_id'] == id:
#             city.append((i['name'], i["id"]))
#     f.close()
#     return JsonResponse(data = city, safe=False)


def GetRegion(request):
	region_list = []
	for region in Country.objects.get(id = request.POST['id']).region.all():
		region_list.append((region.name, region.id))
	return JsonResponse(data = region_list, safe=False)

def GetCity(request):
	city_list = []
	for city in Region.objects.get(id = request.POST['id']).city.all():
		city_list.append((city.name, city.id))
	return JsonResponse(data = city_list, safe=False)

def GetArea(request):
	area_list = []
	for area in City.objects.get(id = request.POST['id']).area.all():
		area_list.append((area.name, area.id))
	return JsonResponse(data = area_list, safe=False)

class MergeCart(View):
	def post(self, request):
		from_cart = request.POST['from']
		if from_cart == 'gcart':
			gcart = ShopCart.objects.get(device=request.COOKIES['device'], on_order=False)
			ucart = ShopCart.objects.get(user = request.user, on_order=False)
			for cart in gcart.carts.all():
				if cart not in ucart.carts.all():
					ucart.carts.add(cart)
			gcart.carts.all().delete()
		else:
			gcart = ShopCart.objects.get(device=request.COOKIES['device'], on_order=False)
			ucart = ShopCart.objects.get(user = request.user, on_order=False)
			for cart in ucart.carts.all():
				if cart not in gcart.carts.all():
					gcart.carts.add(cart)
			ucart.carts.all().delete()
		return JsonResponse('success', safe=False)