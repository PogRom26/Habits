from django.contrib import admin
from django.utils.html import format_html
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_email', 'action', 'place', 'time',
        'is_pleasant', 'periodicity', 'is_public', 'created_at'
    )
    list_filter = (
        'is_pleasant', 'is_public', 'periodicity',
        'created_at', 'user'
    )
    search_fields = ('action', 'place', 'user__email')
    readonly_fields = ('created_at', 'last_reminder')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Детали привычки', {
            'fields': ('is_pleasant', 'related_habit', 'periodicity',
                       'reward', 'duration', 'is_public')
        }),
        ('Даты', {
            'fields': ('created_at', 'last_reminder'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Пользователь'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # при редактировании существующего объекта
            return readonly_fields + ('user',)
        return readonly_fields


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit_action', 'completed_at', 'was_successful')
    list_filter = ('was_successful', 'completed_at', 'habit')
    search_fields = ('habit__action',)
    readonly_fields = ('completed_at',)

    def habit_action(self, obj):
        return obj.habit.action

    habit_action.short_description = 'Привычка'