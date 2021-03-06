# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

__author__ = 'Evren Esat Ozkan'


from django.contrib.auth.models import User
from django.contrib import admin
from utils.admin import admin_register
from models import *
from datetime import datetime

class PromotionCodeAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'puser', 'sender','price','percentage','expiry_date','timestamp','type','used','active')
    search_fields = ['code', ]
    list_filter = ['type', ]
    raw_id_fields = ['puser','sender']
    save_on_top = True

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id','admin_image', 'name', 'place', 'type')
    search_fields = ['name', ]
    list_filter = ['type', ]
    raw_id_fields = ['place']
    save_on_top = True



class GeoLocationAdmin(admin.ModelAdmin):
    list_display = ('name','iso', 'id', 'type')
    search_fields = ['=name', ]
    list_filter = ['type','iso' ]
    raw_id_fields = ['parent']
    save_on_top = True



class TagTranslationAdmin(admin.ModelAdmin):
    list_display = ('tag','lang', 'translation',)
    search_fields = ['translation', ]
    list_filter = ['lang','tag' ]
    save_on_top = True



class TagTranslationInline(admin.TabularInline):
    model = TagTranslation

class PhotoInline(admin.TabularInline):
    model = Photo



class DescriptionInline(admin.TabularInline):
    model = Description


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('lang', 'place')
    search_fields = ['text', ]
    list_filter = ['lang', ]
    raw_id_fields = ['place']
    save_on_top = True


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'read','timestamp','status')
    search_fields = ['text', ]
    list_filter = ['status', ]
    date_hierarchy = 'timestamp'
    raw_id_fields = ['sender','receiver','replyto','place']
    save_on_top = True
#
#    def save_model(self, request, obj, form, change):
#        obj.save()

class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('writer', 'person', 'active','timestamp','status')
    search_fields = ['text', ]
    list_filter = ['status', ]
    date_hierarchy = 'timestamp'
    save_on_top = True

class PlaceReviewAdmin(admin.ModelAdmin):
    list_display = ('writer', 'place', 'active','timestamp','status')
    search_fields = ['text', ]
    list_filter = ['status', ]
    raw_id_fields = ['place','writer']
    date_hierarchy = 'timestamp'
    save_on_top = True



class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'host', 'guest', 'place', 'valid', 'status')
    search_fields = ['summary', ]
    list_filter = ['status','valid', ]
    raw_id_fields = ['host','guest','reservation','place']
    actions = ['odeme_onayla',]
    save_on_top = True
    readonly_fields=['timestamp','confirmation_date','rejection_date','guest_ok_date','payment_notification_date','payment_notification_date','payment_confirmation_date','payment_transfer_date']
    def odeme_onayla(self, request, queryset):
        booking = queryset[0]
        booking.status = 10
        booking.payment_confirmation_date = datetime.now()
        booking.save()
        booking.send_booking_request(request)
        self.message_user(request, "Rezervasyon başarıyla güncellendi. İstek ev sahibine bildirildi.")
    odeme_onayla.short_description = u'İşaretli rezervasyonun banka transferi ile yapılan ödemesini onayla.'


class ReservedDatesAdmin(admin.ModelAdmin):
    list_display = ('place', 'start','end','type')
    raw_id_fields = ['place']
#    search_fields = ['', ]
    list_filter = ['type', ]
    save_on_top = True
    date_hierarchy = 'start'


class SessionalPriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'place','active')
#    search_fields = ['name', ]
    list_filter = ['active', ]
    raw_id_fields = ['place']
    save_on_top = True



class BookingInline(admin.TabularInline):
    model = Booking
import csv
from django.http import HttpResponse
def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        if not queryset:
            queryset = modeladmin.model.objects.all()
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv
export_as_csv_action.short_description = "Kayıtları csv olarak kaydet"

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_image','lang', 'city', 'price','currency','published', 'active', 'size', 'timestamp','last_modified')
    search_fields = ['title','i18_tags' ]
    list_filter = ['type', 'space', 'bedroom', 'translated','active','published']
    save_on_top = True

    raw_id_fields=('owner', 'placement')
    readonly_fields=['timestamp','last_modified']
    #save_as=True
    #ordering = ['',]
    #description=''
    list_per_page=25
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PhotoInline, DescriptionInline]
    #list_display_links = ('','')
    date_hierarchy = 'timestamp'
    #list_select_related=False
    filter_horizontal = ('tags',)




    def save_model(self, request, obj, form, change):
        desc = obj.descriptions.filter(lang=obj.lang)
        if desc:
            desc[0].title = obj.title
            desc[0].text = obj.description
            desc[0].save()
        obj.pick_primary_photo()
        obj.translation_check()
        obj.save()
        obj.invalidate_caches()


class TagInline(admin.TabularInline):
    model = Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'category')
    search_fields = ['name', ]
    list_filter = ['category', ]
    inlines = [TagTranslationInline]


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',  'main', 'active','factor')
    search_fields = ['name','code' ]
    list_filter = ['active', ]



class TagCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ['active', ]
    inlines = [TagInline,]

class PaymentSelectionInline(admin.StackedInline):
    model = PaymentSelection

class ProfileInline(admin.StackedInline):
    model = Profile

class PlaceInline(admin.TabularInline):
    model = Place
    fields = ['title']
    readonly_fields = ['title']

    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields=('user', )
    list_display = ('full_name', )
    search_fields = ['full_name', 'user__email']
    save_on_top = True
    actions = ['yerine_gec',export_as_csv_action("Seçilen kayıtları CSV olarak kaydet", fields=['full_name','city','cell','phone','user'], header=False),]

    def yerine_gec(self, request, queryset):
        m=queryset.all()[0]
        sonuc= HttpResponseRedirect("/job/mtx/?id=%s" % m.user.id)
#        assert 0, sonuc
        return sonuc
    yerine_gec.short_description = u'İşaretli kullanıcının yerine geç.'





class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser')
    filter_horizontal = ['user_permissions','groups']
    search_fields = ['first_name','last_name', 'email']
    inlines = [PaymentSelectionInline, ProfileInline, PlaceInline]



admin.site.unregister(User)
admin.site.register(User, UserAdmin)



class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'type','receiver_type','sender_type' ,'active', 'timestamp')
#    search_fields = ['', ]
    list_filter = ['receiver_type','sender_type','active' ]
    date_hierarchy = 'timestamp'
    save_on_top = True




admin_register(admin, namespace=globals())
