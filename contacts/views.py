from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        # check the inquery if the alreaady exits
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request , 'your inquery already exists for this listing')
                return redirect('/listing/'+listing_id)
        contact = Contact(listing_id=listing_id , listing=listing, name=name, email=email,phone=phone,message=message,user_id=user_id)
        contact.save()
        send_mail(
            'Property Listing Inquery',
            'There has been inquery for '+listing+ '. sign into the admin for more information',
            'btre123@gmail.com',
            [realtor_email, 'saifultechie@gmail.com'],
            fail_silently=False

        )
        messages.success(request , 'your request has been submitted, the realtor will get back to soon you')
        return redirect('/listing/'+listing_id)
