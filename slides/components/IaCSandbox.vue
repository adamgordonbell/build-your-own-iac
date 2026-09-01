<script setup>
import { ref, computed, watch } from 'vue'

// The whole toy: three columns, and however many buttons the engine has earned.
//   Program  — you edit it (intent, logical names, no IDs)
//   State    — the tool writes it (name -> id, plus the tag as of last run)
//   Cloud    — reality (IDs, no idea which things are yours)
//
// `stage` gates which buttons exist. It is a verb budget, not a folder number —
// the `src/` steps were renumbered 2026-08-31 and renamed to the concept ladder
// (1-cli · 2-api · 3-state · 4-graph …) 2026-09-01, and these values
// deliberately did not move. `up` always runs the full loop — visit 1 (right after the
// matching-problem triangle, before any code) demos the destination, and the
// engine spends the next steps catching up. What grows:
//   1 — `up` only: the loop itself, deletes included. No plan, no refresh, no
//       way to touch the cloud behind the tool's back. Visit 1, before any
//       engine code.
//   3 — `plan` appears: the same three sets `up` would apply, printed and not
//       applied. The visit after step 3's line-count slide (`src/3-state`,
//       the one engine file: state + diff + loop).
//   6 — everything: refresh, `+ portal`, per-row ✕, editable cloud tags. The
//       drift visit (`src/6-drift`), where those buttons are the beat.

const props = defineProps({
  stage: { type: Number, default: 6 },
})

const hasPlan = computed(() => props.stage >= 3)
const full = computed(() => props.stage >= 6)

const SUB = '/subscriptions/8fa2…/resourceGroups'

const programText = ref(`rg:
  tag: demo
storage:
  tag: demo`)

const state = ref({})   // { name: { id, tag } }
const cloud = ref([])   // [ { id, tag } ]
const log = ref('')
const flash = ref('')

// ---- parse: ten lines, no YAML dependency ---------------------------------

const program = computed(() => {
  const out = {}
  let cur = null
  for (const line of programText.value.split('\n')) {
    const head = line.match(/^([A-Za-z][\w-]*):\s*$/)
    if (head) { cur = head[1]; out[cur] = { tag: '' }; continue }
    const tag = line.match(/^\s+tag:\s*(.+?)\s*$/)
    if (tag && cur) out[cur].tag = tag[1]
  }
  return out
})

// two blocks with the same key are one wish written twice — the name IS the
// identity, so the toy refuses instead of silently keeping the last one
const dupes = computed(() => {
  const seen = new Set(), out = new Set()
  for (const line of programText.value.split('\n')) {
    const head = line.match(/^([A-Za-z][\w-]*):\s*$/)
    if (head) { if (seen.has(head[1])) out.add(head[1]); seen.add(head[1]) }
  }
  return [...out]
})

function refuseDupes() {
  if (!dupes.value.length) return false
  planned.value = null
  applied.value = {
    items: dupes.value.map((name) => ({ glyph: '!', name, kind: 'noidea' })),
    note: 'duplicate names — the name is the identity, give each its own',
  }
  flashStrip()
  return true
}

const idFor = (name) => `${SUB}/${name}`
const cloudAt = (id) => cloud.value.find((r) => r.id === id)

// ---- diff: desired vs state, same three lists as engine.py ----------------

function diff() {
  const desired = program.value, st = state.value
  return {
    creates: Object.keys(desired).filter((k) => !(k in st)),
    deletes: Object.keys(st).filter((k) => !(k in desired)),
    updates: Object.keys(desired).filter((k) => k in st && desired[k].tag !== st[k].tag),
  }
}

function touch(pane) { flash.value = pane; setTimeout(() => (flash.value = ''), 600) }

// ---- the strip: what the last verb said, big enough to read ---------------
// plan's preview and up's per-resource report share it; whichever ran last wins.

