<script setup>
import { useDevicesStore } from '@/stores/devices.js'
import { useMqtt } from '@/composables/useMqtt.js'
import GunCard    from '@/components/GunCard.vue'
import ModuleCard from '@/components/ModuleCard.vue'

const store = useDevicesStore()
const { connected } = useMqtt()
</script>

<template>
  <main class="devices-area">
    <div class="panel">
      <div class="panel-header">
        <span class="panel-label gun-label">GUNS</span>
        <span class="panel-count">{{ store.guns.length }}</span>
        <button @click="store.addGun()" :disabled="!connected" class="btn-add btn-add-gun">+ GUN</button>
      </div>
      <div class="panel-cards">
        <div v-if="store.guns.length === 0" class="empty-hint">no guns added</div>
        <GunCard
          v-for="d in store.guns"
          :key="d.uid"
          :id="d.id"
          :real="d.real ?? false"
          @remove="store.remove(d.uid)"
        />
      </div>
    </div>

    <div class="divider"></div>

    <div class="panel">
      <div class="panel-header">
        <span class="panel-label mod-label">MODULES</span>
        <span class="panel-count">{{ store.modules.length }}</span>
        <button @click="store.addModule()" :disabled="!connected" class="btn-add btn-add-mod">+ MODULE</button>
      </div>
      <div class="panel-cards">
        <div v-if="store.modules.length === 0" class="empty-hint">no modules added</div>
        <ModuleCard
          v-for="d in store.modules"
          :key="d.uid"
          :id="d.id"
          :real="d.real ?? false"
          @remove="store.remove(d.uid)"
        />
      </div>
    </div>
  </main>
</template>

<style scoped>
.devices-area {
  flex: 1;
  overflow: hidden;
  display: flex;
  gap: 0;
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: var(--bg2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.panel-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.gun-label { color: var(--gun) }
.mod-label { color: var(--mod) }

.panel-count {
  font-size: 10px;
  color: var(--text-dim);
  flex: 1;
}

.btn-add {
  font-size: 10px;
  padding: 3px 8px;
}
.btn-add-gun { color: var(--gun); border-color: var(--gun) }
.btn-add-gun:hover:not(:disabled) { background: var(--gun-glow) }
.btn-add-mod { color: var(--mod); border-color: var(--mod) }
.btn-add-mod:hover:not(:disabled) { background: var(--mod-glow) }

.panel-cards {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  align-content: flex-start;
}

.divider {
  width: 1px;
  background: var(--border);
  flex-shrink: 0;
}

.empty-hint {
  color: var(--text-dim);
  font-size: 11px;
  letter-spacing: 0.06em;
  padding: 4px 0;
}
</style>
