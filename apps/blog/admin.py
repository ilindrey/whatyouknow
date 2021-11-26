from django.contrib import admin

from apps.moderation.admin import ModeratedObjectAdmin

from .models import Post


@admin.register(Post)
class PostAdmin(ModeratedObjectAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'user', 'category')
    search_fields = ('title', 'user__username')
    list_filter = ('category', )
    ordering = ('-date_created', )
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


# admin.site.register(Post, PostAdmin)
