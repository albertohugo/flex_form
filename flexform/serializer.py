from .models import Form, Object, FormMember, Result
from rest_framework import serializers

class FormSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Form
        fields = ('title', 'status', 'private', 'created_by', 'timestamp',)

class ObjectSerializer(serializers.HyperlinkedModelSerializer):
    form = serializers.ReadOnlyField(source='form.title')
    type = serializers.ChoiceField(choices=Object.OBJECT_TYPES)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Object
        fields = ('form', 'label', 'description', 'type', 'created_by' , 'timestamp',)

class FormMemberSerializer(serializers.HyperlinkedModelSerializer):
    form = serializers.ReadOnlyField(source='form.title')
    role = serializers.ChoiceField(choices=FormMember.OBJECT_TYPES)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = FormMember
        fields = ('form', 'role', 'user',)

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    form = serializers.ReadOnlyField(source='form.title')
    object = serializers.ReadOnlyField(source='object.label')
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Result
        fields = ('form', 'object', 'id_result', 'value', 'created_by' , 'timestamp',)



