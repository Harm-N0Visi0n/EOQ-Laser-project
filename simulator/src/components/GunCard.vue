<script setup>
import { useGun } from '@/composables/useGun.js'
import BaseCard from '@/components/BaseCard.vue'
import RgbwInput from '@/components/RgbwInput.vue'

const props = defineProps(['id', 'real'])
defineEmits(['remove'])

const gun = useGun(props.id)
</script>

<template>
  <BaseCard type="GUN" :id="props.id" :real="props.real" status-dot-class="dot-on" :status-label="gun.statusLabel" class="gun-card"
    :class="{ firing: gun.firing, 'no-ammo': gun.ammo <= 0 }" @remove="$emit('remove')">
    <template #header-extras>
      <div class="team-led" :style="{ background: gun.teamColorCss, boxShadow: `0 0 6px ${gun.teamColorCss}` }"
        title="Team color" />
    </template>

    <div class="ammo-section">
      <div class="ammo-label-row">
        <span class="field-label">AMMO</span>
        <span class="ammo-value" :class="{ reloading: gun.reloading, 'ammo-low': gun.ammo > 0 && gun.ammo <= 10 }">
          {{ gun.reloading ? 'RELOADING…' : gun.ammo }}
        </span>
      </div>
      <div class="ammo-bar">
        <div class="ammo-fill" :style="{ width: gun.ammoBarPct + '%' }"></div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat">
        <span class="field-label">PWM</span>
        <span class="field-val">{{ gun.pwm }}%</span>
      </div>
      <div class="stat">
        <span class="field-label">TYPE</span>
        <span class="field-val type-val">{{ gun.gunType === 'continuous-mode' ? 'CONT' : 'SINGLE' }}</span>
      </div>
    </div>

    <template #actions>
      <select v-model="gun.cmdTarget" class="target-select" title="Target module">
        <option value="">MISS</option>
        <option v-for="modId in gun.moduleIds" :key="modId" :value="modId">{{ modId }}</option>
      </select>
      <button @click="gun.toggleFire" :class="['btn-fire', { active: gun.firing }]"
        :disabled="gun.ammo <= 0 && !gun.firing">{{ gun.firing ? '■ STOP' : '▶ FIRE' }}</button>
      <button @click="gun.sendPresent" class="btn-secondary">PRESENT</button>
    </template>

    <template #cmd>
      <div class="cmd-row">
        <span class="cmd-label">AMMO</span>
        <input type="number" v-model.number="gun.cmdAmmo" min="0" class="cmd-input-sm" />
        <button @click="gun.setAmmo" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row">
        <span class="cmd-label">PWM %</span>
        <input type="number" v-model.number="gun.cmdPwm" min="0" max="100" class="cmd-input-sm" />
        <button @click="gun.setPwm" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row">
        <span class="cmd-label">TYPE</span>
        <select v-model="gun.cmdGunType" class="cmd-select">
          <option value="single-shot">single-shot</option>
          <option value="continuous-mode">continuous</option>
        </select>
        <button @click="gun.setGunType" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row">
        <span class="cmd-label">DEPLET</span>
        <input type="number" v-model.number="gun.cmdDepletion" min="1" class="cmd-input-sm" />
        <button @click="gun.setDepletion" class="cmd-btn">SET</button>
      </div>
      <div class="cmd-row">
        <span class="cmd-label">TEAM</span>
        <RgbwInput :color="gun.cmdTeamColor" />
        <button @click="gun.setTeamColor" class="cmd-btn">SET</button>
      </div>
    </template>
  </BaseCard>
</template>

<style scoped>
.gun-card {
  border-color: var(--gun);
  box-shadow: 0 0 0 1px rgba(217, 119, 6, 0.3), inset 0 1px 0 rgba(251, 191, 36, 0.05);
}

.gun-card:hover {
  box-shadow: 0 0 0 1px rgba(217, 119, 6, 0.5), 0 0 20px rgba(217, 119, 6, 0.08);
}

.gun-card.firing {
  border-color: var(--gun-hi);
  box-shadow: 0 0 0 1px var(--gun-hi), 0 0 24px rgba(245, 158, 11, 0.25);
  animation: fire-pulse 0.4s ease-in-out infinite alternate;
}

@keyframes fire-pulse {
  from {
    box-shadow: 0 0 0 1px var(--gun-hi), 0 0 16px rgba(245, 158, 11, 0.2)
  }

  to {
    box-shadow: 0 0 0 1px var(--gun-hi), 0 0 32px rgba(245, 158, 11, 0.4)
  }
}

.ammo-bar {
  height: 3px;
  background: var(--border);
  border-radius: 1px;
  margin-top: 4px;
}

.ammo-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gun), var(--gun-hi));
  border-radius: 1px;
  transition: width 0.3s ease;
}

.ammo-value {
  color: var(--gun-hi);
  font-weight: 600;
  font-size: 14px
}

.ammo-value.reloading {
  color: var(--amber);
  animation: blink 0.6s step-end infinite
}

.ammo-value.ammo-low {
  color: var(--red)
}

@keyframes blink {
  50% {
    opacity: 0
  }
}

.target-select {
  width: 80px;
  font-size: 10px
}

.btn-fire {
  flex: 1;
  background: rgba(217, 119, 6, 0.1);
  border-color: var(--gun);
  color: var(--gun);
  font-weight: 600;
  letter-spacing: 0.08em;
}

.btn-fire:hover:not(:disabled) {
  background: rgba(217, 119, 6, 0.2);
  color: var(--gun-hi);
  border-color: var(--gun-hi);
}

.btn-fire.active {
  background: rgba(239, 68, 68, 0.15);
  border-color: var(--red);
  color: var(--red);
}
</style>
