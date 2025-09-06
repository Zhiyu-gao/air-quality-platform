@echo off
echo 启动空气质量预测平台前端服务...
echo.

cd frontend

echo 检查Node.js环境...
node --version
if errorlevel 1 (
    echo 错误: 未找到Node.js，请确保已安装Node.js并添加到PATH
    pause
    exit /b 1
)

echo.
echo 安装依赖包...
npm install

echo.
echo 检查依赖安装状态...
npm list vue-router
if errorlevel 1 (
    echo 警告: vue-router可能未正确安装，尝试重新安装...
    npm install vue-router@^4.2.5
)

echo.
echo 启动开发服务器...
echo 前端将在 http://localhost:5173 启动
echo 按 Ctrl+C 停止服务器
echo.
npm run dev

pause 