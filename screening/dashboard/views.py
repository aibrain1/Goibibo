from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Stock
from .forms import StockForm
import os,json
# Create your views here.

def index(request):
	template = loader.get_template('dashboard/dashboard.html')

	if request.method == "POST":
		form = StockForm(request.POST)
		if form.is_valid():
			stock = form.save(commit=False)
			stock.save()
			return redirect('/')
	data_form = StockForm()
	context = {
		'title': 'Dashboard',
		'form': data_form,
	}
	return HttpResponse(template.render(context, request))

def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


def suggestionSearch(request):
	data = request.GET
	stock_detail = Stock.objects.filter(title__icontains=data.get("term")).values('title','id')
	results = []
	for stock in stock_detail.all():
		user_json = {}
		user_json['id'] = stock['id']
		user_json['label'] = stock['title']
		user_json['value'] = stock['title']
		results.append(user_json)
	data = json.dumps(results)
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)	   
	