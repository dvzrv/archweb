import re
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from archweb.main.models import (AltForum, Arch, Donor,
        Mirror, MirrorProtocol, MirrorUrl, MirrorRsync,
        Package, Press, Repo, UserProfile, ExternalProject)

class AltForumAdmin(admin.ModelAdmin):
    list_display = ('language', 'name')
    list_filter = ('language',)
    ordering = ['name']
    search_fields = ('name',)

class DonorAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ('name',)

class MirrorUrlForm(forms.ModelForm):
    class Meta:
        model = MirrorUrl
    def clean_url(self):
        # ensure we always save the URL with a trailing slash
        url = self.cleaned_data["url"].strip()
        if url[-1] == '/':
            return url
        return url + '/'

class MirrorUrlInlineAdmin(admin.TabularInline):
    model = MirrorUrl
    form = MirrorUrlForm
    extra = 3

# ripped off from django.forms.fields, adding netmask ability
ipv4nm_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}(/(\d|[1-2]\d|3[0-2])){0,1}$')
class IPAddressNetmaskField(forms.fields.RegexField):
    default_error_messages = {
        'invalid': u'Enter a valid IPv4 address, possibly including netmask.',
    }

    def __init__(self, *args, **kwargs):
        super(IPAddressNetmaskField, self).__init__(ipv4nm_re, *args, **kwargs)

class MirrorRsyncForm(forms.ModelForm):
    class Meta:
        model = MirrorRsync
    ip = IPAddressNetmaskField(label='IP')

class MirrorRsyncInlineAdmin(admin.TabularInline):
    model = MirrorRsync
    form = MirrorRsyncForm
    extra = 2

class MirrorAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active', 'public', 'isos', 'admin_email', 'supported_protocols')
    list_filter = ('country', 'active', 'public')
    ordering = ['country', 'name']
    search_fields = ('name',)
    inlines = [
            MirrorUrlInlineAdmin,
            MirrorRsyncInlineAdmin,
    ]

class PackageAdmin(admin.ModelAdmin):
    list_display = ('pkgname', 'repo', 'arch', 'maintainer')
    list_filter = ('repo', 'arch', 'maintainer')
    ordering = ['pkgname']
    search_fields = ('pkgname',)

class PressAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    ordering = ['name']
    search_fields = ('name',)

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.register(User, UserProfileAdmin)
admin.site.register(AltForum, AltForumAdmin)
admin.site.register(Donor, DonorAdmin)

admin.site.register(Mirror, MirrorAdmin)
admin.site.register(MirrorProtocol)

admin.site.register(Package, PackageAdmin)
admin.site.register(Press, PressAdmin)
admin.site.register(Arch)
admin.site.register(Repo)
admin.site.register(ExternalProject)

# vim: set ts=4 sw=4 et:
