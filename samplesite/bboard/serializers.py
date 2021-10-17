from rest_framework import serializers
from .models import Bb, Rubric


class RubricSerializer(serializers.ModelSerializer):

	class Meta:

		model = Rubric
		fields = ('id', 'name')


class BbSerializer(serializers.ModelSerializer):

	rubric = RubricSerializer()

	class Meta:

		model = Bb
		fields = '__all__'
