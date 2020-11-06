from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from listings.choices import state_choices,bedroom_choices,price_choices
# Create your views here.
def index(request):
    listings = Listing.objects.all().filter(is_published=True)
    paginator = Paginator(listings,6)
    page = request.GET.get('page')
    paged_listing = paginator.get_page(page)
    context ={
        'listings':paged_listing
    }
    return render(request,'listing/listings.html',context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    context ={
        'listing' : listing
    }
    return render(request,'listing/listing.html' ,context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # get keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    #prices
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
     #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    context ={
        'state_choices':state_choices,
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,
        'listings': queryset_list,
        'values':request.GET
    }
    return render(request,'listing/search.html', context)

