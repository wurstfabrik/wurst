from django.contrib import admin

from .models import Issue, IssueType, Priority, Project, Status


class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'nouns')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'title', 'priority', 'status')
    list_filter = ('project', 'type', 'status')


class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'nouns')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'value')
    list_list_filter = ('category',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'prefix')


admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Project, ProjectAdmin)
