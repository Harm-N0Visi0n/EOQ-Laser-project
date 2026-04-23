<script setup>
import { ref } from 'vue'
import { useMqtt } from '@/composables/useMqtt.js'
import { useDevicesStore } from '@/stores/devices.js'

const { connect, disconnect, connected } = useMqtt()
const brokerUrl = ref(window.__MQTT_URL__ || 'ws://localhost:9001')
const store = useDevicesStore()
</script>

<template>
  <header class="topbar">
    <div class="logo">
      <span class="logo-text">[ COLAT SIM ]</span>
    </div>

    <button v-if="store.hasRealDevices" @click="store.showReal = !store.showReal"
      class="btn-real-toggle" :class="{ active: store.showReal }">
      REAL
    </button>

    <div class="connect-group">
      <div class="status-indicator" :class="connected ? 'conn' : 'disc'">
        <span class="status-pip"></span>
        <span>{{ connected ? 'CONNECTED' : 'OFFLINE' }}</span>
      </div>
      <input type="text" v-model="brokerUrl" :disabled="connected" class="url-input" />
      <button v-if="!connected" @click="connect(brokerUrl)" class="btn-connect">CONNECT</button>
      <button v-else @click="disconnect()" class="btn-disconnect">DISCONNECT</button>
    </div>

  </header>
</template>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 0 16px;
  height: 48px;
  flex-shrink: 0;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
}

.logo {
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.12em;
  white-space: nowrap
}

.logo-text {
  color: var(--text-hi)
}

.connect-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  letter-spacing: 0.08em;
  white-space: nowrap
}

.status-pip {
  width: 7px;
  height: 7px;
  border-radius: 50%
}

.conn {
  color: var(--green)
}

.conn .status-pip {
  background: var(--green);
  box-shadow: 0 0 5px var(--green)
}

.disc {
  color: var(--text-dim)
}

.disc .status-pip {
  background: var(--text-dim)
}

.url-input {
  width: 230px
}

.btn-connect:hover:not(:disabled) {
  background: rgba(34, 197, 94, 0.1)
}

.btn-disconnect:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1)
}

.btn-real-toggle {
  color: #f59e0b;
  border-color: #f59e0b;
  font-size: 10px;
  letter-spacing: 0.1em;
  opacity: 0.4;
}

.btn-real-toggle.active {
  opacity: 1;
  background: rgba(245, 158, 11, 0.1);
}

.btn-real-toggle:hover {
  opacity: 1;
}

.btn-connect {
  color: var(--green);
  border-color: var(--green)
}

.btn-disconnect {
  color: var(--red);
  border-color: var(--red)
}
</style>
