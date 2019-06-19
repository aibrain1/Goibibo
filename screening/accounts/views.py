from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.


def index(request):
	if not request.user.is_authenticated:
		template = loader.get_template('accounts/login.html')
		context = {
			'title': 'Login',
		}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/dashboard')

@login_required(login_url='/')
def logout(request):
	auth.logout(request)
	return redirect('/')


def registerView(request):
	template = loader.get_template('accounts/register.html')
	context = {
		'title': 'Register',
	}
	try:
		return HttpResponse(template.render(context, request))
	except Exception as exception:
		context['errormsg'] = 'something went wrong please try again'
		return HttpResponse(template.render(context, request))	

def registerNewUser(request):
	context = {
		'title': 'Register',
	}
	if not request.user.is_authenticated:
		try:
			if request.method == 'POST':
				if request.POST['inputPassword'] == request.POST['inputConfirmPassword']:
					userObjectEmail = User.objects.filter(email=request.POST['inputEmail']).exists()
					userObjectName = User.objects.filter(username=request.POST['inputName']).exists()
					if userObjectEmail:
						context['formError'] = 'The email has already been taken.'
						template = loader.get_template('accounts/register.html')
						return HttpResponse(template.render(context, request))
					if userObjectName:
						context['formError'] = 'The username has already been taken.'
						template = loader.get_template('accounts/register.html')
						return HttpResponse(template.render(context, request))
					else:
						userObject = User.objects.create_user(username=request.POST['inputName'], password=request.POST['inputPassword'],email=request.POST['inputEmail'])
						auth.login(request,userObject)
						return redirect('/')	
					
			else:
				template = loader.get_template('404.html')
				return HttpResponse(template.render(context, request))	
		except Exception as exception:
			template = loader.get_template('404.html')
			context['errormsg'] = 'something went wrong please try again'
			return HttpResponse(template.render(context, request))
	else:
		return redirect('/')	

def loginAccount(request):

	context = {
		'title': 'Login',
	}
	if not request.user.is_authenticated:
		try:
			if request.method == 'POST':
				if request.POST['inputUser'] and request.POST['inputPassword']:

					userObject = auth.authenticate(username=request.POST['inputUser'],password=request.POST['inputPassword'])

					if userObject is not None:
						auth.login(request,userObject)
						return redirect('/dashboard')
					else:	
						context['formError'] = 'These credentials do not match our records.'
						template = loader.get_template('accounts/login.html')
						return HttpResponse(template.render(context, request))
				else:
					context['formError'] = 'Please fill all fields correctly.'
					template = loader.get_template('accounts/login.html')
					return HttpResponse(template.render(context, request))	
			else:
				template = loader.get_template('404.html')
				return HttpResponse(template.render(context, request))	
		except Exception as exception:
			template = loader.get_template('404.html')
			context['errormsg'] = 'something went wrong please try again'
			return HttpResponse(template.render(context, request))
	else:
		return redirect('/dashboard')