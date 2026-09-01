<script setup>
// The triangle from earlier, with one edge (or the State corner) lit and the
// rest dimmed. Used three times at the roll-call: same picture, new labels.
defineProps({
  focus: { type: String, default: 'ps' }, // 'ps' | 'sc' | 'state'
})
</script>

<template>
  <div class="tf">
    <svg viewBox="0 0 460 300">
      <!-- edges -->
      <line x1="190" y1="68" x2="112" y2="210" stroke="#3b82f6" stroke-width="2.5"
            :style="{ opacity: focus === 'ps' ? 1 : 0.18 }" />
      <line x1="270" y1="68" x2="348" y2="210" stroke="#6b6b7d" stroke-width="2.5"
            stroke-dasharray="7 7" style="opacity:0.18" />
      <line x1="160" y1="240" x2="300" y2="240" stroke="#f59e0b" stroke-width="2.5"
            :style="{ opacity: focus === 'sc' ? 1 : 0.18 }" />

      <!-- Program -->
      <g :style="{ opacity: focus === 'state' ? 0.3 : 1 }">
        <rect x="150" y="16" width="160" height="52" rx="9" fill="#1e2430" stroke="#3b82f6" stroke-width="1.8"/>
        <text x="230" y="48" text-anchor="middle" fill="#e8e8ef" style="font-size:17px;font-weight:600">Program</text>
      </g>

      <!-- State -->
      <g>
        <rect x="10" y="214" width="150" height="52" rx="9" fill="#1e2430"
              :stroke="focus === 'state' ? '#3b82f6' : '#3b82f6'"
              :stroke-width="focus === 'state' ? 3 : 1.8"/>
        <text x="85" y="246" text-anchor="middle" fill="#e8e8ef" style="font-size:17px;font-weight:600">State</text>
      </g>

      <!-- Cloud -->
      <g :style="{ opacity: focus === 'state' ? 0.3 : 1 }">
        <rect x="300" y="214" width="150" height="52" rx="9" fill="#2a2318" stroke="#f59e0b" stroke-width="1.8"/>
        <text x="375" y="246" text-anchor="middle" fill="#e8e8ef" style="font-size:17px;font-weight:600">Cloud</text>
      </g>
    </svg>

    <div class="labels"><slot /></div>
  </div>
</template>

<style scoped>
.tf { display: grid; grid-template-columns: 42% 1fr; gap: 1.6rem; align-items: center; margin-top: 0.6rem; }
.tf svg { width: 100%; height: auto; }
.labels :deep(p), .labels :deep(li) { margin: 0.42rem 0; }
.labels :deep(ul) { list-style: none; padding: 0; }
.labels { font-size: 1.05rem; line-height: 1.45; }
</style>
