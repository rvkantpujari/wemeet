from django.contrib import admin
from .models import BoardMemberStatus


@admin.register(BoardMemberStatus)
class BoardMemberStatusAdmin(admin.ModelAdmin):
	list_display = ['statusId', 'status']

