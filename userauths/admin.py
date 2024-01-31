from django.contrib import admin
from userauths.models import User
from .models import Index, Package
# from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Withdrawal #,Deposit

class IndexAdmin(admin.ModelAdmin):
    list_display = ['Home', 'HeroHeader','whyChooseUs']  # Add or remove fields as needed

admin.site.register(Index, IndexAdmin)

class PackageAdmin(admin.ModelAdmin):
    list_display = ['package_Header', 'Package_Price', 'Package_Discribtion_1']  # Add or remove fields as needed

admin.site.register(Package, PackageAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_active')
    search_fields = ('username', 'email')

    def display_balance(self, obj):
        # Custom method to display balance with a dollar sign
        return f"${obj.balance}"

    display_balance.short_description = 'Balance'  # Set the column header

    def add_balance_to_selected_users(self, request, queryset):
        # Define the default balance to be added
        default_balance = 100  # Change this value as needed

        # Loop through all selected users and add the default balance
        for user in queryset:
            user.balance += default_balance
            user.save()

        self.message_user(request, f'Added ${default_balance} to balance for selected users.')

admin.site.register(User, UserAdmin)





class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
