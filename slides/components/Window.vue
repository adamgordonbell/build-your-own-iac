<script setup>
defineProps({
  title: { type: String, default: '' },
  kind: { type: String, default: 'editor' }, // 'editor' | 'terminal'
})
</script>

<template>
  <div class="win" :class="kind">
    <div class="win-bar">
      <span class="dot" /><span class="dot" /><span class="dot" />
      <span class="win-title">{{ title }}</span>
    </div>
    <div class="win-body">
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
</style>
