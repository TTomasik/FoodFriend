from django.contrib import admin
from foodfriend.models import UserExtend



@admin.register(UserExtend)
class UserExtendAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_url', 'age', 'sex', 'weight', 'height', 'creation_date', 'calories')

    def image_url(self, obj):
        return "<img src ='/{}' width='50' height='50' >".format(obj.avatar)

    image_url.allow_tags = True



