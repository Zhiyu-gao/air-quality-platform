<template>
  <div class="visualization-container">
    <el-card>
      <template #header>
        <h2>数据可视化分析</h2>
      </template>
      
      <!-- 筛选条件 -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="城市">
          <el-select v-model="filters.city" placeholder="选择城市" clearable>
            <el-option
              v-for="city in cityOptions"
              :key="city"
              :label="city"
              :value="city"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData" :loading="loading">
            查询数据
          </el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ stats.avgAqi }}</div>
              <div class="stats-label">平均AQI</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ stats.avgPm25 }}</div>
              <div class="stats-label">平均PM2.5</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ stats.avgTemperature }}</div>
              <div class="stats-label">平均温度(°C)</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stats-card">
            <div class="stats-content">
              <div class="stats-number">{{ stats.avgAdmissions }}</div>
              <div class="stats-label">平均住院人数</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 图表区域 -->
      <el-row :gutter="20" class="charts-row">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>AQI趋势图</h3>
            </template>
            <div ref="aqiChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>PM2.5与住院人数关系</h3>
            </template>
            <div ref="pm25Chart" style="height: 300px;"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="charts-row">
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>温度与湿度分布</h3>
            </template>
            <div ref="tempHumidityChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <h3>各城市AQI对比</h3>
            </template>
            <div ref="cityChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '../config/axios'
import { API_ENDPOINTS } from '../config/api'
import * as echarts from 'echarts'; 
window.echarts = echarts; // 把 echarts 挂载到 window 上，让组件里能通过 window.echarts 访问

const loading = ref(false)
const filters = ref({
  city: '',
  dateRange: []
})


const stats = ref({
  avgAqi: 0,
  avgPm25: 0,
  avgTemperature: 0,
  avgAdmissions: 0
})

const cityOptions = ref([])
const chartData = ref([])

// 图表引用
const aqiChart = ref()
const pm25Chart = ref()
const tempHumidityChart = ref()
const cityChart = ref()

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    
    const res = await apiClient.get(API_ENDPOINTS.RECORDS)
    let data = res.data.data
    // console.log("--------------------")
    // console.log(data)
    // console.log("--------------------")
    
    
    // 应用筛选条件
    if (filters.value.city) {
      data = data.filter(item => item.city === filters.value.city)
    }
    
    if (filters.value.dateRange && filters.value.dateRange.length === 2) {
      const [startDate, endDate] = filters.value.dateRange
      data = data.filter(item => {
        const itemDate = item.date
        return itemDate >= startDate && itemDate <= endDate
      })
    }
    
    chartData.value = data
    calculateStats(data)
    drawCharts()
    
    ElMessage.success(`成功加载 ${data.length} 条数据`)
  } catch (err) {
    console.error('加载数据错误:', err)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 计算统计数据
const calculateStats = (data) => {
  if (data.length === 0) return
  const aqiValues = data.map(item => parseFloat(item.aqi) || 0).filter(v => v > 0)
  const pm25Values = data.map(item => parseFloat(item.pm2_5) || 0).filter(v => v > 0)
  const tempValues = data.map(item => parseFloat(item.temperature) || 0).filter(v => v > 0)
  const admissionValues = data.map(item => parseFloat(item.hospital_admissions) || 0).filter(v => v > 0)
  
  stats.value = {
    avgAqi: aqiValues.length > 0 ? (aqiValues.reduce((a, b) => a + b, 0) / aqiValues.length).toFixed(1) : 0,
    avgPm25: pm25Values.length > 0 ? (pm25Values.reduce((a, b) => a + b, 0) / pm25Values.length).toFixed(1) : 0,
    avgTemperature: tempValues.length > 0 ? (tempValues.reduce((a, b) => a + b, 0) / tempValues.length).toFixed(1) : 0,
    avgAdmissions: admissionValues.length > 0 ? (admissionValues.reduce((a, b) => a + b, 0) / admissionValues.length).toFixed(1) : 0
  }
}

// 重置筛选条件
const resetFilters = () => {
  filters.value = {
    city: '',
    dateRange: []
  }
  loadData()
}

// 绘制图表
const drawCharts = () => {
  nextTick(() => {
    drawAqiChart()
    drawPm25Chart()
    drawTempHumidityChart()
    drawCityChart()
  })
}

// AQI趋势图
const drawAqiChart = () => {
  if (!aqiChart.value || chartData.value.length === 0) return
  
  const myChart = aqiChart.value.__echarts__ || window.echarts.init(aqiChart.value)
  aqiChart.value.__echarts__ = myChart
  
  const sortedData = chartData.value
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-20) // 只显示最近20条数据
  
  console.log("-------------------")
  console.log("sortedData的值为")
  console.log(sortedData)
  console.log("-------------------")

  
  myChart.setOption({
    title: { text: 'AQI趋势变化' },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: sortedData.map(item => item.date)
    },
    yAxis: { type: 'value' },
    series: [{
      name: 'AQI',
      type: 'line',
      data: sortedData.map(item => parseFloat(item.aqi) || 0),
      smooth: true,
      itemStyle: { color: '#409EFF' }
    }]
  })
}

