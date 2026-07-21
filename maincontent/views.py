from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import EmailSubscriptionForm, ContactForm
from .models import EmailSubscription
from django.conf import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'maincontent/home.html')


def about(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'form1':
            form = EmailSubscriptionForm(request.POST)
        elif form_id == 'form2':
            form = EmailSubscriptionForm(request.POST)

        email = request.POST.get('email')

        if form.is_valid():
            email = form.cleaned_data['email']
            if EmailSubscription.objects.filter(email=email).exists():
                messages.error(request, f'{email} already subscribed.')
            else:
                form.save()
                messages.success(request, f'Thank you for subscribing with email: {email}')
        else:
            messages.error(request, f'{form_id.capitalize()} is not valid.')
            print(form.errors) # Print for errors 

    form1 = EmailSubscriptionForm()
    form2 = EmailSubscriptionForm()

    return render(request, 'maincontent/about.html', {'form1': form1, 'form2': form2})

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email
            subject = 'Contact Form Submission'
            email_message = f'We have successfully recieved your form.\n\nThank you for contacting us.'
            from_email = settings.DEFAULT_FROM_EMAIL
            email_cpy = f'Username: {username}\nEmail: {email}\n\nMessage: {message}'
            recipient_list = [email]
            cpy_recipient = [from_email]

            print(recipient_list)
            try:
                send_mail(subject, email_message, from_email, recipient_list)
                send_mail(subject, email_cpy, from_email, cpy_recipient)
                messages.success(request, 'Your message has been sent successfully.')
            except Exception as e:
                messages.error(request, 'An error occurred while sending the email. Please try again.')
    

    form = ContactForm()
    return render(request, 'maincontent/contact.html', {'form': form})    
