from django.contrib import admin
from django.contrib.auth.models import User

from .models import Wallet
from .models import Transaction


class WalletInline(admin.TabularInline):
    model = Wallet
    extra = 0  # Чтобы избежать отображения дополнительных пустых форм
    show_change_link = True


class UserAdmin(admin.ModelAdmin):
    inlines = [WalletInline]


class WithdrawTransactionInline(admin.TabularInline):
    verbose_name = 'Withdraw transaction'
    model = Transaction
    extra = 0
    fk_name = 'sender_wallet'
    readonly_fields = ('recipient_wallet', 'amount', 'date')
    can_add_related = False
    can_delete = False

class ReceiveTransactionInline(admin.TabularInline):
    verbose_name = 'Receive transaction'
    model = Transaction
    extra = 0
    fk_name = 'recipient_wallet'
    readonly_fields = ('sender_wallet', 'amount', 'date')
    can_add_related = False
    can_delete = False

class WalletAdmin(admin.ModelAdmin):
    inlines = [
        WithdrawTransactionInline,
        ReceiveTransactionInline,
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction)
