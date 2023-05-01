from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from .models import Evaluation

# Register your models here.

class RatingFilter(SimpleListFilter):
    title = _('user rating choice')
    parameter_name = 'user_rating_choice'

    def lookups(self, request, model_admin):
        return (
            ('U', _('Útil')),
            ('N', _('No útil')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'U':
            return queryset.filter(user_rating_choice='U')
        if self.value() == 'N':
            return queryset.filter(user_rating_choice='N')


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'gpt_answer', 'user_rating_choice', 'timestamp')
    list_filter = (RatingFilter, 'timestamp', 'user')
    search_fields = ('user__username', 'question', 'answer__text', 'gpt_answer')

admin.site.register(Evaluation, EvaluationAdmin)
