<script setup>
import { ref } from 'vue'

defineProps({
  type: { type: String, required: true },
  id: { type: String, required: true },
  statusDotClass: { type: String, required: true },
  statusLabel: { type: String, required: true },
  real: { type: Boolean, default: false },
})
defineEmits(['remove'])

const showCmds = ref(false)
</script>

<template>
  <div class="card">
    <div class="card-header">
      <div class="card-id-row">
        <span class="device-type">{{ type }}</span>
        <span v-if="real" class="badge-real">REAL</span>
        <span class="device-id">{{ id }}</span>
        <slot name="header-extras"></slot>
        <button v-if="!real" class="btn-x" @click="$emit('remove')" title="Remove">✕</button>
      </div>
      <div class="status-row">
        <span class="status-dot" :class="statusDotClass"></span>
        <span class="status-label">{{ statusLabel }}</span>
      </div>
    </div>

    <slot></slot>

    <div class="card-actions">
      <slot name="actions" />
      <button @click="showCmds = !showCmds" class="btn-toggle-cmd">
        {{ showCmds ? '▴' : '▾' }} CMD
      </button>
    </div>

    <div v-if="showCmds" class="cmd-panel">
      <slot name="cmd"></slot>
    </div>
  </div>
</template>