const planned = ref(null)       // plan preview: [ { glyph, verb, name } ] — or null
const applied = ref(null)       // up's report, same shape — or null
const strip = computed(() =>
  planned.value ? { label: 'plan', items: planned.value, note: 'nothing applied', empty: 'no changes.' }
  : applied.value ? { label: 'up', items: applied.value.items, note: applied.value.note, empty: 'no changes — nothing sent.' }
  : null)
const planFlash = ref(false)
function flashStrip() { planFlash.value = true; setTimeout(() => (planFlash.value = false), 600) }

// ---- plan: the same three sets, printed, nothing touched -------------------

function plan() {
  if (refuseDupes()) return
  const { creates, updates, deletes } = diff()
  planned.value = [
    ...creates.map((name) => ({ glyph: '+', name, kind: 'create' })),
    ...updates.map((name) => ({ glyph: '~', name, kind: 'update' })),
    ...deletes.map((name) => ({ glyph: '-', name, kind: 'delete' })),
  ]
  log.value = ''            // the strip below says it; the bar stays quiet
  flashStrip()
  // no touch(): no pane changed, which is the entire point of plan
}

// a plan goes stale the moment the Program does
watch(programText, () => { planned.value = null })

// ---- up: reconcile ---------------------------------------------------------
// The full loop at every stage — create, update, delete, and `=` for the
// untouched. Visit 1 demos the destination; step 3's engine then builds it.
// What grows with `stage` is the OTHER verbs.

function up() {
  if (refuseDupes()) return
  planned.value = null
  const { creates, updates, deletes } = diff()
  const items = []
  for (const name of deletes) {
    const id = state.value[name].id
    cloud.value = cloud.value.filter((r) => r.id !== id)
    delete state.value[name]
    items.push({ glyph: '-', name, kind: 'delete' })
  }
  for (const name of Object.keys(program.value)) {
    if (creates.includes(name)) {
      const id = idFor(name), tag = program.value[name].tag
      cloud.value.push({ id, tag })
      state.value[name] = { id, tag }          // save after each, like the engine
      items.push({ glyph: '+', name, kind: 'create' })
    } else if (updates.includes(name)) {
      const tag = program.value[name].tag
      const row = cloudAt(state.value[name].id)
      if (row) row.tag = tag
      state.value[name].tag = tag
      items.push({ glyph: '~', name, kind: 'update' })
    } else {
      items.push({ glyph: '=', name, kind: 'skip' })
    }
  }
  const sent = items.some((i) => i.kind !== 'skip')
  applied.value = { items, note: sent ? '' : 'nothing sent' }
  flashStrip()
  if (sent) touch('cloud')
}

// ---- refresh: ask the cloud what is ACTUALLY there -------------------------

function refresh() {
  const lines = []
  for (const name of Object.keys(state.value)) {
    const row = cloudAt(state.value[name].id)
    if (!row) {
      delete state.value[name]
      lines.push(`! ${name} vanished`)
    } else if (row.tag !== state.value[name].tag) {
      state.value[name].tag = row.tag
      lines.push(`~ ${name}`)
    } else {
      lines.push(`= ${name}`)
    }
  }
  log.value = lines.join('   ') || 'state is empty.'
  touch('state')
}

// somebody else opens the portal and makes something we never asked for
let portalN = 0
function createInCloud() {
  const name = `legacy-${++portalN}`
  cloud.value.push({ id: idFor(name), tag: 'prod' })
  log.value = 'created in the portal. (nothing else knows about it)'
  touch('cloud')
}

// a cloud row nobody's state points at — the tool cannot see it as "ours"
const managed = computed(() => new Set(Object.values(state.value).map((v) => v.id)))

function destroyInCloud(id) {
  cloud.value = cloud.value.filter((r) => r.id !== id)
  log.value = 'deleted in the portal. (we were not asked)'
  touch('cloud')
}

function reset() {
  state.value = {}
  cloud.value = []
  log.value = ''
  planned.value = null
  applied.value = null
}
</script>

