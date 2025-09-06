from rest_framework import viewsets, status
from django.db import models
from .models import AirQualityHealthDataset
from .serializers import AirQualityHealthDatasetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import numpy as np
import joblib
import os
from typing import Any

class AirQualityViewSet(viewsets.ModelViewSet):
    queryset = AirQualityHealthDataset.objects.all()  # type: ignore
    serializer_class = AirQualityHealthDatasetSerializer

    def create(self, request, *args, **kwargs):
        """创建新记录"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': '记录创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'error': f'创建记录失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """更新记录"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'message': '记录更新成功',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'error': f'更新记录失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """删除记录"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                'message': '记录删除成功'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': f'删除记录失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """获取记录列表"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            # 支持分页
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': '获取记录成功',
                'data': serializer.data,
                'count': len(serializer.data)
            })
        except Exception as e:
            return Response({
                'error': f'获取记录失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """获取单条记录"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'message': '获取记录成功',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'error': f'获取记录失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def predict(self, request: Any) -> Response:
        try:
            data = request.data
            
            # 检查模型文件是否存在
            model_path = 'prediction/model.pkl'
            scaler_path = 'prediction/scaler.pkl'
            
            if not os.path.exists(model_path) or not os.path.exists(scaler_path):
                return Response({
                    'error': '模型文件不存在，请先训练模型'
                }, status=400)
            
            # 准备特征数据
            features = np.array([
                float(data.get('aqi', 0)),
                float(data.get('pm2_5', 0)),
                float(data.get('pm10', 0)),
                float(data.get('no2', 0)),
                float(data.get('o3', 0)),
                float(data.get('temperature', 0)),
                float(data.get('humidity', 0)),
                float(data.get('hospital_capacity', 0))
            ]).reshape(1, -1)
            
            # 加载模型和标准化器
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            
            # 标准化特征
            features_scaled = scaler.transform(features)
            
            # 进行预测
            prediction = model.predict(features_scaled)
            
            return Response({
                'predicted_admissions': float(prediction[0]),
                'message': '预测成功'
            })
            
        except Exception as e:
            return Response({
                'error': f'预测过程中出现错误: {str(e)}'
            }, status=500)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """获取统计数据"""
        try:
            queryset = self.get_queryset()
            
            # 计算基本统计信息
            total_records = queryset.count()
            
            # 按城市分组统计
            cities = queryset.values_list('city', flat=True).distinct()
            city_stats = {}
            
            for city in cities:
                city_data = queryset.filter(city=city)
                city_stats[city] = {
                    'count': city_data.count(),
                    'avg_aqi': city_data.aggregate(avg=models.Avg('aqi'))['avg_aqi'] or 0,
                    'avg_pm25': city_data.aggregate(avg=models.Avg('pm2_5'))['avg_pm25'] or 0,
                    'avg_temperature': city_data.aggregate(avg=models.Avg('temperature'))['avg_temperature'] or 0,
                    'avg_admissions': city_data.aggregate(avg=models.Avg('hospital_admissions'))['avg_admissions'] or 0
                }
            
            return Response({
                'message': '获取统计数据成功',
                'data': {
                    'total_records': total_records,
                    'city_stats': city_stats
                }
            })
        except Exception as e:
            return Response({
                'error': f'获取统计数据失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)