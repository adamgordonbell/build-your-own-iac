<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  kind: { type: String, default: 'editor' }, // 'editor' | 'terminal'
  // when set, the body becomes a scroll box that follows the clicks — the
  // transcript grows past the slide and we ride it down, like a real terminal
  maxHeight: { type: String, default: '' },
})

const body = ref(null)
let obs = null

// v-click keeps hidden blocks in the layout at opacity 0, so "the bottom" is
// the last block that is NOT hidden, not the true scrollHeight.
function follow() {
  const el = body.value
  if (!el) return
  const shown = el.querySelectorAll('.slidev-vclick-target:not(.slidev-vclick-hidden)')
  const last = shown[shown.length - 1]
  if (!last) { el.scrollTop = 0; return }
  const top = last.offsetTop + last.offsetHeight - el.clientHeight
  // don't nudge by a few pixels and clip the first line — snap to the top instead
  el.scrollTo({ top: top < 24 ? 0 : top, behavior: 'smooth' })
}

onMounted(() => {
  if (!body.value || !props.maxHeight) return   // only scroll boxes need the observer
  obs = new MutationObserver(() => nextTick(follow))
  obs.observe(body.value, { subtree: true, attributes: true, attributeFilter: ['class'] })
  nextTick(follow)
})
onBeforeUnmount(() => obs && obs.disconnect())
</script>

<template>
  <div class="win" :class="kind">
    <div class="win-bar">
      <span class="dot" /><span class="dot" /><span class="dot" />
      <span class="win-title">{{ title }}</span>
    </div>
    <div
      ref="body"
      class="win-body"
      :class="{ 'win-scroll': maxHeight }"
      :style="maxHeight ? { maxHeight } : null"
    >
      <slot />
    </div>
  </div>
</template>

<style scoped>
.win {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(128, 128, 128, 0.35);
  margin: 0.5rem 0;
}
.win-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  background: var(--w-bar);
}
.dot { width: 11px; height: 11px; border-radius: 50%; background: #5a5a63; }
.dot:nth-child(1) { background: #e0655a; }
.dot:nth-child(2) { background: #e0b23e; }
.dot:nth-child(3) { background: #4f9e5c; }
.win-title {
  margin-left: 10px;
  font-size: 0.7rem;
  color: var(--w-title);
  font-family: ui-monospace, monospace;
}
.win-body { background: var(--w-body); }
.win.terminal .win-body {
  padding: 10px 14px;
  font-family: ui-monospace, monospace;
  font-size: 0.78rem;
  line-height: 1.45;
  color: var(--w-fg);
  min-height: 2rem;
}
/* let slidev's code blocks sit flush inside the editor window */
.win.editor .win-body :deep(pre) { margin: 0; border-radius: 0; }
/* terminal: fences stack seamlessly as one dark session, no card look */
.win.terminal .win-body { padding: 4px 0; }
.win.terminal .win-body :deep(pre) {
  margin: 0 !important;
  border-radius: 0 !important;
  border: none !important;
  background: transparent !important;
  padding: 4px 16px !important;
}
.win.terminal .win-body :deep(.slidev-code-line-numbers),
.win.terminal .win-body :deep(.line-number) { display: none; }

/* scroll box: the transcript is taller than the slide and the clicks walk it */
.win-body.win-scroll {
  overflow-y: auto;
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(128, 128, 128, 0.35) transparent;
}
.win-body.win-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
.win-body.win-scroll::-webkit-scrollbar-thumb {
  background: rgba(128, 128, 128, 0.35);
  border-radius: 3px;
}
.win-body.win-scroll::-webkit-scrollbar-track { background: transparent; }
</style>
