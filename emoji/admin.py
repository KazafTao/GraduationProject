from django.contrib import admin

# from django.contrib.auth.models import User
from .models import AsciiEmoji, Tag, EmojiSeries, SeriesElement, User, Material


class AsciiAdmin(admin.ModelAdmin):
    list_display = ('content',)
    list_per_page = 10


class AsciiInLine(admin.TabularInline):
    model = AsciiEmoji


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'hits')
    inlines = [AsciiInLine]


class ElementInLine(admin.TabularInline):
    model = SeriesElement
    # 默认添加的选项数
    extra = 2


class EmojiSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'num')
    search_fields = ['=name']
    list_filter = ['name']
    inlines = [ElementInLine]


class SeriesElementAdmin(admin.ModelAdmin):
    list_display = ('series', 'path')
    list_filter = ['series']
    search_fields = ['path']

class MaterialAdmin(admin.ModelAdmin):
    list_per_page = 600

# 在后台注册模型
admin.site.register(User)
admin.site.register(AsciiEmoji, AsciiAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(EmojiSeries, EmojiSeriesAdmin)
admin.site.register(SeriesElement, SeriesElementAdmin)
# admin.site.register(Material)
admin.site.register(Material,MaterialAdmin)