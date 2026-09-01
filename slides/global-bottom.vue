<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'
import ActNav from './components/ActNav.vue'

// Hide the strip on the cover — nothing has started yet.
const nav = useNav()
const show = computed(() => (nav.currentSlideNo?.value ?? 1) > 1)
</script>

<template>
  <div v-if="show" class="act-strip">
    <ActNav size="sm" />
  </div>
</template>

<style scoped>
.act-strip {
  position: absolute; top: 0.55rem; right: 0.8rem; z-index: 20;
  opacity: 0.75; transition: opacity .2s;
}
.act-strip:hover { opacity: 1; }
</style>
