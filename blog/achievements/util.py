# Данный файл созда для сeрвис-функция приложения achievements

from users.models import CustomUser 
from achievements.models import Achievement

def first_post_achievement(user_id):
    achievement = Achievement.objects.get(name='Первый пост')
    print('dadadadad')

    customuser = CustomUser.objects.get(id=user_id)
    try:
        print(customuser.achievements.all + "www")
        customuser.achievements.filter(achievement_id=achievement.id)
    except:
        customuser.achievements.add(achievement)
        customuser.save()
        print(customuser.achievements)
