from rest_framework import serializers
from .models import wish

class wishSerializer(serializers.ModelSerializer):
    class Meta:
        model = wish
        fields = ['id', 'title', 'content', 'category', 'created_at']

    # 예외 처리를 위한 유효성 검사
    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("제목은 필수 입력 항목입니다.")
        if not data.get('content'):
            raise serializers.ValidationError("내용은 필수 입력 항목입니다.")
        if not data.get('category'):
            raise serializers.ValidationError("카테고리는 필수 입력 항목입니다.")
        return data