from rest_framework import serializers

from .models import Schedule, Event, RequirementCategory, InterestCategory

class InterestCategorySerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source="name")

    class Meta:
        model = InterestCategory
        fields = ['tag']

class RequirementCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = RequirementCategory
        fields = ['category']


class EventSerializer(serializers.ModelSerializer):
    categories = RequirementCategorySerializer(source="requirement_categories", many=True)
    tags = InterestCategorySerializer(source="interest_categories", many=True)

    class Meta:
        model = Event
        fields = ('name', "location", "min_price", "max_price", "short_description", "categories", "tags")


class ScheduleSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    def to_representation(self, instance):
        representation = super(ScheduleSerializer, self).to_representation(instance)
        representation['start_time'] = instance.start_time.strftime("%d/%m/%Y %H:%M")
        representation['end_time'] = instance.end_time.strftime("%d/%m/%Y %H:%M")
        return representation
    
    class Meta:
        model = Schedule
        fields = ('id','start_time', 'end_time', 'event' )
