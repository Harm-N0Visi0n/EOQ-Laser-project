<script setup>
defineProps({ color: { type: Array, required: true } })
</script>

<template>
  <div class="cmd-rgbw">
    <input type="number" v-model.number="color[0]" min="0" max="255" placeholder="R" class="cmd-input-xs" />
    <input type="number" v-model.number="color[1]" min="0" max="255" placeholder="G" class="cmd-input-xs" />
    <input type="number" v-model.number="color[2]" min="0" max="255" placeholder="B" class="cmd-input-xs" />
    <input type="number" v-model.number="color[3]" min="0" max="255" placeholder="W" class="cmd-input-xs" />
  </div>
</template>
