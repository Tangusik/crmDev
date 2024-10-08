from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ListField, CharField, Serializer, EmailField, IntegerField, BooleanField, DateField, DateTimeField, TimeField, DictField


class ClientSerializer(serializers.ModelSerializer):
    state = serializers.IntegerField(required= False)
    class Meta:
        model = Client
        fields = ("__all__")

class UserAuthSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)

class UserEditSerializer(Serializer):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    otchestv = CharField(required=False) #зачем тут ? оно же в тренере
    email = EmailField(required=False)

class ClientEditSerializer(Serializer):
    firstName = CharField(required=False)
    lastName = CharField(required=False)
    middleName = CharField(required=False)
    birthDate = DateField(required=False)
    state = serializers.IntegerField(required= False)
    phone = CharField(required=False)
    email = CharField(required=False)

class TrainerStateEditSerializer(Serializer):
    state = IntegerField(required= True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","last_name", "id", "email")

class TrainerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    class Meta:
        model = Trainer
        fields = ['user', 'middleName', 'birthDate', 'role', 'state', 'phone']
        depth = 1


class TrainerCreationSerializer(serializers.Serializer):
    first_name = CharField()
    last_name = CharField()
    middleName = CharField()
    email = EmailField()
    password = CharField()
    birthDate = DateField()
    role = IntegerField()

class ActivitiesSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer(many=False)
    clients = ClientSerializer(many=True)
    area = serializers.StringRelatedField()
    sport = serializers.StringRelatedField()
    class Meta:
        model = Lesson
        fields = ("__all__")

class GroupSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)
    sportType = serializers.StringRelatedField()
    trainer = TrainerSerializer()
    class Meta:
        model = Group
        fields = ('title','clients', 'trainer','sportType')

class GroupEditSerializer(serializers.Serializer):
    title = CharField(required=False)
    clients = ListField(child = IntegerField(), required=False)
    sportType = IntegerField(required = False)
    trainer = IntegerField(required = False)
    



class LessonSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()
    clients = ClientSerializer(many=True)
    area = serializers.StringRelatedField()
    sport = serializers.StringRelatedField()
    group = GroupSerializer()
    class Meta:
        model = Lesson
        fields = ("__all__")






class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("__all__")

class TrainerStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerState
        fields = ("__all__")

class ClientStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientState
        fields = ("__all__")


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ("__all__")

class SportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportType
        fields = ("__all__")

class AbonementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonement
        fields = ("title","price","duration","lessonCount","sportType", "id")

class AbonementCreationSerializer(serializers.Serializer):
    title = CharField(required=True)
    price = IntegerField(required=True)
    is_duration = BooleanField(required=False)
    duration = IntegerField(required=False)
    duration_type = CharField(required=False)
    is_lesson_count = BooleanField(required=False)
    lesson_count = IntegerField(required=False)
    sport_type = IntegerField(required=True)

class AbonementhistorySerializer(serializers.ModelSerializer):
    abonement = AbonementSerializer()
    class Meta:
        model = PurchaseHistory
        fields = ['abonement', 'purchaseDate', "status", 'activitiesLeft', 'endDate', 'id']


class AbonementAddSerializer(serializers.Serializer):
    abonement = IntegerField(required = True)

class AddBalanceSerializer(serializers.Serializer):
    balance=IntegerField(required =True)

class ClientIdSer(serializers.Serializer):
    id = IntegerField()

class ActCreationSerializer(serializers.Serializer):
    day_of_week = IntegerField()
    time_begin = TimeField()
    time_end = TimeField() 

class GroupCreationSerializer(serializers.Serializer):
    team_name = CharField()
    trainer = IntegerField()
    sport_type = IntegerField()
    area = IntegerField()
    members = ListField(child = IntegerField())
    date_end = DateField()
    acts = ActCreationSerializer(many=True)
    abonements = ListField(child=IntegerField(), required=True)

class PresencesSerializer(serializers.Serializer):
    client = IntegerField(required=True)
    presence = BooleanField(required=True)
    paid_by = IntegerField(required=False, allow_null=True)
    

class MarkSerializer(serializers.Serializer):
    presences = ListField(child = PresencesSerializer() ,required=True)

class PrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ("__all__")

class TarinerLessonsSerializer(serializers.Serializer):
    fut_lessons = ListField(child = LessonSerializer())
    last_lessons = ListField(child = LessonSerializer())
