from rest_framework import serializers

from .models import Schedule, Event, AccessibilityTag, EventCategory

class InterestCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = EventCategory
        fields = ['category']

class RequirementCategorySerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source="name")

    class Meta:
        model = AccessibilityTag
        fields = ['tag']


class EventSerializer(serializers.ModelSerializer):
    accessibility_tags = RequirementCategorySerializer(many=True)
    event_categories = InterestCategorySerializer(many=True)
    price_range = serializers.CharField(source="name") #any source will do, it gets changed in representation anyway

    def to_representation(self, instance):
        representation = super(EventSerializer, self).to_representation(instance)
        if instance.max_price == 0:
            representation['price_range'] = "FREE"
        else:
            representation['price_range'] = str(instance.min_price) + " - " + str(instance.max_price)
        #Changes the format of categories and tags so that it can be read in excel
        def flatten_list(representation, list_name, item_name):
            copied_list = representation[list_name].copy()
            representation[list_name] = ""
            for od in copied_list:
                representation[list_name] += od.get(item_name) + ", "
            if len(representation[list_name]) > 1:
                representation[list_name] = representation[list_name][:-2]
            return representation
        representation = flatten_list(representation, "accessibility_tags", "tag")
        representation = flatten_list(representation, "event_categories", "category")
        return representation

    class Meta:
        model = Event
        fields = ('name', "location", "price_range", "short_description", "accessibility_tags", "event_categories")


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
