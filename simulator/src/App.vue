<script setup>
import TheHeader from '@/components/TheHeader.vue'
import BroadcastBar from '@/components/BroadcastBar.vue'
import DevicePanel from '@/components/DevicePanel.vue'
import LogPanel from '@/components/LogPanel.vue'
</script>

<template>
  <div class="layout">
    <TheHeader />
    <BroadcastBar />
    <DevicePanel />
    <LogPanel />
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}
</style>
