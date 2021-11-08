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
        representation = flatten_list(representation, "categories", "category")
        representation = flatten_list(representation, "tags", "tag")
        return representation

    class Meta:
        model = Event
        fields = ('name', "location", "price_range", "short_description", "categories", "tags")


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
