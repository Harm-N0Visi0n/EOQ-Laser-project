import mqtt from 'mqtt'
import { ref, reactive } from 'vue'

const connected = ref(false)
const messages = reactive([])
const handlers = []
let client = null
let msgSeq = 0

function matchTopic(pattern, topic) {
  const pp = pattern.split('/')
  const tp = topic.split('/')
  for (let i = 0; i < pp.length; i++) {
    if (pp[i] === '#') return true
    if (pp[i] === '+') { if (i >= tp.length) return false; continue }
    if (pp[i] !== tp[i]) return false
  }
  return pp.length === tp.length
}

export function connect(url) {
  if (client) { client.end(true); client = null; connected.value = false }
  client = mqtt.connect(url)
  client.on('connect', () => {
    connected.value = true
    const patterns = [...new Set(handlers.map(h => h.pattern))]
    patterns.forEach(p => client.subscribe(p))
  })
  client.on('close', () => { connected.value = false })
  client.on('error', (e) => console.error('[MQTT]', e.message))
  client.on('message', (topic, payload) => {
    const str = payload.toString()
    messages.unshift({ id: msgSeq++, topic, payload: str, ts: Date.now() })
    if (messages.length > 200) messages.pop()
    handlers.forEach(h => { if (matchTopic(h.pattern, topic)) h.cb(topic, str) })
  })
}

export function disconnect() {
  if (client) { client.end(); client = null }
  connected.value = false
}

export function publish(topic, payload = '') {
  if (!client || !connected.value) return
  client.publish(topic, String(payload))
}

export function addHandler(pattern, cb) {
  handlers.push({ pattern, cb })
  if (client && connected.value) client.subscribe(pattern)
}

export function removeHandler(pattern, cb) {
  const i = handlers.findIndex(h => h.pattern === pattern && h.cb === cb)
  if (i !== -1) handlers.splice(i, 1)
  if (!handlers.some(h => h.pattern === pattern) && client) client.unsubscribe(pattern)
}

export function useMqtt() {
  return { connected, messages, connect, disconnect, publish, addHandler, removeHandler }
}
