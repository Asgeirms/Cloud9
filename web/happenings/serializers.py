from rest_framework import serializers

from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='event.name')
    location = serializers.CharField(source='event.location')
    min_price = serializers.IntegerField(source='event.min_price')
    max_price = serializers.IntegerField(source='event.max_price')
    short_description = serializers.CharField(source='event.short_description', allow_blank=True)
    # test = serializers.CharField(default=str(serializers.IntegerField(source='event.min_price').get_value()) + " - " + str(serializers.IntegerField(source='event.max_price').get_value))

    def to_representation(self, instance):
        representation = super(ScheduleSerializer, self).to_representation(instance)
        representation['start_time'] = instance.start_time.strftime("%d/%m/%Y %H:%M")
        representation['end_time'] = instance.end_time.strftime("%d/%m/%Y %H:%M")
        return representation
    
    class Meta:
        model = Schedule
        fields = ('id', 'name', 'start_time', 'end_time', "location", "min_price", "max_price", "short_description" )
