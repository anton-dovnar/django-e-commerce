# -*- coding: utf-8 -*-
from django.contrib import admin

from shop.models import Category, Photo, Product, Size

admin.site.index_template = 'memcache_status/admin_index.html'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'name',
        'slug',
        'description',
        'price',
        'available',
        'created',
        'updated',
    )
    list_filter = ('category', 'available', 'created', 'updated')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    list_filter = ('product',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size')
    list_filter = ('product',)
