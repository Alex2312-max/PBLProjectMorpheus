from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from updatePage.models import UpdatePage
from processing.models import Schedule


class empty_schedule:
    def __init__(self, sq = 0, ids = 0, sh = 0):
        self.Slept_hours = sh
        self.IDS = ids
        self.Sleep_Quality = sq


def userPage_view(request, id):
    user = get_user_model()
    users = user.objects.all()
    user_data = UpdatePage.objects.all()
    if Schedule.objects.filter(user=users[id]).exists():
        user_schedule = Schedule.objects.filter(user=users[id]).reverse()[0]
        hours_generated = [
            user_schedule.hour0_Generated,
            user_schedule.hour1_Generated,
            user_schedule.hour2_Generated,
            user_schedule.hour3_Generated,
            user_schedule.hour4_Generated,
            user_schedule.hour5_Generated,
            user_schedule.hour6_Generated,
            user_schedule.hour7_Generated,
            user_schedule.hour8_Generated,
            user_schedule.hour9_Generated,
            user_schedule.hour10_Generated,
            user_schedule.hour11_Generated,
            user_schedule.hour12_Generated,
            user_schedule.hour13_Generated,
            user_schedule.hour14_Generated,
            user_schedule.hour15_Generated,
            user_schedule.hour16_Generated,
            user_schedule.hour17_Generated,
            user_schedule.hour18_Generated,
            user_schedule.hour19_Generated,
            user_schedule.hour20_Generated,
            user_schedule.hour21_Generated,
            user_schedule.hour22_Generated,
            user_schedule.hour23_Generated
        ]
    else:
        hours_generated = [0] * 24
        user_schedule = empty_schedule()

    return render(request, 'userPage/userPage.html', {'user_data': user_data[id-1], 'data': users[id], 'schedule':
                                                      user_schedule, 'hours_generated': hours_generated})
