from .models import Form
from rest_framework import serializers

class FormSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='username'
    )
    class Meta:
        model = Form
        fields = ('title', 'status', 'private', 'created_by', 'timestamp',  )