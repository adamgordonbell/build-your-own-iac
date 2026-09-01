<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'

// Act strip: click to jump, completed acts struck through, current one lit.
// Boundaries are derived from each slide's routeAlias (I_*, II_*, …) so adding
// or cutting slides never needs touching this file.
const props = defineProps({
  size: { type: String, default: 'sm' }, // 'sm' (corner) | 'lg' (on a slide)
})

const NAMES = { I: 'why', II: 'the loop', III: 'the hard part', IV: 'land it' }
const ORDER = ['I', 'II', 'III', 'IV']

const nav = useNav()

const acts = computed(() => {
  const out = []
  const list = nav.slides?.value ?? []
  list.forEach((s, i) => {
    const alias = s?.meta?.slide?.frontmatter?.routeAlias ?? ''
    const m = /^(I|II|III|IV)_/.exec(alias)
    if (!m) return
    if (!out.length || out[out.length - 1].act !== m[1]) out.push({ act: m[1], start: i + 1 })
  })
  if (out.length) return out
  return [                              // fallback if frontmatter isn't reachable
    { act: 'I', start: 1 }, { act: 'II', start: 5 },
    { act: 'III', start: 20 }, { act: 'IV', start: 44 },
  ]
})

const here = computed(() => {
  const n = nav.currentSlideNo?.value ?? 1
  let cur = acts.value[0]?.act
  for (const a of acts.value) if (n >= a.start) cur = a.act
  return cur
})

const stateOf = (act) =>
  ORDER.indexOf(act) < ORDER.indexOf(here.value) ? 'done'
  : act === here.value ? 'now' : 'todo'
</script>

<template>
  <div class="acts" :class="size">
    <button v-for="a in acts" :key="a.act" :class="stateOf(a.act)" @click="nav.go(a.start)">
      <span class="num">{{ a.act }}</span>
      <span class="nm">{{ NAMES[a.act] }}</span>
    </button>
  </div>
</template>

<style scoped>
.acts { display: flex; align-items: center; gap: 0.35rem; font-family: ui-monospace, monospace; }
button {
  display: flex; align-items: baseline; gap: 0.3em;
  background: none; border: 1px solid transparent; border-radius: 5px;
  padding: 1px 6px; cursor: pointer; color: var(--dg-muted); line-height: 1.5;
  transition: opacity .2s, color .2s;
}
button:hover { border-color: var(--dg-border); color: var(--dg-fg); }
.num { font-weight: 700; }
.sm button { font-size: 0.52rem; }
.lg button { font-size: 0.95rem; padding: 3px 10px; }
.sm .nm { display: none; }

/* done: struck through and faded — you have been here */
button.done { opacity: 0.32; text-decoration: line-through; text-decoration-thickness: 1px; }
/* now: lit, and the only one that shows its name in the small strip */
button.now { color: #3b82f6; border-color: #3b82f6; opacity: 1; }
.sm button.now .nm { display: inline; }
/* todo: present but quiet */
button.todo { opacity: 0.55; }
</style>
