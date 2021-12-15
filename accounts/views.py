from django.shortcuts import get_object_or_404, render
from accounts.models import User


def profile(request, profile_id):
    user = get_object_or_404(User, id=profile_id)
    print(user)
    context = {
        'user': user,
        'games': [
            {
                'name': 'Новогодняя вечеринка программистов',
                'created_by': 'Олег Тарасов',
                'participants_count': 3,
                'is_admin': False,
                'id': 1,
            },
            {
                'name': 'Devman Party',
                'created_by': 'Юлия Свириденко',
                'participants_count': 5,
                'is_admin': True,
                'id': 2,
            },
        ]
    }
    return render(request, "profile.html", context)
