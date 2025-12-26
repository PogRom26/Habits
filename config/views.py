# config/views.py
from django.http import JsonResponse
from django.views import View

class APIRootView(View):
    def get(self, request):
        api_info = {
            "name": "Habit Tracker API",
            "version": "1.0.0",
            "description": "API для трекера привычек по книге 'Атомные привычки'",
            "endpoints": {
                "authentication": {
                    "register": "/api/users/register/",
                    "login": "/api/users/login/",
                    "token_refresh": "/api/token/refresh/",
                },
                "habits": {
                    "my_habits": "/api/habits/",
                    "public_habits": "/api/habits/public/",
                    "habit_detail": "/api/habits/{id}/",
                    "complete_habit": "/api/habits/{id}/complete/",
                    "stats": "/api/habits/stats/",
                },
                "users": {
                    "profile": "/api/users/profile/",
                    "connect_telegram": "/api/users/connect-telegram/",
                },
                "documentation": {
                    "swagger": "/swagger/",
                    "redoc": "/redoc/",
                },
                "admin": "/admin/",
            }
        }
        return JsonResponse(api_info)