from django.contrib import admin
from django.db import models
from django import forms

from models import Query, QueryField, QueryOrder, QueryCondition
from utils.admin import ERPModelAdmin as ModelAdmin, ERPTabularInline as TabularInline

class InlineQueryField(TabularInline):
    model = QueryField
    formfield_overrides = {
            models.TextField: {'widget': forms.TextInput},
            }

class InlineQueryOrder(TabularInline):
    model = QueryOrder

class InlineQueryCondition(TabularInline):
    model = QueryCondition

class FormQuery(forms.ModelForm):
    class Meta:
        model = Query

    def __init__(self, *args, **kwargs):
        self.base_fields['url'].widget.attrs['class'] = self.base_fields['url'].widget.attrs['class'].replace('forca_caixa_alta', '')
        self.base_fields['title'].widget.attrs['class'] = self.base_fields['title'].widget.attrs['class'].replace('forca_caixa_alta', '')

        super(FormQuery, self).__init__(*args, **kwargs)

class AdminQuery(ModelAdmin):
    list_display = ('title','kind','content_type')
    inlines = [InlineQueryField, InlineQueryOrder, InlineQueryCondition]
    prepopulated_fields = {'name': ('title',)}
    form = FormQuery

admin.site.register(Query, AdminQuery)

