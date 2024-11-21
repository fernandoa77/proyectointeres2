from django.contrib import admin
from .models import AmortizationTable, SinkingFund

@admin.register(AmortizationTable)
class AmortizationTableAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(SinkingFund)
class SinkingFundAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
