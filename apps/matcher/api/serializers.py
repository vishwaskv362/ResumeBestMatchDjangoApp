"""
Serializers for the resume matcher API.
"""
from rest_framework import serializers
from apps.matcher.models import ResumeData


class ResumeDataSerializer(serializers.ModelSerializer):
    """Serializer for resume matching requests."""
    
    class Meta:
        model = ResumeData
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
    
    def validate_threshold(self, value):
        """Validate threshold is a valid number."""
        try:
            threshold_val = float(value)
            if not 0 <= threshold_val <= 1:
                raise serializers.ValidationError(
                    "Threshold must be between 0 and 1"
                )
        except ValueError:
            raise serializers.ValidationError(
                "Threshold must be a valid number"
            )
        return value
    
    def validate_category(self, value):
        """Validate category is either 'resume' or 'job_search'."""
        valid_categories = ['resume', 'job_search']
        if value not in valid_categories:
            raise serializers.ValidationError(
                f"Category must be one of: {', '.join(valid_categories)}"
            )
        return value
    
    def validate_noOfMatches(self, value):
        """Validate noOfMatches is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError(
                "Number of matches must be greater than 0"
            )
        return value


class MatchResultSerializer(serializers.Serializer):
    """Serializer for match results."""
    id = serializers.CharField()
    path = serializers.CharField()
    score = serializers.CharField()


class ResumeMatchResponseSerializer(serializers.Serializer):
    """Serializer for the resume match response."""
    count = serializers.IntegerField()
    metadata = serializers.DictField()
    results = MatchResultSerializer(many=True)
    status = serializers.CharField()
    error_message = serializers.CharField(required=False)
