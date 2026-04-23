import { ref, reactive } from 'vue'
import { publish } from '@/composables/useMqtt.js'

export function useGunBroadcast() {
  const ammo = ref(100)
  const pwm = ref(50)

  return reactive({
    ammo, pwm,
    setAmmo: () => publish('gun/*/v1/ammo', ammo.value),
    setPwm: () => publish('gun/*/v1/pwm', pwm.value),
  })
}
