from dataclasses import fields
from rest_framework import serializers
from projects.models import Mod, Tag, Review
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ModSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Mod
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializers = ReviewSerializer(reviews, many=True)
        return serializers.data
