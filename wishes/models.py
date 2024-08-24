from django.db import models

class wish(models.Model):
    # 카테고리
    CATEGORY = [
        ('career', '진로'),
        ('health', '건강'),
        ('relationships', '인간 관계'),
        ('money', '돈'),
        ('goals', '목표'),
        ('academics', '학업/성적'),
        ('others', '기타'),
    ]
    # WISH의 상태
    WISH_STATUS = [
        ('pending', '보류'),
        ('approved', '승인'),
        ('rejected', '거절'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY,
        # 기본값을 기타로 설정
        default='others'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirm = models.CharField(
        max_length=10,
        # 기본값을 보류로 설정
        default='pending'
    )

    def __str__(self):
        return self.title