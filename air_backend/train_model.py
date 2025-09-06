# prediction/train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model():
    try:
        # 读取Excel文件
        df = pd.read_excel(r'D:\aaaaaaaaaaaaaaaaaaaaaa\air-quality-platform\air_quality_health_dataset.xlsx')
        
        # 数据预处理
        # 将字符串类型的数值列转换为数值类型
        numeric_columns = ['aqi', 'pm2_5', 'pm10', 'no2', 'o3', 'temperature', 
                          'humidity', 'hospital_capacity', 'hospital_admissions']
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        
        # 准备特征和目标变量
        features = df[["aqi", "pm2_5", "pm10", "no2", "o3", "temperature", 
                      "humidity", "hospital_capacity"]]
        target = df["hospital_admissions"]
        
        # 数据标准化
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # 分割训练和测试数据
        X_train, X_test, y_train, y_test = train_test_split(
            features_scaled, target, test_size=0.2, random_state=42
        )
        
        # 训练模型
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # 评估模型
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print(f"训练集R²分数: {train_score:.4f}")
        print(f"测试集R²分数: {test_score:.4f}")
        
        # 保存模型和标准化器
        model_dir = "prediction"
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        model_path = f"{model_dir}/model.pkl"
        scaler_path = f"{model_dir}/scaler.pkl"

        print(f"模型将保存到: {os.path.abspath(model_path)}")
        print(f"标准化器将保存到: {os.path.abspath(scaler_path)}")

        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        print("模型训练完成并保存")
        
    except Exception as e:
        print(f"训练过程中出现错误: {str(e)}")

if __name__ == "__main__":
    train_model()
