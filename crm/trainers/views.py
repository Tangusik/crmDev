import datetime
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from .models import Client, Team, Trainer, Activity, News, Area, SportType, Abonement, TrainerState, ClientState, Role, \
    Presence, PurchaseHistory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q
from .serializers import ClientSerializer
from .serializers import ScheduleSerializer
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main'))
    else:
        return render(request, 'trainers/login.html')


def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('login_page'))
    else:
        return HttpResponseRedirect(reverse('main'))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))


def main(request):
    if request.user.is_authenticated:
        news = News.objects.filter(pub_date__lte=timezone.now(), expiry_date__gt=timezone.now())
        areas = Area.objects.all()
        sport_types = SportType.objects.all()
        abonements = Abonement.objects.all()
        roles = Role.objects.all()
        trainer_states = TrainerState.objects.all()
        clients_states = ClientState.objects.all()

        if request.user.trainer.role.name == "директор":
            context = {
                'userinfo': request.user,
                'trainer': request.user.trainer,
                'news': news,
                'areas': areas,
                'sport_types': sport_types,
                'abonements': abonements,
                'roles': roles,
                'trainer_states': trainer_states,
                'clients_states': clients_states
            }

        elif request.user.trainer.role.name == "тренер":

            teams = Team.objects.filter(trainer=request.user.trainer)
            clients = Client.objects.all()
            current_time = datetime.datetime.now()
            current_time = current_time.time()

            try:
                act = Activity.objects.filter(trainer=request.user.trainer,
                                              status="Состоится",
                                              act_date__gte=datetime.date.today()).order_by('act_date', 'act_time_begin')[0]

            except :
                act = None

            ended_acts = Activity.objects.filter(trainer=request.user.trainer,
                                                 status="Состоится",
                                                 act_date__lt=datetime.date.today(),
                                                 act_time_end__lt=current_time).order_by('act_date', 'act_time_begin')
            context = {'userinfo': request.user,
                       'act': act,
                       'role_trainer': request.user.trainer,
                       'trainer': request.user.trainer,
                       'news': news,
                       'teams': teams,
                       'clients': clients,
                       'ended_acts': ended_acts}

        return render(request, 'trainers/main.html', context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def clients(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()
        teams = Team.objects.all()
        trainers = Trainer.objects.filter(role__name="тренер")
        sport_types = SportType.objects.all()
        areas = Area.objects.all()
        context = {'clients': clients,
                   'teams': teams,
                   'trainers': trainers,
                   'sport_types': sport_types,
                   'areas': areas}

        return render(request, "trainers/clients.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def client_info(request, client_id):
    if request.user.is_authenticated:
        client = get_object_or_404(Client, pk=client_id)
        active_abonements = PurchaseHistory.objects.filter(client=client, status="активен")
        abonements = Abonement.objects.all()
        context = {'client': client,
                   'active_abonements': active_abonements,
                   'abonements':abonements}
        return render(request, "trainers/clients_info.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def client_add_action(request):
    client_name = request.POST['client_name']
    client_surname = request.POST['client_surname']
    client_birthdate = request.POST['client_birthdate']
    try:
        Client.objects.create(first_name=client_name, last_name=client_surname, birth_date=client_birthdate)
        return HttpResponseRedirect(reverse('clients'))
    except:
        return HttpResponseRedirect(reverse('client_add'))


def team_creation(request):
    team_name = request.POST.get('title', 'group')
    sport_type = request.POST['sport_type']
    members = request.POST.getlist('members')
    trainer = request.POST['trainer']
    date_end = request.POST['date_end']
    area = request.POST['area']
    # ___________________Нужно изменить
    days = request.POST.getlist('days')
    act_begin_time = request.POST['act_begin_time']
    act_end_time = request.POST['act_end_time']
    # __________________________________

    tr = get_object_or_404(Trainer, pk=trainer)
    sp_type = get_object_or_404(SportType, pk=sport_type)
    area = get_object_or_404(Area, pk=area)
    team = Team.objects.create(name=team_name, trainer=tr, sport_type=sp_type)
    for client in members:
        team.clients.add(client)

    date1 = datetime.date.today()
    date2 = datetime.datetime.strptime(date_end, '%Y-%m-%d')

    while date1 <= date2.date():
        if str(date1.weekday()) in days:
            act = Activity(act_date=date1, act_time_begin=act_begin_time,
                           act_time_end=act_end_time,
                           trainer=tr, area=area,
                           status="Состоится",
                           sport=sp_type)
            act.save()
            for client in members:
                act.clients.add(client)
            act.save()
        date1 = date1 + datetime.timedelta(days=1)

    return HttpResponseRedirect(reverse('clients'))


def trainers(request):
    if request.user.is_authenticated:
        status = TrainerState.objects.all()
        sport = SportType.objects.all()
        director = Trainer.objects.filter(role__name="директор")
        trainers = Trainer.objects.exclude(role__name="директор")

        if request.GET.get('state'):
            trainers = trainers.filter(state__name=request.GET.get('state'))

        if request.GET.get('sport'):
            sp = sport.filter(title=request.GET.get('sport'))
            trainers = sp.filter()

        today = date.today()
        trainers_birth = Trainer.objects.order_by('birthdate')
        upcoming_birthdays = []
        today_birthdays = []
        for trainer in trainers_birth:
            # дата> рождения тренера в этом году
            birthdate_this_year = date(today.year, trainer.birthdate.month, trainer.birthdate.day)
            if birthdate_this_year < today:
                birthdate_this_year = date(today.year + 1, trainer.birthdate.month, trainer.birthdate.day)
            # оставшееся время до дня рождения
            time_to_birthday = (birthdate_this_year - today).days
            if time_to_birthday <= 7 & time_to_birthday != 0:
                upcoming_birthdays.append(trainer)
            if time_to_birthday == 0:
                today_birthdays.append(trainer)

        trainers_search = []
        query = request.GET.get('q')
        if query:
            trainers_search = Trainer.objects.filter(
                Q(user__first_name__icontains=query) | Q(user__email__icontains=query))

        roles = Role.objects.all()

        context = {'trainers': trainers,
                   'status': status,
                   'sport': sport,
                   'upcoming_birthdays': upcoming_birthdays,
                   'today_birthdays': today_birthdays,
                   'trainers_search': trainers_search,
                   'query': query,
                   'user': request.user,
                   'director': director,
                   'roles': roles}

        return render(request, "trainers/trainers.html", context)
    else:
        return HttpResponseRedirect(reverse('login_page'))


def trainers_add_action(request):
    trainer_name = request.POST['name']
    trainer_last_name = request.POST['last_name']
    trainer_otchestv = request.POST['otchestv']
    trainer_mail = request.POST['mail']
    trainer_pass = request.POST['password']
    trainer_birthdate = request.POST['birth_date']
    role = request.POST['role']
    role = get_object_or_404(Role, pk=role)
    try:
        user = User.objects.create_user(username=trainer_mail, email=trainer_mail, password=trainer_pass)
        user.last_name = trainer_last_name
        user.first_name = trainer_name
        user.save()
        trainer = Trainer(user=user, otchestv=trainer_otchestv,
                          birthdate=trainer_birthdate,
                          role=role,
                          state=TrainerState.objects.get(id=1))
        trainer.save()
        return HttpResponseRedirect(reverse('trainers'))
    except:
        return HttpResponseRedirect(reverse('trainers'))


# def schedule(request):
#     if request.user.is_authenticated:
#         activities = Activity.objects.all()
#         context = [activity.to_json() for activity in activities]
#         context = json.dumps(context)
#         return render(request, "trainers/schedule.html", {'activities': context})
#     else:
#         return HttpResponseRedirect(reverse('login_page'))
# def schedule(request):
#     if request.user.is_authenticated:
#         month = request.POST['month']
#         activities = Activity.objects.all()
#         context = [activity.to_json() for activity in activities]
#         return JsonResponse(context, safe=False)
#     else:
#         return HttpResponseRedirect(reverse('login_page'))

# def schedule(request):
#     if request.user.is_authenticated:
#         activities = Activity.objects.filter(act_date__month=1)
#         context = [activity.to_json() for activity in activities]
#         return JsonResponse(context, safe=False)
#     else:
#         return HttpResponseRedirect(reverse('login_page'))
# @csrf_exempt
# def schedule(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             data = json.loads(request.body)
#             selected_month = data.get('month')
#             activities = Activity.objects.filter(act_date__month=selected_month)
#         else:
#             activities = Activity.objects.all()
#
#         context = [activity.to_json() for activity in activities]
#         json_response = JsonResponse(context, safe=False)
#         return render(request, "trainers/schedule.html", {'activities': json_response})
#     else:
#         return HttpResponseRedirect(reverse('login_page'))
def schedule(request):
    if request.user.is_authenticated:
        selected_month = int(request.GET.get('selectedMonth', 0)) + 1
        print("selected_month",selected_month)
        activities = Activity.objects.filter(act_date__month=selected_month).order_by('act_date', 'act_time_begin')
        context = [activity.to_json() for activity in activities]
        context = json.dumps(context)
        print(context)
        return render(request, "trainers/schedule.html", {'activities': context})
#         return JsonResponse({'activities': context})
    else:
        return HttpResponseRedirect(reverse('login_page'))




def sport_type_creation(request):
    title = request.POST['title']
    sport_type = SportType(title=title)
    sport_type.save()
    return HttpResponseRedirect(reverse('main'))


def sport_type_delete(request):
    if request.method == 'POST':
        type_title = request.POST.get('type_title')
        try:
            sport_type = SportType.objects.get(title=type_title)
            sport_type.delete()
            return HttpResponseRedirect(reverse('main'))
        except SportType.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def area_creation(request):
    address = request.POST['address']
    area = Area(address=address)
    area.save()
    return HttpResponseRedirect(reverse('main'))


def area_delete(request):
    if request.method == 'POST':
        area_address = request.POST.get('area_address')
        try:
            area = Area.objects.get(address=area_address)
            area.delete()
            return HttpResponseRedirect(reverse('main'))
        except Area.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def role_creation(request):
    role_name = request.POST['role']
    role = Role(name=role_name)
    role.save()
    return HttpResponseRedirect(reverse('main'))


def role_delete(request):
    if request.method == 'POST':
        role_name = request.POST.get('role_name')
        try:
            role = Role.objects.get(name=role_name)
            role.delete()
            return HttpResponseRedirect(reverse('main'))
        except Role.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def trainer_state_creation(request):
    state_name = request.POST['trainer_state']
    state = TrainerState(name=state_name)
    state.save()
    return HttpResponseRedirect(reverse('main'))


def trainer_state_delete(request):
    if request.method == 'POST':
        trainer_state = request.POST.get('trainer_state')
        try:
            state = TrainerState.objects.get(name=trainer_state)
            state.delete()
            return HttpResponseRedirect(reverse('main'))
        except TrainerState.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def client_state_creation(request):
    state_name = request.POST['client_state']
    state = ClientState(name=state_name)
    state.save()
    return HttpResponseRedirect(reverse('main'))


def client_state_delete(request):
    if request.method == 'POST':
        client_state = request.POST.get('client_state')
        try:
            state = ClientState.objects.get(name=client_state)
            state.delete()
            return HttpResponseRedirect(reverse('main'))
        except ClientState.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def abonement_creation(request):
    title = request.POST['title']
    price = request.POST['price']
    sport = request.POST['sport']
    sport = get_object_or_404(SportType, pk=sport)
    is_duration = request.POST.get('duration_check', False)
    is_count = request.POST.get('count_check', False)

    if is_count == 'on':
        count = request.POST['count']
    else:
        count = None

    if is_duration == 'on':
        duration = request.POST['duration']
        duration_type = request.POST['duration_type']
        if duration_type == 'days':
            dur = timedelta(days=int(duration))
        elif duration_type == 'weeks':
            dur = timedelta(weeks=int(duration))
        elif duration_type == 'month':
            dur = timedelta(days=int(duration) * 30)
    else:
        dur = None

    abonement = Abonement.objects.create(title=title, price=price, lesson_count=count, duration=dur, sport=sport)
    abonement.save()

    return HttpResponseRedirect(reverse('main'))


def abonement_delete(request):
    if request.method == 'POST':
        abonement_title = request.POST.get("abonement_title")
        try:
            abonement = Abonement.objects.get(title=abonement_title)
            abonement.delete()
            return HttpResponseRedirect(reverse('main'))
        except Abonement.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('main'))


def mark(request, activity_id):
    near_act = Activity.objects.get(id=activity_id)
    clients_id = request.POST.getlist('clients')
    for client in clients_id:

        if client not in near_act.clients.all():
            client = get_object_or_404(Client, pk=client)
            client_presence = Presence(client=client, activity=near_act, presence=True)
            client_presence.save()
        else:
            client = get_object_or_404(Client, pk=client)
            presence = Presence.objects.create(client=client, activity=near_act,presence = True)
            presence.save()

        checkout_abonement(client.id)

        near_act.status = 'Проведено'
        near_act.save()
        return HttpResponseRedirect(reverse('main'))


def edit(request):
    name = request.POST['name']
    last_name = request.POST['last_name']
    otchestv = request.POST['otchestcv']
    email = request.POST['email']

    request.user.first_name = name
    request.user.last_name = last_name
    request.user.email = email
    request.user.username = email
    request.user.save()

    request.user.trainer.otchestv = otchestv
    request.user.trainer.save()
    return HttpResponseRedirect(reverse('main'))


def add_balance(request, client_id):
    added_money = request.POST['added_money']
    client=get_object_or_404(Client, pk=client_id)
    client.balance += int(added_money)
    client.save()
    return HttpResponseRedirect(reverse('client_info', args=[client_id]))

def buy_abonement(request, client_id):
    client = get_object_or_404(Client, pk = client_id)
    abonement_id = request.POST['abonement']
    abonement = get_object_or_404(Abonement, pk = abonement_id)

    purchase_date = request.POST['date']
    purchase_date=datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date()

    if purchase_date >datetime.date.today():
        PurchaseHistory.objects.create(client=client, abonement=abonement, status="на будущее",
                                           activities_left=abonement.lesson_count,
                                           date_of_end=purchase_date + abonement.duration,
                                   purchase_date=purchase_date)
    else:
        PurchaseHistory.objects.create(client=client, abonement=abonement, status="активен",
                                       activities_left=abonement.lesson_count,
                                       date_of_end=purchase_date + abonement.duration,
                                       purchase_date=purchase_date)

    client.balance -= abonement.price
    client.save()
    return HttpResponseRedirect(reverse('client_info', args=[client_id]))

def delete_abonement(request, abonement_id, client_id):
    ab = PurchaseHistory.objects.get(id=abonement_id)
    ab.delete()
    return HttpResponseRedirect(reverse('client_info', args=[client_id]))

def checkout_abonement(client_id):
    client = get_object_or_404(Client, pk=client_id)
    active_abonements = PurchaseHistory.objects.filter(client=client, status="активен")
    for abonement in active_abonements:

        if abonement.abonement.duration != 0:
            if datetime.date.today() > abonement.date_of_end:
                abonement.status = 'прошедший'

        if abonement.abonement.lesson_count != 0:
            lessons = 0
            all_activities = Presence.objects.filter(client=client)
            for act in all_activities:
                if act.activity.act_date > abonement.purchase_date and act.activity.sport == abonement.abonement.sport :
                    lessons += 1

            abonement.activities_left = abonement.abonement.lesson_count - lessons
            if abonement.activities_left == 0:
                abonement.status = 'прошедший'
            abonement.save()

@api_view(['GET','POST'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, context={'request': request},many=True)
        return JsonResponse(serializer.data, safe = False)

    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        else:
             Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
