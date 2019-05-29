from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'description')
    extra = 2      # 一次能更改几个
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    ''' 继承并调用过滤器，只显示自己创建的分类 '''

    #  过滤器名字
    title = '分类过滤器'
    # 查询时URL参数的名字
    parameter_name = 'owner_category'

    # 获取id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    # 展示页面字段及顺序设置，外健category 需要在model里设置__str__ 属性来人性化显示
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator', 'owner'
    ]
    # 点击进入编辑页面的字段，和自定义的 orerator函数功能一样
    list_display_links = []

    # 调用了自定义的过滤器
    list_filter = [CategoryOwnerFilter]
    # __ 可调用关联模型字段
    search_fields = ['title', 'category__name']

    # 在上、下显示增删改
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    '''
        fields = (
            ('category', 'title'),
            'description',
            'status',
            'content',
            'tags',
        )
    '''
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'description',
                'content'
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tags', ),
        })
    )
    filter_vertical = ('tags', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # 自定义css
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
