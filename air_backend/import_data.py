#!/usr/bin/env python
"""
数据导入脚本
将Excel文件中的数据导入到Django数据库
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_backend.settings')
django.setup()

from prediction.models import AirQualityHealthDataset

def import_excel_data():
    """导入Excel数据到数据库"""
    try:
        # 读取Excel文件
        excel_file = '../air_quality_health_dataset.xlsx'
        if not os.path.exists(excel_file):
            print(f"错误: 找不到文件 {excel_file}")
            return False
            
        print(f"正在读取文件: {excel_file}")
        df = pd.read_excel(excel_file)
        
        print(f"数据行数: {len(df)}")
        print(f"数据列: {list(df.columns)}")
        
        # 清空现有数据
        AirQualityHealthDataset.objects.all().delete()
        print("已清空现有数据")
        
        # 导入数据
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # 处理日期格式
                date_str = str(row.get('date', ''))
                if pd.isna(date_str) or date_str == 'nan':
                    date_str = datetime.now().strftime('%Y-%m-%d')
                
                # 创建记录
                record = AirQualityHealthDataset(
                    city=str(row.get('city', '')),
                    date=date_str,
                    aqi=str(row.get('aqi', '')),
                    pm2_5=str(row.get('pm2_5', '')),
                    pm10=str(row.get('pm10', '')),
                    no2=str(row.get('no2', '')),
                    o3=str(row.get('o3', '')),
                    temperature=str(row.get('temperature', '')),
                    humidity=str(row.get('humidity', '')),
                    hospital_admissions=str(row.get('hospital_admissions', '')),
                    population_density=str(row.get('population_density', '')),
                    hospital_capacity=str(row.get('hospital_capacity', ''))
                )
                record.save()
                success_count += 1
                
                if success_count % 100 == 0:
                    print(f"已导入 {success_count} 条记录...")
                    
            except Exception as e:
                print(f"导入第 {index + 1} 行时出错: {str(e)}")
                error_count += 1
                continue
        
        print(f"\n导入完成!")
        print(f"成功导入: {success_count} 条记录")
        print(f"导入失败: {error_count} 条记录")
        
        return True
        
    except Exception as e:
        print(f"导入过程中出现错误: {str(e)}")
        return False

if __name__ == '__main__':
    print("开始导入数据...")
    success = import_excel_data()
    if success:
        print("数据导入成功!")
    else:
        print("数据导入失败!")
        sys.exit(1) 