import { publish } from '@/composables/useMqtt.js'

export function useSystem() {
  return {
    identify: () => publish('system/*/v1/identify', ''),
    initGame: () => publish('system/*/v1/init', ''),
    endGame: () => publish('system/*/v1/end', ''),
  }
}
