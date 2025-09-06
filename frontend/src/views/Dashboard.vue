<template>
  <el-card>
    <template #header>
      <h2>住院人数预测</h2>
    </template>
    
    <el-form :model="form" label-width="140px" :rules="rules" ref="formRef">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="城市" prop="city">
            <el-input v-model="form.city" placeholder="请输入城市名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="日期" prop="date">
            <el-date-picker 
              v-model="form.date" 
              type="date" 
              placeholder="选择日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="AQI" prop="aqi">
            <el-input-number v-model="form.aqi" :min="0" :max="500" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="PM2.5" prop="pm2_5">
            <el-input-number v-model="form.pm2_5" :min="0" :max="500" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="PM10" prop="pm10">
            <el-input-number v-model="form.pm10" :min="0" :max="600" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="NO2" prop="no2">
            <el-input-number v-model="form.no2" :min="0" :max="200" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="O3" prop="o3">
            <el-input-number v-model="form.o3" :min="0" :max="300" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="温度(°C)" prop="temperature">
            <el-input-number v-model="form.temperature" :min="-50" :max="50" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="湿度(%)" prop="humidity">
            <el-input-number v-model="form.humidity" :min="0" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="人口密度" prop="population_density">
            <el-input-number v-model="form.population_density" :min="0" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="医院容量" prop="hospital_capacity">
            <el-input-number v-model="form.hospital_capacity" :min="0" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item>
        <el-button type="primary" @click="predict" :loading="loading">
          开始预测
        </el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <el-alert 
      v-if="result" 
      :title="`预测住院人数：${result} 人`" 
      type="success" 
      :closable="false"
      show-icon
    />
    
    <el-alert 
      v-if="error" 
      :title="error" 
      type="error" 
      :closable="false"
      show-icon
    />
    
    <div ref="chart" style="height: 400px; margin-top: 20px;"></div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '../config/axios'
import { API_ENDPOINTS } from '../config/api'

const form = ref({ 
  city: '', 
  date: '', 
  aqi: 50, 
  pm2_5: 30, 
  pm10: 40, 
  no2: 25, 
  o3: 18, 
  temperature: 22, 
  humidity: 60, 
  population_density: 3000, 
  hospital_capacity: 100 
})

const result = ref(null)
const error = ref(null)
const loading = ref(false)
const chart = ref()
const formRef = ref()

const rules = {
  city: [{ required: true, message: '请输入城市名称', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }]
}

const predict = async () => {
  try {
    await formRef.value.validate()
    
    loading.value = true
    error.value = null
    result.value = null
    
    const res = await apiClient.post(API_ENDPOINTS.PREDICT, form.value)
    
    if (res.data.error) {
      error.value = res.data.error
    } else {
      result.value = res.data.predicted_admissions.toFixed(2)
      drawChart()
      ElMessage.success('预测成功！')
    }
  } catch (err) {
    console.error('预测错误:', err)
    error.value = err.response?.data?.error || '预测失败，请检查网络连接'
    ElMessage.error('预测失败')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formRef.value.resetFields()
  result.value = null
  error.value = null
}

const drawChart = () => {
  nextTick(() => {
    if (!chart.value) return
    
    const myChart = chart.value.__echarts__ || window.echarts.init(chart.value)
    chart.value.__echarts__ = myChart
    
    const chartData = [
      { name: 'AQI', value: form.value.aqi },
      { name: 'PM2.5', value: form.value.pm2_5 },
      { name: 'PM10', value: form.value.pm10 },
      { name: 'NO2', value: form.value.no2 },
      { name: 'O3', value: form.value.o3 },
      { name: '温度', value: form.value.temperature },
      { name: '湿度', value: form.value.humidity },
      { name: '人口密度', value: form.value.population_density },
      { name: '医院容量', value: form.value.hospital_capacity }
    ]
    
    myChart.setOption({
      title: { 
        text: '环境指标对比',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      xAxis: { 
        type: 'category',
        data: chartData.map(item => item.name),
        axisLabel: { rotate: 45 }
      },
      yAxis: { type: 'value' },
      series: [{ 
        type: 'bar', 
        data: chartData.map(item => item.value),
        itemStyle: {
          color: '#409EFF'
        }
      }],
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      }
    })
  })
}

onMounted(() => {
  drawChart()
})
</script>

<style scoped>
.el-card {
  margin: 20px;
}

.el-form-item {
  margin-bottom: 18px;
}
</style>