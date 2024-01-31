from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from userauths.forms import UserRegisterForm
from userauths.models import User
from .forms import WithdrawalForm
from .models import UserProfile, Withdrawal
from .forms import DepositForm
from django.core.mail import send_mail

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey {username}, Account Successfully Created')
            new_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('core:index')  # Redirect to a specific page after registration
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'userauths/sign-up.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')  # Redirect to a specific page if the user is already authenticated

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, "Invalid credentials")
            return redirect('userauths:sign-in')  # Redirect to the login page with a warning

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In Successfully')
            return redirect('core:index')  # Redirect to a specific page after successful login
        else:
            messages.warning(request, 'Invalid credentials')

    return render(request, 'userauths/sign-in.html')

@login_required
def base_view(request):
    user = request.user
    balance = user.balance
    return render(request, 'patrtials/base.html', {'balance': balance})

def logout_view(request):
    logout(request)
    return redirect(reverse('userauths:sign-in'))  # Redirect to the login page after logout


@login_required
def withdrawal_view(request):
    # Retrieve or create UserProfile for the current user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount <= user_profile.balance:
                withdrawal = Withdrawal.objects.create(user=request.user, amount=amount)
                user_profile.balance -= amount
                user_profile.save()
                return redirect('core:withdrawal')  # Redirect to a success page or home page
            else:
                form.add_error('amount', 'Insufficient balance.')
    else:
        form = WithdrawalForm()

    return render(request, 'core/withdrawal.html', {'form': form})




@login_required
def deposit_form(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            # Get the deposit amount and username from the form
            deposit_amount = form.cleaned_data['amount']
            username = request.user.username

            # Update user profile balance
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.balance += deposit_amount
            user_profile.save()
        
            # Send an email notification
            send_mail(
                'Deposit Request',
                f'{username} has requested to deposit ${deposit_amount}.',
                'your@email.com',  # Your email address
                ['jahswillomenazu@gmail.com'],  # Your email address
                fail_silently=False,
            )

            messages.success(request, 'Deposit request submitted. You will be contacted soon.')
            return redirect('core:index')  # Redirect to a success page or the index

    else:
        form = DepositForm()

    return render(request, 'core/deposit_form.html', {'form': form})
