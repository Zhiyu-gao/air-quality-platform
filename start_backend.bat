@echo off
echo 启动空气质量预测平台后端服务...
echo.

cd air_backend

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请确保已安装Python并添加到PATH
    pause
    exit /b 1
)

echo.
echo 安装依赖包...
pip install -r requirements.txt

echo.
echo 运行数据库迁移...
python manage.py makemigrations
python manage.py migrate

echo.
echo 导入Excel数据到数据库...
python import_data.py

echo.
echo 训练机器学习模型...
python train_model.py

echo.
echo 启动Django服务器...
echo 服务器将在 http://localhost:8000 启动
echo 按 Ctrl+C 停止服务器
echo.
python manage.py runserver

pause 