// PM2.5与住院人数关系图
const drawPm25Chart = () => {
  if (!pm25Chart.value || chartData.value.length === 0) return
  
  const myChart = pm25Chart.value.__echarts__ || window.echarts.init(pm25Chart.value)
  pm25Chart.value.__echarts__ = myChart
  
  const data = chartData.value.map(item => [
    parseFloat(item.pm2_5) || 0,
    parseFloat(item.hospital_admissions) || 0
  ]).filter(point => point[0] > 0 && point[1] > 0)
  
  myChart.setOption({
    title: { text: 'PM2.5与住院人数关系' },
    tooltip: { trigger: 'item' },
    xAxis: { type: 'value', name: 'PM2.5' },
    yAxis: { type: 'value', name: '住院人数' },
    series: [{
      name: '关系',
      type: 'scatter',
      data: data,
      itemStyle: { color: '#67C23A' }
    }]
  })
}

// 温度与湿度分布图
const drawTempHumidityChart = () => {
  if (!tempHumidityChart.value || chartData.value.length === 0) return
  
  const myChart = tempHumidityChart.value.__echarts__ || window.echarts.init(tempHumidityChart.value)
  tempHumidityChart.value.__echarts__ = myChart
  
  const data = chartData.value.map(item => [
    parseFloat(item.temperature) || 0,
    parseFloat(item.humidity) || 0
  ]).filter(point => point[0] > 0 && point[1] > 0)
  
  myChart.setOption({
    title: { text: '温度与湿度分布' },
    tooltip: { trigger: 'item' },
    xAxis: { type: 'value', name: '温度(°C)' },
    yAxis: { type: 'value', name: '湿度(%)' },
    series: [{
      name: '分布',
      type: 'scatter',
      data: data,
      itemStyle: { color: '#E6A23C' }
    }]
  })
}

// 各城市AQI对比图
const drawCityChart = () => {
  if (!cityChart.value || chartData.value.length === 0) return
  
  const myChart = cityChart.value.__echarts__ || window.echarts.init(cityChart.value)
  cityChart.value.__echarts__ = myChart
  
  // 按城市分组计算平均AQI
  const cityData = {}
  chartData.value.forEach(item => {
    if (!cityData[item.city]) {
      cityData[item.city] = []
    }
    const aqi = parseFloat(item.aqi) || 0
    if (aqi > 0) {
      cityData[item.city].push(aqi)
    }
  })
  
  const cities = Object.keys(cityData)
  const avgAqi = cities.map(city => {
    const values = cityData[city]
    return values.length > 0 ? (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1) : 0
  })
  
  myChart.setOption({
    title: { text: '各城市平均AQI对比' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: cities },
    yAxis: { type: 'value' },
    series: [{
      name: '平均AQI',
      type: 'bar',
      data: avgAqi,
      itemStyle: { color: '#F56C6C' }
    }]
  })
}

// 获取城市选项
const loadCityOptions = async () => {
  try {
    const res = await apiClient.get(API_ENDPOINTS.RECORDS)
    const cities = [...new Set(res.data.data.map(item => item.city).filter(city => city))]
    cityOptions.value = cities
  } catch (err) {
    console.error('加载城市选项错误:', err)
  }
}

onMounted(() => {
  loadCityOptions()
  loadData()
})
</script>

<style scoped>
.visualization-container {
  padding: 20px;
}

.filter-form {
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  text-align: center;
}

.stats-content {
  padding: 10px;
}

.stats-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stats-label {
  font-size: 14px;
  color: #666;
}

.charts-row {
  margin-bottom: 20px;
}
</style> 