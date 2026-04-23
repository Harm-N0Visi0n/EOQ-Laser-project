import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { publish, addHandler, removeHandler } from '@/composables/useMqtt.js'
import { useDevicesStore } from '@/stores/devices.js'
import { rgbwToCss } from '@/utils/color.js'

export function useGun(id) {
  const ammo = ref(0)
  const maxAmmo = ref(100)
  const pwm = ref(50)
  const gunType = ref('single-shot')
  const ammoDepletion = ref(1)
  const teamColor = ref([0, 0, 0, 0])
  const firing = ref(false)
  const reloading = ref(false)

  const cmdAmmo = ref(100)
  const cmdPwm = ref(50)
  const cmdGunType = ref('single-shot')
  const cmdDepletion = ref(1)
  const cmdTeamColor = reactive([0, 0, 0, 0])
  const cmdTarget = ref('')

  const ammoBarPct = computed(() =>
    maxAmmo.value > 0 ? Math.round((ammo.value / maxAmmo.value) * 100) : 0
  )

  const teamColorCss = computed(() => rgbwToCss(teamColor.value, '#1a1a1a'))

  const statusLabel = computed(() => {
    if (firing.value) return 'FIRING'
    if (reloading.value) return 'RELOADING'
    if (ammo.value <= 0) return 'NO AMMO'
    return 'STANDBY'
  })

  const store = useDevicesStore()
  const moduleIds = computed(() => store.modules.map(m => m.id))

  const ownPattern = `gun/${id}/v1/#`
  const broadcastPattern = `gun/*/v1/#`
  let fireTimer = null

  function doShot() {
    if (ammo.value <= 0) { stopFiring(); return }
    ammo.value = Math.max(0, ammo.value - ammoDepletion.value)
    publish(`gun/${id}/v1/fire-start`, ammo.value)
    if (cmdTarget.value) {
      publish(`module/${cmdTarget.value}/v1/fake-hit`, `${pwm.value},1`)
    }
    if (ammo.value <= 0) stopFiring()
  }

  function stopFiring() {
    if (fireTimer) { clearInterval(fireTimer); fireTimer = null }
    if (firing.value) {
      firing.value = false
      publish(`gun/${id}/v1/fire-stop`, ammo.value)
    }
  }

  function handleMsg(topic, payload) {
    const cmd = topic.split('/')[3]
    switch (cmd) {
      case 'identify':
        publish(`gun/${id}/v1/present`, '')
        break
      case 'ammo': {
        const val = parseInt(payload) || 0
        ammo.value = val
        maxAmmo.value = Math.max(maxAmmo.value, val)
        reloading.value = true
        setTimeout(() => { reloading.value = false }, 1500)
        break
      }
      case 'pwm':
        pwm.value = parseInt(payload) || 50
        break
      case 'gun-type':
        gunType.value = payload.trim()
        break
      case 'ammo-depletion':
        ammoDepletion.value = parseInt(payload) || 1
        break
      case 'team-color':
        teamColor.value = payload.split(',').map(Number)
        break
    }
  }

  function handleSystem(topic) {
    if (topic.split('/')[3] === 'identify') publish(`gun/${id}/v1/present`, '')
  }

  function setAmmo() { publish(`gun/${id}/v1/ammo`, cmdAmmo.value) }
  function setPwm() { publish(`gun/${id}/v1/pwm`, cmdPwm.value) }
  function setGunType() { publish(`gun/${id}/v1/gun-type`, cmdGunType.value) }
  function setDepletion() { publish(`gun/${id}/v1/ammo-depletion`, cmdDepletion.value) }
  function setTeamColor() { publish(`gun/${id}/v1/team-color`, cmdTeamColor.join(',')) }

  function toggleFire() {
    if (firing.value) { stopFiring(); return }
    if (ammo.value <= 0) return
    if (gunType.value === 'continuous-mode') {
      firing.value = true
      doShot()
      fireTimer = setInterval(doShot, 1000)
    } else {
      doShot()
      setTimeout(() => publish(`gun/${id}/v1/fire-stop`, ammo.value), 120)
    }
  }

  function sendPresent() { publish(`gun/${id}/v1/present`, '') }

  // ── lifecycle ──────────────────────────────────────────────────────────────
  onMounted(() => {
    addHandler(ownPattern, handleMsg)
    addHandler(broadcastPattern, handleMsg)
    addHandler('system/#', handleSystem)
    publish(`gun/${id}/v1/present`, '')
  })

  onUnmounted(() => {
    stopFiring()
    removeHandler(ownPattern, handleMsg)
    removeHandler(broadcastPattern, handleMsg)
    removeHandler('system/#', handleSystem)
  })

  return reactive({
    ammo, pwm, gunType, ammoDepletion, teamColor, firing, reloading,
    ammoBarPct, teamColorCss, statusLabel,
    cmdAmmo, cmdPwm, cmdGunType, cmdDepletion, cmdTeamColor, cmdTarget,
    moduleIds,
    toggleFire, sendPresent,
    setAmmo, setPwm, setGunType, setDepletion, setTeamColor,
  })
}
