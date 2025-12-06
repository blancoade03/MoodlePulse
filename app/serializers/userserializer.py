from rest_framework import serializers
from app.models import user 

class userserializer(serializers.Serializer):

    class Meta:
        model = user 
        fields = '__all__' 
