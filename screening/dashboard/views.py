from django.shortcuts import render,redirect
from django.http import HttpResponse
from cache_memoize import cache_memoize
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import Stock
from .forms import StockForm
import os,json,requests
import objectpath


#For Main Dashboard View
@login_required(login_url='/')
def index(request):
	template = loader.get_template('dashboard/dashboard.html')

	context = {
		'title': 'Dashboard',
	}
	return HttpResponse(template.render(context, request))

#Handel Error View
def handler404(request):
	return render(request, '404.html', status=404)

#Handel Error View
def handler500(request):
	return render(request, '500.html', status=500)

#Add Value In Suggestion Search DropDown View
@login_required(login_url='/')
def addStock(request):
	template = loader.get_template('dashboard/addStock.html')
	try:
		if request.method == "POST":
			form = StockForm(request.POST)
			if form.is_valid():
				stock = form.save(commit=False)
				stock.save()
				return redirect('/')
		data_form = StockForm()
		context = {
			'title': 'Add Stock',
			'form': data_form,
		}
		return HttpResponse(template.render(context, request))
	except Exception as exception:
		context['errormsg'] = 'something went wrong please try again'
		return HttpResponse(template.render(context, request))

#Get Value Suggestion Search DropDown
@login_required(login_url='/')
@cache_memoize(100)
def suggestionSearch(request):
	results = []
	try:
		if request.is_ajax():
			data = request.GET
			stock_detail = Stock.objects.filter(title__icontains=data.get("term")).order_by('-title').values('title').distinct()
			for stock in stock_detail:
				user_json = {}
				user_json['label'] = stock['title']
				user_json['value'] = stock['title']
				results.append(user_json)
			data = json.dumps(results)
			mimetype = 'application/json'
			return HttpResponse(data, mimetype)
	except Exception as exception:
		results['errormsg'] = 'something went wrong please try again'
		data = json.dumps(results)
		mimetype = 'application/json'
		return HttpResponse(data, mimetype)

#Parse Json View
@login_required(login_url='/')
def jsonParserView(request):
	template = loader.get_template('dashboard/jsonParser.html')
	try:
		context = {
			'title': 'Parse Json',
		}
		return HttpResponse(template.render(context, request))
	except Exception as exception:
		context['errormsg'] = 'something went wrong please try again'
		return HttpResponse(template.render(context, request))

#Parse JSON BY key Value
@login_required(login_url='/')
def extract_values(obj, key):
	"""Pull all values of specified key from nested JSON."""
	arr = []
	def extract(obj, arr, key):
		"""Recursively search for values of key in JSON tree."""
		if isinstance(obj, dict):
			for k, v in obj.items():
				if isinstance(v, (dict, list)):
					extract(v, arr, key)
				if k == key:
					arr.append(v)
		elif isinstance(obj, list):
			for item in obj:
				extract(item, arr, key)
		return arr
	results = extract(obj, arr, key)
	return results

#Response after parse JSON Data	
@login_required(login_url='/')
def jsonLoadAndParse(request):
	try:
		arr = []
		if request.is_ajax() and request.POST['dataLoad'] and request.POST['searchKey']:
			users = json.loads(request.POST['dataLoad'])
			names = extract_values(users, request.POST['searchKey'])
			data = json.dumps(names)
			mimetype = 'application/json'
			return HttpResponse(data, mimetype)
	except Exception as exception:
		return HttpResponse([])		
