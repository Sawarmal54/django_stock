from django.shortcuts import render,redirect, get_object_or_404
from .models import Stock
from .forms import StockForm
from django.contrib import messages
def home(request):
    import requests
    import json
    
    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get(" https://api.iex.cloud/v1/data/core/quote/"+ ticker +"?token=pk_9b367d9b8e0b49388cbc6885ca6274e0")
    
        try:
            api =json.loads(api_request.content)
        except Exception as e:
            api = "Error"
        
        #pk=pk_9b367d9b8e0b49388cbc6885ca6274e0
        return render(request, 'home.html',{'api' : api})

    else:
        return render(request, 'home.html', {'ticker':"Enter a Ticker Symbol Above..."})
    


def add_stock(request):
    import requests
    import json
    if request.method == "POST":
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request,("Stock Has Been Added "))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output=[]
        for ticker_item in ticker:
            
            api_request = requests.get(" https://api.iex.cloud/v1/data/core/quote/"+ str(ticker_item) +"?token=pk_9b367d9b8e0b49388cbc6885ca6274e0")
            
            try:
                api =json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api ="Error..."
        return render(request, 'add_stock.html', {'ticker':ticker,'output':output})

def about(request):
    return render(request, 'about.html', {})


def delete(request,stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock Has Been Deleted"))
    return redirect('delete_stock')

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html',{'ticker':ticker})