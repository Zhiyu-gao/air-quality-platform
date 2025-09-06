<template>
  <div class="data-management-container">
    <el-card>
      <template #header>
        <div class="header-content">
          <h2>数据管理</h2>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加数据
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <el-form :inline="true" class="search-form">
        <el-form-item label="城市">
          <el-input v-model="searchForm.city" placeholder="搜索城市" clearable />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="searchForm.date"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchData" :loading="loading">
            搜索
          </el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
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
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="editRecord(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteRecord(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>

      <!-- 批量操作 -->
      <div class="batch-actions" v-if="selectedRows.length > 0">
        <el-button type="danger" @click="batchDelete">
          批量删除 ({{ selectedRows.length }})
        </el-button>
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="isEdit ? '编辑数据' : '添加数据'"
      width="600px"
    >
      <el-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="城市" prop="city">
              <el-input v-model="formData.city" placeholder="请输入城市名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="日期" prop="date">
              <el-date-picker
                v-model="formData.date"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="AQI" prop="aqi">
              <el-input-number v-model="formData.aqi" :min="0" :max="500" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="PM2.5" prop="pm2_5">
              <el-input-number v-model="formData.pm2_5" :min="0" :max="500" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="PM10" prop="pm10">
              <el-input-number v-model="formData.pm10" :min="0" :max="600" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="NO2" prop="no2">
              <el-input-number v-model="formData.no2" :min="0" :max="200" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="O3" prop="o3">
              <el-input-number v-model="formData.o3" :min="0" :max="300" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="温度(°C)" prop="temperature">
              <el-input-number v-model="formData.temperature" :min="-50" :max="50" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="湿度(%)" prop="humidity">
              <el-input-number v-model="formData.humidity" :min="0" :max="100" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="人口密度" prop="population_density">
              <el-input-number v-model="formData.population_density" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="医院容量" prop="hospital_capacity">
              <el-input-number v-model="formData.hospital_capacity" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="住院人数" prop="hospital_admissions">
          <el-input-number v-model="formData.hospital_admissions" :min="0" style="width: 100%" />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="saveRecord" :loading="saving">
            {{ isEdit ? '更新' : '保存' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import apiClient from '../config/axios'
import { API_ENDPOINTS } from '../config/api'

const loading = ref(false)
const saving = ref(false)
const showAddDialog = ref(false)
const isEdit = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const selectedRows = ref([])
const tableData = ref([])
const formRef = ref()

const searchForm = reactive({
  city: '',
  date: ''
})

const formData = reactive({
  id: null,
  city: '',
  date: '',
  aqi: 50,
  pm2_5: 30,
  pm10: 40,
  no2: 25,
  o3: 18,
  temperature: 22,
  humidity: 60,
  hospital_admissions: 100,
  population_density: 3000,
  hospital_capacity: 100
})

const formRules = {
  city: [{ required: true, message: '请输入城市名称', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  aqi: [{ required: true, message: '请输入AQI值', trigger: 'blur' }],
  pm2_5: [{ required: true, message: '请输入PM2.5值', trigger: 'blur' }],
  pm10: [{ required: true, message: '请输入PM10值', trigger: 'blur' }],
  no2: [{ required: true, message: '请输入NO2值', trigger: 'blur' }],
  o3: [{ required: true, message: '请输入O3值', trigger: 'blur' }],
  temperature: [{ required: true, message: '请输入温度值', trigger: 'blur' }],
  humidity: [{ required: true, message: '请输入湿度值', trigger: 'blur' }],
  hospital_admissions: [{ required: true, message: '请输入住院人数', trigger: 'blur' }],
  population_density: [{ required: true, message: '请输入人口密度', trigger: 'blur' }],
  hospital_capacity: [{ required: true, message: '请输入医院容量', trigger: 'blur' }]
}

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const res = await apiClient.get(API_ENDPOINTS.RECORDS)
    let data = res.data.data
    console.log("data的值为-----------")
    console.log(data)

    // 应用搜索条件
    if (searchForm.city) {
      data = data.filter(item => item.city.includes(searchForm.city))
    }
    if (searchForm.date) {
      data = data.filter(item => item.date === searchForm.date)
    }

    total.value = data.length
    
    // 分页
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    tableData.value = data.slice(start, end)
    
  } catch (err) {
    console.error('加载数据错误:', err)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索数据
const searchData = () => {
  currentPage.value = 1
  loadData()
}

// 重置搜索
const resetSearch = () => {
  searchForm.city = ''
  searchForm.date = ''
  currentPage.value = 1
  loadData()
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadData()
}

// 选择处理
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

// 编辑记录
const editRecord = (row) => {
  isEdit.value = true
  Object.assign(formData, row)
  showAddDialog.value = true
}

// 删除记录
const deleteRecord = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 ${row.city} 在 ${row.date} 的记录吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await apiClient.delete(`${API_ENDPOINTS.RECORDS}${row.id}/`)
    ElMessage.success('删除成功')
    loadData()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除错误:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除
const batchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 条记录吗？`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const deletePromises = selectedRows.value.map(row => 
      apiClient.delete(`${API_ENDPOINTS.RECORDS}${row.id}/`)
    )
    await Promise.all(deletePromises)
    
    ElMessage.success('批量删除成功')
    selectedRows.value = []
    loadData()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('批量删除错误:', err)
      ElMessage.error('批量删除失败')
    }
  }
}

// 保存记录
const saveRecord = async () => {
  try {
    await formRef.value.validate()
    saving.value = true

    if (isEdit.value) {
      await apiClient.put(`${API_ENDPOINTS.RECORDS}${formData.id}/`, formData)
      ElMessage.success('更新成功')
    } else {
      await apiClient.post(API_ENDPOINTS.RECORDS, formData)
      ElMessage.success('添加成功')
    }

    showAddDialog.value = false
    resetForm()
    loadData()
  } catch (err) {
    console.error('保存错误:', err)
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  } finally {
    saving.value = false
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.resetFields()
  Object.assign(formData, {
    id: null,
    city: '',
    date: '',
    aqi: 50,
    pm2_5: 30,
    pm10: 40,
    no2: 25,
    o3: 18,
    temperature: 22,
    humidity: 60,
    hospital_admissions: 100,
    population_density: 3000,
    hospital_capacity: 100
  })
  isEdit.value = false
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.data-management-container {
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.batch-actions {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.dialog-footer {
  text-align: right;
}
</style> 