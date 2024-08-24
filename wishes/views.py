from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import wish
from .serializers import wishSerializer
from rest_framework.pagination import PageNumberPagination

class wishPagination(PageNumberPagination):
    page_size = 10

class wishViewSet(viewsets.ModelViewSet):
    queryset = wish.objects.all().order_by('-created_at')
    serializer_class = wishSerializer
    pagination_class = wishPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        is_confirm = self.request.query_params.get('is_confirm')
        if is_confirm in ['approved', 'rejected', 'pending']:
            queryset = queryset.filter(is_confirm=is_confirm)
        return queryset

    # wish 생성 시 보류를 기본 값으로 설정 -> models에서 pending으로 설정했는데 여기서 또 설정??
    def perform_create(self, serializer):
        serializer.save(is_confirm='pending')

    def destroy(self, request, *args, **kwargs):
        # destroy 메서드를 오버라이드하여 delete 메서드를 호출하고 소프트 삭제를 수행
        instance = self.get_object()
        instance.delete()  # Soft delete instead of actual deletion
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def approve_all(self, request, *args, **kwargs):
        updated_count = wish.objects.filter(is_confirm='pending').update(is_confirm='approved')
        return Response({'status': f'{updated_count} wishes approved'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def reject_all(self, request, *args, **kwargs):
        updated_count = wish.objects.filter(is_confirm='pending').update(is_confirm='rejected')
        return Response({'status': f'{updated_count} wishes rejected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, *args, **kwargs):
        # restore 메서드는 커스텀 액션으로, 삭제된 항목을 복원
        instance = self.get_object()
        if instance.is_deleted:
            instance.restore()  # Restore the wish
            return Response({'status': 'restored'}, status=status.HTTP_200_OK)
        return Response({'status': 'not deleted'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def all_with_deleted(self, request, *args, **kwargs):
        # all_with_deleted 메서드는 모든 항목(삭제된 항목 포함)을 조회
        queryset = wish.all_objects.all().order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_wishes(self, request, *args, **kwargs):
        # 보류 상태의 소원을 조회합니다.
        queryset = wish.objects.filter(is_confirm='pending').order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_confirm == 'pending':
            instance.is_confirm = 'approved'
            instance.save()
            return Response({'status': 'approved'}, status=status.HTTP_200_OK)
        return Response({'status': 'not pending'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_confirm == 'pending':
            instance.is_confirm = 'rejected'
            instance.save()
            return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
        return Response({'status': 'not pending'}, status=status.HTTP_400_BAD_REQUEST)
