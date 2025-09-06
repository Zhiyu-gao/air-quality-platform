# 空气质量预测平台

这是一个基于机器学习的空气质量健康影响预测平台，包含Django后端和Vue.js前端。

## 项目结构

```
air-quality-platform/
├── air_backend/          # Django后端
│   ├── air_backend/      # Django项目配置
│   ├── prediction/       # 预测应用
│   ├── train_model.py    # 模型训练脚本
│   ├── import_data.py    # 数据导入脚本
│   ├── requirements.txt  # Python依赖
│   └── pyrightconfig.json # 类型检查配置
├── frontend/             # Vue.js前端
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── router/       # 路由配置
│   │   ├── config/       # 配置文件
│   │   ├── types/        # 类型声明
│   │   └── App.vue       # 根组件
│   └── package.json      # Node.js依赖
└── air_quality_health_dataset.xlsx  # 数据集
```

## 安装和运行

### 后端设置

1. 进入后端目录：
```bash
cd air_backend
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 配置数据库（MySQL）：
   - 创建数据库 `air_quality`
   - 更新 `air_backend/settings.py` 中的数据库配置

4. 运行数据库迁移：
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 导入Excel数据：
```bash
python import_data.py
```

6. 训练模型：
```bash
python train_model.py
```

7. 启动Django服务器：
```bash
python manage.py runserver
```

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装Node.js依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

## 功能特性

- **空气质量预测**：基于多个环境指标预测医院住院人数
- **历史记录查看**：查看历史预测记录
- **数据可视化**：使用ECharts展示数据图表
  - AQI趋势图
  - PM2.5与住院人数关系图
  - 温度与湿度分布图
  - 各城市AQI对比图
- **数据管理**：完整的增删改查功能
  - 添加新记录
  - 编辑现有记录
  - 删除记录
  - 批量删除
  - 搜索和筛选
  - 分页显示
- **响应式设计**：使用Element Plus组件库
- **数据管理**：Django管理后台支持数据管理
- **API配置**：统一的API配置和错误处理

## 页面说明

### 1. 空气质量预测 (/)
- 输入环境指标进行预测
- 实时图表展示
- 预测结果可视化

### 2. 历史记录 (/records)
- 查看所有历史数据
- 表格形式展示
- 数据加载状态

### 3. 数据可视化 (/visualization)
- 多种图表类型
- 数据筛选功能
- 统计信息展示
- 交互式图表

### 4. 数据管理 (/data-management)
- 完整的CRUD操作
- 搜索和筛选
- 分页功能
- 批量操作

## API接口

- `GET /prediction/` - 获取所有记录
- `POST /prediction/` - 创建新记录
- `PUT /prediction/{id}/` - 更新记录
- `DELETE /prediction/{id}/` - 删除记录
- `POST /prediction/predict/` - 进行预测
- `GET /prediction/stats/` - 获取统计数据
- `GET /admin/` - Django管理后台

## 技术栈

### 后端
- Django 4.2
- Django REST Framework
- scikit-learn
- MySQL
- PyMySQL

### 前端
- Vue 3
- TypeScript
- Vue Router 4
- Element Plus
- ECharts
- Vite
- Axios

## 开发说明

### 类型检查
- **后端**：使用Pyright进行Python类型检查，配置文件位于 `air_backend/pyrightconfig.json`
- **前端**：使用TypeScript进行类型检查，配置文件位于 `frontend/tsconfig.app.json`

如果遇到Django相关的类型检查警告，这些是正常的，因为Django的动态特性。项目已配置忽略这些警告。

### 数据管理
- 使用 `import_data.py` 脚本将Excel数据导入到数据库
- 通过Django管理后台管理数据
- 支持数据的增删改查操作

### API配置
- 前端使用统一的API配置文件 `src/config/api.ts`
- 支持开发和生产环境的不同配置
- 使用axios拦截器进行统一的错误处理

### TypeScript配置
- 项目使用独立的TypeScript配置，不依赖@vue/tsconfig
- 已禁用 `verbatimModuleSyntax` 以避免类型导入问题
- 使用 `bundler` 模块解析策略

### 数据可视化
- 使用ECharts进行图表展示
- 支持多种图表类型：折线图、散点图、柱状图
- 响应式图表设计
- 数据筛选和交互功能

### 快速启动
- 后端：双击 `start_backend.bat`
- 前端：双击 `start_frontend.bat`

## 注意事项

1. 确保MySQL数据库已正确配置
2. 首次运行会自动导入数据并训练模型
3. 前端默认连接到 `http://localhost:8000`
4. 类型检查警告不会影响程序运行
5. 前端使用Vue Router 4进行路由管理
6. 数据导入脚本会自动处理Excel文件格式
7. 如果遇到TypeScript模块解析问题，请检查node_modules是否正确安装
8. 数据可视化功能需要ECharts库支持
9. 数据管理功能支持完整的CRUD操作 "# air-quality-platform" 
