<script setup>
import { useMqtt } from '@/composables/useMqtt.js'
import { useSystem } from '@/composables/useSystem.js'
import { useGunBroadcast } from '@/composables/useGunBroadcast.js'
import { useModuleBroadcast } from '@/composables/useModuleBroadcast.js'
import RgbwInput from '@/components/RgbwInput.vue'

const { connected } = useMqtt()
const sys = useSystem()
const gun = useGunBroadcast()
const mod = useModuleBroadcast()
</script>

<template>
  <div v-if="connected" class="broadcast-bar">
    <span class="bc-label">BROADCAST</span>
    <button @click="sys.identify()" class="bc-btn">IDENTIFY ALL</button>
    <button @click="sys.initGame()" class="bc-btn bc-btn-green">INIT GAME</button>
    <button @click="sys.endGame()" class="bc-btn bc-btn-red">END GAME</button>

    <div class="bc-sep"></div>
    <span class="bc-label">ALL GUNS</span>
    <input type="number" v-model.number="gun.ammo" min="0" class="bc-input" placeholder="ammo" />
    <button @click="gun.setAmmo()" class="bc-btn">SET AMMO</button>
    <input type="number" v-model.number="gun.pwm" min="0" max="100" class="bc-input" placeholder="pwm%" />
    <button @click="gun.setPwm()" class="bc-btn">SET PWM</button>

    <div class="bc-sep"></div>
    <span class="bc-label">ALL MODULES</span>
    <RgbwInput :color="mod.color" />
    <button @click="mod.setColor()" class="bc-btn">SET COLOR</button>
  </div>
</template>

<style scoped>
.broadcast-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 16px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  flex-wrap: wrap;
}

.bc-label {
  font-size: 9px;
  letter-spacing: 0.1em;
  color: var(--text-dim);
  white-space: nowrap;
}

.bc-sep {
  width: 1px;
  height: 16px;
  background: var(--border2);
  margin: 0 4px;
  flex-shrink: 0;
}

.bc-btn {
  font-size: 10px;
  padding: 3px 8px;
  white-space: nowrap;
}

.bc-btn-green {
  color: var(--green);
  border-color: var(--green)
}

.bc-btn-green:hover:not(:disabled) {
  background: rgba(34, 197, 94, 0.1)
}

.bc-btn-red {
  color: var(--red);
  border-color: var(--red)
}

.bc-btn-red:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.1)
}

.bc-input {
  width: 52px;
  font-size: 11px;
  padding: 3px 6px;
}

</style>
