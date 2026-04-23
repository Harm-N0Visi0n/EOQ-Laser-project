import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { publish, addHandler, removeHandler } from '@/composables/useMqtt.js'
import { blendRgbw, rgbwToCss } from '@/utils/color.js'

export function useModule(id) {
  const color = ref([0, 0, 0, 0])
  const blinking = ref(false)
  const hitFlash = ref(false)

  const hitPwm = ref(10)
  const cmdColor = reactive([0, 0, 0, 0])
  const cmdBlink1 = reactive([255, 0, 0, 0])
  const cmdBlink2 = reactive([0, 0, 255, 0])
  const cmdBlinkTime = ref(5)

  const colorCss = computed(() => {
    if (hitFlash.value) return '#ffffff'
    return rgbwToCss(color.value, '#111418')
  })

  const ledGlow = computed(() => {
    if (hitFlash.value) return '0 0 30px #ffffff, 0 0 60px rgba(255,255,255,0.4)'
    const [cr, cg, cb] = blendRgbw(color.value)
    if (cr + cg + cb === 0) return 'none'
    const intensity = Math.min(1, (cr + cg + cb) / 400)
    return `0 0 ${20 * intensity}px rgba(${cr},${cg},${cb},${0.6 * intensity}), 0 0 ${40 * intensity}px rgba(${cr},${cg},${cb},${0.2 * intensity})`
  })

  const statusLabel = computed(() => blinking.value ? 'BLINKING' : 'STANDBY')

  const statusDotClass = computed(() => blinking.value ? 'dot-blink' : 'dot-on')

  const ownPattern = `module/${id}/v1/#`
  const broadcastPattern = `module/*/v1/#`
  let blinkTimer = null
  let hitFlashTimer = null

  function clearBlink() {
    if (blinkTimer) { clearInterval(blinkTimer); blinkTimer = null }
    blinking.value = false
  }

  function doHitFlash() {
    hitFlash.value = true
    if (hitFlashTimer) clearTimeout(hitFlashTimer)
    hitFlashTimer = setTimeout(() => { hitFlash.value = false }, 500)
  }

  function handleMsg(topic, payload) {
    const cmd = topic.split('/')[3]
    switch (cmd) {
      case 'identify':
        publish(`module/${id}/v1/present`, '')
        break
      case 'fake-hit': {
        const pwm = payload.split(',')[0]
        doHitFlash()
        publish(`module/${id}/v1/hit-1`, pwm)
        break
      }
      case 'color':
        clearBlink()
        color.value = payload.split(',').map(Number).slice(0, 4)
        break
      case 'blink': {
        clearBlink()
        const nums = payload.split(',').map(Number)
        const c1 = nums.slice(0, 4)
        const c2 = nums.slice(5, 9)
        const t = Math.max(100, (nums[4] || 5) * 100)
        let toggle = false
        color.value = c1
        blinking.value = true
        blinkTimer = setInterval(() => {
          toggle = !toggle
          color.value = toggle ? c2 : c1
        }, t)
        break
      }
    }
  }

  function handleSystem(topic) {
    if (topic.split('/')[3] === 'identify') publish(`module/${id}/v1/present`, '')
  }

  function setColor() { publish(`module/${id}/v1/color`, cmdColor.join(',')) }
  function sendHit() { publish(`module/${id}/v1/hit-1`, String(hitPwm.value)) }
  function sendPresent() { publish(`module/${id}/v1/present`, '') }

  function sendBlink() {
    const t = cmdBlinkTime.value || 5
    publish(`module/${id}/v1/blink`, [...cmdBlink1, t, ...cmdBlink2, t].join(','))
  }

  // ── lifecycle ──────────────────────────────────────────────────────────────
  onMounted(() => {
    addHandler(ownPattern, handleMsg)
    addHandler(broadcastPattern, handleMsg)
    addHandler('system/#', handleSystem)
    publish(`module/${id}/v1/present`, '')
  })

  onUnmounted(() => {
    clearBlink()
    if (hitFlashTimer) clearTimeout(hitFlashTimer)
    removeHandler(ownPattern, handleMsg)
    removeHandler(broadcastPattern, handleMsg)
    removeHandler('system/#', handleSystem)
  })

  return reactive({
    blinking, hitFlash,
    hitPwm, cmdColor, cmdBlink1, cmdBlink2, cmdBlinkTime,
    colorCss, ledGlow, statusLabel, statusDotClass,
    sendHit, sendPresent, sendBlink, setColor,
  })
}
