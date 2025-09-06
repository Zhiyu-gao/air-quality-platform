// API配置
export const API_CONFIG = {
  // 开发环境
  development: {
    baseURL: 'http://localhost:8000',
    timeout: 10000
  },
  // 生产环境
  production: {
    baseURL: 'https://your-production-api.com',
    timeout: 10000
  }
}

// 根据环境获取配置
const env = import.meta.env.MODE || 'development'
export const API_BASE_URL = API_CONFIG[env as keyof typeof API_CONFIG].baseURL

// API端点
export const API_ENDPOINTS = {
  PREDICT: '/prediction/predict/',
  RECORDS: '/prediction/',
  STATS: '/prediction/stats/'
} as const 