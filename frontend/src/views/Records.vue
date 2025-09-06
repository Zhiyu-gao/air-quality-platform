<template>
  <el-card>
    <template #header>
      <h2>历史记录</h2>
    </template>
    
    <el-table 
      :data="records" 
      v-loading="loading"
      stripe
      border
      style="width: 100%"
    >
      <el-table-column prop="city" label="城市" width="120" />
      <el-table-column prop="date" label="日期" width="120" />
      <el-table-column prop="aqi" label="AQI" width="80" />
      <el-table-column prop="pm2_5" label="PM2.5" width="80" />
      <el-table-column prop="pm10" label="PM10" width="80" />
      <el-table-column prop="no2" label="NO2" width="80" />
      <el-table-column prop="o3" label="O3" width="80" />
      <el-table-column prop="temperature" label="温度(°C)" width="100" />
      <el-table-column prop="humidity" label="湿度(%)" width="100" />
      <el-table-column prop="hospital_admissions" label="住院人数" width="100" />
      <el-table-column prop="population_density" label="人口密度" width="100" />
      <el-table-column prop="hospital_capacity" label="医院容量" width="100" />
    </el-table>
    
    <el-alert 
      v-if="error" 
      :title="error" 
      type="error" 
      :closable="false"
      show-icon
      style="margin-top: 20px;"
    />
    
    <div v-if="records.length === 0 && !loading && !error" style="text-align: center; padding: 40px; color: #909399;">
      暂无数据
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '../config/axios'
import { API_ENDPOINTS } from '../config/api'

const records = ref([])
const loading = ref(false)
const error = ref(null)

const fetchRecords = async () => {
  try {
    loading.value = true
    error.value = null
    
    const res = await apiClient.get(API_ENDPOINTS.RECORDS)
    records.value = res.data
    
    if (records.value.length > 0) {
      ElMessage.success(`成功加载 ${records.value.length} 条记录`)
    }
  } catch (err) {
    console.error('获取记录错误:', err)
    error.value = err.response?.data?.error || '获取数据失败，请检查网络连接'
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.el-card {
  margin: 20px;
}

.el-table {
  margin-top: 20px;
}
</style>
  