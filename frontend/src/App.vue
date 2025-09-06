<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-menu mode="horizontal" router>
          <el-menu-item index="/">住院人数预测</el-menu-item>
          <el-menu-item index="/records">历史记录</el-menu-item>
          <el-menu-item index="/visualization">数据可视化</el-menu-item>
          <el-menu-item index="/data-management">数据管理</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
// 组件逻辑
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  padding: 0;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
}

.el-main {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px);
}
</style> 