<template>
  <div class="sandbox">
    <!-- the same triangle as the previous slide, made live -->
    <svg class="edges" viewBox="0 0 100 100" preserveAspectRatio="none">
      <line x1="40" y1="34" x2="24" y2="53" stroke="#3b82f6" stroke-width="0.4" />
      <line x1="60" y1="34" x2="76" y2="53" style="stroke:var(--dg-line)" stroke-width="0.4" stroke-dasharray="1.6 1.6" />
      <line x1="42" y1="80" x2="58" y2="80" stroke="#f59e0b" stroke-width="0.4" />
    </svg>

    <!-- PROGRAM -->
    <div class="pane program">
      <div class="pane-head">Program <span>you edit this</span></div>
      <textarea v-model="programText" spellcheck="false" />
    </div>

    <!-- STATE -->
    <div class="pane state" :class="{ flash: flash === 'state' }">
      <div class="pane-head">State <span>the tool writes this</span></div>
      <div class="body">
        <div v-if="!Object.keys(state).length" class="empty">empty</div>
        <div v-for="(v, name) in state" :key="name" class="row">
          <div><b>{{ name }}</b> <span class="arrow">→</span> <span class="id">{{ v.id }}</span></div>
          <div class="sub">tag: {{ v.tag }}</div>
        </div>
      </div>
    </div>

    <!-- CLOUD -->
    <div class="pane cloud" :class="{ flash: flash === 'cloud' }">
      <div class="pane-head">
        Cloud
        <button v-if="full" class="portal" title="create one in the portal" @click="createInCloud">+ portal</button>
        <span v-else>what actually exists</span>
      </div>
      <div class="body">
        <div v-if="!cloud.length" class="empty">empty</div>
        <div v-for="r in cloud" :key="r.id" class="row">
          <div class="rowtop">
            <span class="id">{{ r.id }}</span>
            <button v-if="full" class="x" title="delete in the portal" @click="destroyInCloud(r.id)">✕</button>
          </div>
          <div class="sub">
            <template v-if="!full">tag: {{ r.tag }}</template>
            <template v-else>
              tag: <input v-model="r.tag" spellcheck="false" />
              <span v-if="!managed.has(r.id)" class="chip">unmanaged</span>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- controls sit inside the triangle -->
    <div class="bar">
      <div class="btns">
        <button v-if="hasPlan" class="go" @click="plan">plan</button>
        <button class="go" @click="up">up</button>
        <button v-if="full" class="go" @click="refresh">refresh</button>
        <button class="ghost" @click="reset">reset</button>
      </div>
      <code class="log">{{ log || ' ' }}</code>
    </div>

    <!-- the strip: plan's preview, or up's per-resource report — the generated diff, readable -->
    <div class="planout" :class="{ flash: planFlash, filled: strip }">
      <template v-if="strip">
        <span class="planlab">{{ strip.label }}</span>
        <span v-if="!strip.items.length" class="planempty">{{ strip.empty }}</span>
        <span v-for="p in strip.items" :key="p.glyph + p.name" class="pitem" :class="p.kind">
          <b>{{ p.glyph }}</b> {{ p.name }}
        </span>
        <span v-if="strip.note" class="planempty">— {{ strip.note }}</span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.sandbox {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.68rem;
  position: relative;
  display: grid;
  grid-template-columns: 1fr 124px 1fr;
  column-gap: 0;
  row-gap: 1.9rem;
  padding-top: 0.2rem;
}
.edges { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.program { grid-column: 1 / -1; justify-self: center; width: 44%; }
.state { grid-column: 1; }
.cloud { grid-column: 3; }
.bar {
  position: absolute; left: 50%; top: 58%; transform: translate(-50%, -50%);
  z-index: 2; width: 104px; display: flex; flex-direction: column; align-items: stretch; gap: 0.25rem;
  background: var(--w-panel); padding: 0.32rem 0.34rem; border-radius: 7px; border: 1px solid var(--dg-border);
}
.btns { display: flex; flex-direction: column; gap: 0.25rem; }
.pane {
  position: relative; z-index: 1;
  border: 1px solid rgba(128,128,128,0.35); border-radius: 8px; overflow: hidden;
  background: var(--w-body); transition: box-shadow .25s;
}
.pane.flash { box-shadow: 0 0 0 2px #3b82f6; }
.pane-head {
  padding: 5px 10px; background: var(--w-bar); color: var(--dg-fg);
  font-weight: 600; font-size: 0.72rem; display: flex; justify-content: space-between; align-items: baseline;
}
.pane-head span { color: var(--dg-muted); font-weight: 400; font-size: 0.62rem; }
textarea {
  width: 100%; height: 96px; resize: none; border: 0; outline: none;
  background: var(--w-body); color: var(--w-fg); padding: 8px 10px;
  font-family: inherit; font-size: inherit; line-height: 1.55;
}
.body { height: 134px; overflow-y: auto; padding: 8px 10px; color: var(--w-fg); line-height: 1.5; }
.empty { color: var(--dg-line); font-style: italic; }
.row { margin-bottom: 7px; }
.rowtop { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
.arrow { color: var(--dg-line); }
.id { color: #f59e0b; font-size: 0.58rem; white-space: nowrap; }
.sub { color: var(--dg-muted); padding-left: 2px; }
.sub input {
  background: var(--w-input); border: 1px solid var(--w-border); border-radius: 3px;
  color: var(--w-fg); font-family: inherit; font-size: inherit; width: 6.5rem; padding: 0 4px;
}
.portal {
  background: none; border: 1px solid var(--w-border); border-radius: 4px; color: var(--dg-muted);
  font-family: inherit; font-size: 0.6rem; padding: 1px 6px; cursor: pointer; font-weight: 400;
}
.portal:hover { color: #f59e0b; border-color: #f59e0b; }
.chip {
  margin-left: 6px; padding: 0 5px; border-radius: 3px; font-size: 0.55rem;
  color: #f59e0b; border: 1px solid var(--w-amber-bd); background: var(--w-amber-bg);
}
.x { color: var(--dg-muted); background: none; border: 0; cursor: pointer; padding: 0 2px; line-height: 1; }
.x:hover { color: #f59e0b; }
button.go {
  background: #3b82f6; color: #fff; border: 0; border-radius: 5px;
  padding: 2px 8px; font-family: inherit; font-size: 0.6rem; font-weight: 600; cursor: pointer;
}
button.go:hover { filter: brightness(1.12); }
button.ghost {
  background: none; color: var(--dg-muted); border: 1px solid var(--w-border); border-radius: 5px;
  padding: 1px 8px; font-family: inherit; font-size: 0.56rem; cursor: pointer;
}
.planout {
  grid-column: 1 / -1; position: relative; z-index: 1;
  min-height: 1.05rem; margin-top: -1.25rem;
  display: flex; flex-wrap: wrap; align-items: baseline; gap: 0 0.9rem;
  padding: 3px 10px; border-radius: 6px;
  border: 1px solid transparent;               /* reserved, invisible until it has something to say */
  transition: box-shadow .25s;
}
.planout.filled { border-color: rgba(128,128,128,0.28); background: var(--w-soft); }
.planout.flash { box-shadow: 0 0 0 2px #3b82f6; }
.planlab { color: var(--dg-muted); }
.planempty { color: var(--dg-line); font-style: italic; }
.pitem b { font-size: 0.8rem; }
.pitem.create, .pitem.update { color: #3b82f6; }
.pitem.delete { color: #f59e0b; }
.pitem.skip { color: var(--dg-muted); }
.pitem.noidea { color: #f59e0b; }
.log { color: var(--dg-fg); min-height: 1em; text-align: center; font-size: 0.52rem; line-height: 1.35; word-break: break-word; }
</style>
