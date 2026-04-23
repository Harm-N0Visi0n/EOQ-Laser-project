import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'colat-devices'

function loadVirtualState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      return { devices: parsed.devices ?? [], uidCounter: parsed.uidCounter ?? 1 }
    }
  } catch { }
  return null
}

function parseRealDevices() {
  const parse = (globalKey, type) =>
    (window[globalKey] || '').split(',').map(s => s.trim()).filter(Boolean)
      .map(id => ({ uid: `real:${id}`, type, id, real: true }))
  return [...parse('__REAL_GUNS__', 'gun'), ...parse('__REAL_MODULES__', 'module')]
}

export const useDevicesStore = defineStore('devices', () => {
  const saved = loadVirtualState()
  const realDevices = parseRealDevices()

  const devices = ref([...(saved?.devices ?? []), ...realDevices])
  let uidCounter = saved?.uidCounter ?? 1

  const showReal = ref(true)
  const hasRealDevices = computed(() => devices.value.some(d => d.real))

  const guns = computed(() => devices.value.filter(d => d.type === 'gun' && (showReal.value || !d.real)))
  const modules = computed(() => devices.value.filter(d => d.type === 'module' && (showReal.value || !d.real)))

  function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      devices: devices.value.filter(d => !d.real),
      uidCounter,
    }))
  }

  watch(devices, persist, { deep: true })

  function randomHexId() {
    const existing = new Set(devices.value.map(d => d.id))
    let id
    do {
      id = '0x' + Math.floor(Math.random() * 0xffffffff + 1).toString(16).padStart(8, '0')
    } while (existing.has(id))
    return id
  }

  function addGun() {
    devices.value.push({ uid: uidCounter++, type: 'gun', id: randomHexId() })
  }

  function addModule() {
    devices.value.push({ uid: uidCounter++, type: 'module', id: randomHexId() })
  }

  function remove(uid) {
    devices.value = devices.value.filter(d => d.uid !== uid || d.real)
  }

  return { guns, modules, addGun, addModule, remove, showReal, hasRealDevices }
})
