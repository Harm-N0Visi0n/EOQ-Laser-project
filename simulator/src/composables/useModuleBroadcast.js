import { reactive } from 'vue'
import { publish } from '@/composables/useMqtt.js'

export function useModuleBroadcast() {
  const color = reactive([0, 0, 0, 0])
  return {
    color,
    setColor: () => publish('module/*/v1/color', color.join(',')),
  }
}
