from django.db import models
from django.utils import timezone

# soft delete를 위한 manager
class SoftDeleteManager(models.Manager):
    # 기본적으로 삭제되지 않은 항목만 조회
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    # 삭제된 항목 포함하여 모든 항목 조회
    def all_with_deleted(self):
        return super().get_queryset()

class wish(models.Model):
    # 데이터베이스에는 영어 값이 저장되고, 사용자 인터페이스에는 한글 표시 값이 제공
    # -> 다국어 지원과 사용자 친화적 인터페이스 제공에 유용

    # 카테고리
    CATEGORY_CHOICES = [
        ('career', '진로'),
        ('health', '건강'),
        ('relationships', '인간 관계'),
        ('money', '돈'),
        ('goals', '목표'),
        ('academics', '학업/성적'),
        ('others', '기타'),
    ]
    # WISH의 상태
    WISH_STATUS_CHOICES = [
        ('pending', '보류'),
        ('approved', '승인'),
        ('rejected', '거절'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        # 기본값을 기타로 설정
        default='others'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirm = models.CharField(
        max_length=10,
        choices=WISH_STATUS_CHOICES,
        # 기본값을 보류로 설정
        default='pending'
    )
    # 소프트 삭제 필드 - 삭제 상태 표시
    is_deleted = models.BooleanField(default=False)

    # 소프트 삭제 메서드
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    # 복원 메서드
    def restore(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.title

    # 객체 관리자 설정
    objects = SoftDeleteManager()
    all_objects = models.Manager()