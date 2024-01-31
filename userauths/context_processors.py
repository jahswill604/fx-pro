# userauths/context_processors.py
from .models import UserProfile

def balance(request):
    user_balance = 0  # Default value if the user is not logged in or doesn't have a profile

    if request.user.is_authenticated:
        try:
            user_balance = UserProfile.objects.get(user=request.user).balance
        except UserProfile.DoesNotExist:
            pass  # Handle the case where the user doesn't have a profile

    return {'user_balance': user_balance}
