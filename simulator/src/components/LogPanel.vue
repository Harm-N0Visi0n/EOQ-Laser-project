<script setup>
import { useMqtt } from '@/composables/useMqtt.js'

const { messages } = useMqtt()

function fmtTime(ts) {
  const d = new Date(ts)
  return [d.getHours(), d.getMinutes(), d.getSeconds()]
    .map(n => String(n).padStart(2, '0'))
    .join(':')
}
</script>

<template>
  <footer class="log-panel">
    <div class="log-header">
      <span class="log-title">MQTT LOG</span>
      <span class="log-count">{{ messages.length }} messages</span>
      <button @click="messages.splice(0)" class="btn-clear">CLEAR</button>
    </div>
    <div class="log-entries">
      <div v-for="msg in messages" :key="msg.id" class="log-entry">
        <span class="log-topic">{{ msg.topic }}</span>
        <span class="log-payload">{{ msg.payload }}</span>
        <span class="log-time">{{ fmtTime(msg.ts) }}</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.log-panel {
  height: 190px;
  flex-shrink: 0;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

.log-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.log-title {
  color: var(--green);
  font-size: 10px;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.log-count {
  color: var(--text-dim);
  font-size: 10px;
  margin-left: auto;
}

.btn-clear {
  font-size: 10px;
  padding: 2px 7px;
}

.log-entries {
  flex: 1;
  overflow-y: auto;
  padding: 3px 0;
}

.log-entry {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 6px;
  padding: 2px 12px;
  border-bottom: 1px solid rgba(30, 38, 47, 0.5);
  align-items: baseline;
  font-size: 11px;
  transition: background 0.1s;
}

.log-entry:hover {
  background: var(--bg2)
}

.log-topic {
  color: var(--text-hi);
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.log-payload {
  color: var(--text-dim);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.log-time {
  color: var(--text-dim);
  font-size: 10px;
  white-space: nowrap;
  padding-left: 8px;
}
</style>
