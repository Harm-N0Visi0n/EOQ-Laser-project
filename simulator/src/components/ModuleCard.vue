<script setup>
import { useModule } from '@/composables/useModule.js'
import BaseCard from '@/components/BaseCard.vue'
import RgbwInput from '@/components/RgbwInput.vue'

const props = defineProps(['id', 'real'])
defineEmits(['remove'])

const mod = useModule(props.id)
</script>

<template>
  <BaseCard type="MOD" :id="props.id" :real="props.real" :status-dot-class="mod.statusDotClass" :status-label="mod.statusLabel"
    class="mod-card" :class="{ hit: mod.hitFlash }" @remove="$emit('remove')">
    <div class="led-section">
      <div class="led-circle" :style="{ background: mod.colorCss, boxShadow: mod.ledGlow }"></div>
    </div>

    <template #actions>
      <input type="number" v-model.number="mod.hitPwm" min="0" max="100" class="pwm-input" title="PWM value"
        placeholder="PWM" />
      <button @click="mod.sendHit" class="btn-hit">HIT</button>
      <button @click="mod.sendPresent" class="btn-secondary">PRESENT</button>
    </template>

    <template #cmd>
      <div class="cmd-row">
        <span class="cmd-label">COLOR</span>
        <RgbwInput :color="mod.cmdColor" />
        <button @click="mod.setColor" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row">
        <span class="cmd-label">BLINK</span>
        <RgbwInput :color="mod.cmdBlink1" />
        <button @click="mod.sendBlink" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row blink-row2">
        <span class="cmd-label"></span>
        <RgbwInput :color="mod.cmdBlink2" />
        <div class="cmd-blink-time">
          <input type="number" v-model.number="mod.cmdBlinkTime" min="1" max="50" class="cmd-input-xs"
            title="Time (×100ms)" placeholder="t" />
          <span class="cmd-unit">×100ms</span>
        </div>
      </div>
    </template>
  </BaseCard>
</template>

<style scoped>
.mod-card {
  border-color: var(--mod);
  box-shadow: 0 0 0 1px rgba(8, 145, 178, 0.3), inset 0 1px 0 rgba(34, 211, 238, 0.04);
}

.mod-card:hover {
  box-shadow: 0 0 0 1px rgba(8, 145, 178, 0.5), 0 0 20px rgba(8, 145, 178, 0.08);
}

.mod-card.hit {
  box-shadow: 0 0 0 1px #fff, 0 0 40px rgba(255, 255, 255, 0.35);
  animation: hit-flash 0.5s ease-out;
}

@keyframes hit-flash {
  0% {
    box-shadow: 0 0 0 2px #fff, 0 0 60px rgba(255, 255, 255, 0.6)
  }

  100% {
    box-shadow: 0 0 0 1px rgba(8, 145, 178, 0.5)
  }
}

.dot-blink {
  background: var(--mod-hi);
  animation: blink 0.5s step-end infinite
}

@keyframes blink {
  50% {
    opacity: 0
  }
}

.led-section {
  display: flex;
  justify-content: center;
  padding: 4px 0
}

.led-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: background 0.15s ease, box-shadow 0.15s ease;
}

.pwm-input {
  width: 48px
}

.btn-hit {
  background: rgba(8, 145, 178, 0.1);
  border-color: var(--mod);
  color: var(--mod);
  font-weight: 600;
  letter-spacing: 0.08em;
}

.btn-hit:hover:not(:disabled) {
  background: rgba(8, 145, 178, 0.2);
  color: var(--mod-hi);
  border-color: var(--mod-hi);
}

.blink-row2 {
  margin-top: -2px
}

.cmd-blink-time {
  display: flex;
  align-items: center;
  gap: 3px;
  flex-shrink: 0
}

.cmd-unit {
  font-size: 9px;
  color: var(--text-dim);
  white-space: nowrap
}
</style>
