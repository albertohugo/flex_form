from .models import Form, Object, FormMember, Result, IdResult
from rest_framework import serializers
from django.contrib.auth.models import User

class FormSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Form
        fields = ('title', 'status', 'private', 'created_by', 'timestamp',)

class ObjectSerializer(serializers.HyperlinkedModelSerializer):
    #form = serializers.ReadOnlyField(source='form.title')
    type = serializers.ChoiceField(choices=Object.OBJECT_TYPES)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Object
        fields = ('form', 'label', 'description', 'type', 'created_by' , 'timestamp',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class FormMemberSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.ChoiceField(choices=FormMember.OBJECT_TYPES, read_only=True)
    #user = UserSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    form = serializers.ReadOnlyField(source='form.title')

    class Meta:
        model = FormMember
        fields = ('form', 'role', 'user',)

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    form_id = serializers.ReadOnlyField(source='form.id')
    object_id = serializers.ReadOnlyField(source='object.id')
    id_result = serializers.ReadOnlyField(label='id_result', read_only=True)
    class Meta:
        model = Result
        fields = ('form', 'object', 'form_id', 'object_id', 'id_result', 'value', 'created_by' , 'timestamp',)

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    object = serializers.ReadOnlyField(source='object.label')
    class Meta:
        model = Result
        fields = ('object','value', 'image')

class IdResultSerializer(serializers.HyperlinkedModelSerializer):
    response_detail = ResultSerializer(many=True)
    class Meta:
        model = IdResult
        fields = ('id', 'response_detail')

class FlexFormGetSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username', read_only=True)
    object = serializers.StringRelatedField(many=True, read_only=True)
    member = serializers.StringRelatedField(many=True, read_only=True)
    response = IdResultSerializer(many=True, read_only=True)
    class Meta:
        model = Form
        fields = ('id','title', 'status', 'private', 'created_by', 'timestamp','object', 'member', 'response')

class FlexFormSetSerializer(serializers.HyperlinkedModelSerializer):
    #created_by = serializers.ReadOnlyField(source='created_by.username', read_only=True)
    #objects = Object.objects.all()
    #for object in objects:
    #    object.id = serializers.ReadOnlyField(source='object.label', read_only=True)

    class Meta:
        model = None
        #fields = ('form', 'label', 'description', 'type', 'created_by' , 'timestamp',)

#https://www.django-rest-framework.org/api-guide/relations/
