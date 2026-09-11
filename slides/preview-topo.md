---
theme: default
colorSchema: both
highlighter: shiki
mdc: true
lineNumbers: false
title: Topo sort — visual prototypes
---

# Prototype — the walk, drawn

<div class="mt-8 text-xl opacity-80">

Candidate for the slot between <code>II_11b</code> and <code>II_12</code>.
Nothing here is wired into the real deck.

</div>

<div class="mt-10 text-lg opacity-60 font-mono">

2 — the walk, with the fork built in<br>
3 — start anywhere, same answer<br>
4 — what the flat list throws away (parallelism)

</div>

---
clicks: 12
---

# Arrows in, order out

<svg viewBox="0 0 900 140" class="w-full block" style="max-width:none">
  <defs>
    <marker id="warr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" class="dglnf"/>
    </marker>
  </defs>

  <rect x="40"  y="50"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="270" y="50"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="6"   width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="730" y="6"   width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="94"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>

  <rect v-motion :initial="{opacity:0}" :click-5="{opacity:1}"  x="40"  y="50"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-6="{opacity:1}"  x="270" y="50"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-7="{opacity:1}"  x="500" y="6"   width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-8="{opacity:1}"  x="730" y="6"   width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-11="{opacity:1}" x="500" y="94"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>

  <line x1="266" y1="70"  x2="196" y2="70" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="496" y1="26"  x2="426" y2="56" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="726" y1="26"  x2="656" y2="26" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>
  <line x1="496" y1="114" x2="426" y2="84" class="dgln" stroke-width="2.5" marker-end="url(#warr)"/>

  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}"  x="40"  y="50"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}"  x="270" y="50"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}"  x="500" y="6"   width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-1="{opacity:1}"  x="730" y="6"   width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-9="{opacity:1}"  x="500" y="94"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>

  <text v-motion :initial="{opacity:0}" :click-10="{opacity:1}" x="345" y="40" text-anchor="middle" class="dgbb" style="font-size:13px;font-style:italic">already visited — skip</text>

  <text x="115" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">rg</text>
  <text x="345" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">storage</text>
  <text x="575" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">files</text>
  <text x="805" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">hello</text>
  <text x="575" y="120" text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">cdn</text>
</svg>

<div class="grid grid-cols-[1.5fr_1fr] gap-10 mt-1">

<div>
<div class="text-xs opacity-55 mb-2">the walk <span class="opacity-70">— nothing is written down on the way in</span></div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-26}" :click-1="{opacity:1,x:0}">visit(<b>hello</b>)<span class="opacity-50"> — needs files</span></div>
<div class="pl-4" v-motion :initial="{opacity:0,x:-26}" :click-2="{opacity:1,x:0}">visit(<b>files</b>)<span class="opacity-50"> — needs storage</span></div>
<div class="pl-8" v-motion :initial="{opacity:0,x:-26}" :click-3="{opacity:1,x:0}">visit(<b>storage</b>)<span class="opacity-50"> — needs rg</span></div>
<div class="pl-12" v-motion :initial="{opacity:0,x:-26}" :click-4="{opacity:1,x:0}">visit(<b>rg</b>)<span class="opacity-50"> — no arrows</span></div>
<div class="h-3"></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-9="{opacity:1,x:0}">visit(<b>cdn</b>)<span class="opacity-50"> — needs storage too</span></div>
<div class="pl-4 dgbb-t" v-motion :initial="{opacity:0,x:-26}" :click-10="{opacity:1,x:0}">visit(<b>storage</b>) → <b>in done, return</b></div>
</div>
</div>

<div>
<div class="text-xs opacity-55 mb-2">order <span class="opacity-70">— written on the way back out</span></div>
<div class="font-mono text-sm space-y-1">
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-5="{opacity:1,x:0}"><b>rg</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-6="{opacity:1,x:0}"><b>storage</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-7="{opacity:1,x:0}"><b>files</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-8="{opacity:1,x:0}"><b>hello</b></div>
<div class="dgab-t" v-motion :initial="{opacity:0,x:-300}" :click-11="{opacity:1,x:0}"><b>cdn</b></div>
</div>
</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-12="{opacity:1,y:0}" class="mt-2 text-lg">

A name is written down only once everything it points at already is. <b>That's the whole sort.</b>

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
.dgbb-t { color: var(--dg-blue-bright); }
</style>

---
clicks: 3
layout: center
---

# Start anywhere

<div class="text-base opacity-60 mt-6 mb-4 grid grid-cols-[9rem_1fr_1.5rem_1fr] gap-x-4">
  <div></div><div>the order in the file</div><div></div><div>the order it derives</div>
</div>

<div class="font-mono text-lg grid grid-cols-[9rem_1fr_1.5rem_1fr] gap-x-4 gap-y-5 items-baseline">

<div class="text-sm opacity-50" v-motion :initial="{opacity:0}" :click-1="{opacity:1}">file order</div>
<div v-motion :initial="{opacity:0,x:-24}" :click-1="{opacity:1,x:0}">rg · storage · files · hello</div>
<div class="opacity-40" v-motion :initial="{opacity:0}" :click-1="{opacity:1}">→</div>
<div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-24}" :click-1="{opacity:1,x:0}">rg · storage · files · hello</div>

<div class="text-sm opacity-50" v-motion :initial="{opacity:0}" :click-2="{opacity:1}">the tidied file</div>
<div v-motion :initial="{opacity:0,x:-24}" :click-2="{opacity:1,x:0}">hello · rg · storage · files</div>
<div class="opacity-40" v-motion :initial="{opacity:0}" :click-2="{opacity:1}">→</div>
<div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-24}" :click-2="{opacity:1,x:0}">rg · storage · files · hello</div>

<div class="text-sm opacity-50" v-motion :initial="{opacity:0}" :click-3="{opacity:1}">a Go map</div>
<div v-motion :initial="{opacity:0,x:-24}" :click-3="{opacity:1,x:0}">storage · hello · rg · files</div>
<div class="opacity-40" v-motion :initial="{opacity:0}" :click-3="{opacity:1}">→</div>
<div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-24}" :click-3="{opacity:1,x:0}">rg · storage · files · hello</div>

</div>

<div class="mt-12 text-xl">

The order is <b>derived</b>, so nothing can scramble it.

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
</style>

---
clicks: 4
---

# What the list throws away

<div class="mt-6">

<div class="text-base opacity-60 mb-2">what <code>ordered()</code> hands back — one name after another</div>

<div class="font-mono text-xl flex items-center gap-3" v-motion :initial="{opacity:0}" :click-1="{opacity:1}">
  <span class="dgab-t font-bold">rg</span><span class="opacity-30">→</span>
  <span class="dgab-t font-bold">storage</span><span class="opacity-30">→</span>
  <span class="dgab-t font-bold">files</span><span class="opacity-30">→</span>
  <span class="dgab-t font-bold">hello</span><span class="opacity-30">→</span>
  <span class="dgab-t font-bold">cdn</span>
</div>

</div>

<div class="mt-7" v-motion :initial="{opacity:0}" :click-2="{opacity:1}">

<div class="text-base opacity-60 mb-2">what the arrows actually allow</div>

<div class="font-mono text-xl space-y-1">
  <div><span class="opacity-40 text-sm mr-4">wave 1</span><span class="dgab-t font-bold">rg</span></div>
  <div><span class="opacity-40 text-sm mr-4">wave 2</span><span class="dgab-t font-bold">storage</span></div>
  <div><span class="opacity-40 text-sm mr-4">wave 3</span><span class="dgab-t font-bold">files</span><span class="mx-3 opacity-50 text-base">and</span><span class="dgab-t font-bold">cdn</span><span class="ml-4 text-base opacity-60">— at the same time</span></div>
  <div><span class="opacity-40 text-sm mr-4">wave 4</span><span class="dgab-t font-bold">hello</span></div>
</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-3="{opacity:1,y:0}" class="mt-6 text-lg">

<span class="font-mono">files</span> and <span class="font-mono">cdn</span> share no arrow.
<b>A flat list cannot say "these two at once."</b>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-4="{opacity:1,y:0}" class="mt-2 text-lg opacity-80">

Peel leaves instead and you get waves. <b>That is the go-fast plan every real engine runs.</b>

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
</style>

---
clicks: 6
---

# Counters in, waves out

<svg viewBox="0 0 900 148" class="w-full block" style="max-width:none">
  <defs>
    <marker id="karr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" class="dglnf"/>
    </marker>
  </defs>

  <rect x="40"  y="50" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="270" y="50" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="6"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="730" y="6"  width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>
  <rect x="500" y="94" width="150" height="40" rx="9" class="dgbx dgbd" stroke-width="1.5"/>

  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}" x="40"  y="50" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="270" y="50" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="500" y="6"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-5="{opacity:1}" x="730" y="6"  width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="500" y="94" width="150" height="40" rx="9" class="dgam" stroke="#f59e0b" stroke-width="2.5"/>

  <line x1="266" y1="70"  x2="196" y2="70" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="496" y1="26"  x2="426" y2="56" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="726" y1="26"  x2="656" y2="26" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>
  <line x1="496" y1="114" x2="426" y2="84" class="dgln" stroke-width="2.5" marker-end="url(#karr)"/>

  <rect v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-2="{opacity:0}" x="40"  y="50" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-2="{opacity:1}" :click-3="{opacity:0}" x="270" y="50" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}" x="500" y="6"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}" x="500" y="94" width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>
  <rect v-motion :initial="{opacity:0}" :click-4="{opacity:1}" :click-5="{opacity:0}" x="730" y="6"  width="150" height="40" rx="9" fill="none" stroke="#3b82f6" stroke-width="3.5"/>

  <g v-motion :initial="{opacity:0}" :click-1="{opacity:1}">
    <circle cx="180" cy="58"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="410" cy="58"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="640" cy="14"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="870" cy="14"  r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
    <circle cx="640" cy="102" r="12" class="dgbx2 dgbd" stroke-width="1.5"/>
  </g>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" x="180" cy="0" y="63" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-2="{opacity:0}" x="410" y="63" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-2="{opacity:1}" x="410" y="63" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-3="{opacity:0}" x="640" y="19" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="640" y="19" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-3="{opacity:0}" x="640" y="107" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-3="{opacity:1}" x="640" y="107" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text v-motion :initial="{opacity:0}" :click-1="{opacity:1}" :click-4="{opacity:0}" x="870" y="19" text-anchor="middle" class="dgmu" style="font-size:14px;font-weight:700">1</text>
  <text v-motion :initial="{opacity:0}" :click-4="{opacity:1}" x="870" y="19" text-anchor="middle" class="dgbb" style="font-size:14px;font-weight:700">0</text>

  <text x="115" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">rg</text>
  <text x="345" y="76"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">storage</text>
  <text x="575" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">files</text>
  <text x="805" y="32"  text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">hello</text>
  <text x="575" y="120" text-anchor="middle" class="dgfg" style="font-size:18px;font-weight:600">cdn</text>
</svg>

<div class="grid grid-cols-[1fr_1fr] gap-10 mt-1">

<div>
<div class="text-xs opacity-55 mb-2" v-motion :initial="{opacity:0}" :click-1="{opacity:0.55}">the badge = arrows still unmet · <span class="dgbb-t font-bold">0</span> = ready</div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-26}" :click-2="{opacity:1,x:0}">take <b>rg</b> <span class="opacity-50">→ storage 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-3="{opacity:1,x:0}">take <b>storage</b> <span class="opacity-50">→ files 1→0, cdn 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-4="{opacity:1,x:0}">take <b>files</b>, <b>cdn</b> <span class="opacity-50">→ hello 1→0</span></div>
<div v-motion :initial="{opacity:0,x:-26}" :click-5="{opacity:1,x:0}">take <b>hello</b> <span class="opacity-50">→ nothing left</span></div>
</div>
</div>

<div>
<div class="text-xs opacity-55 mb-2">waves</div>
<div class="font-mono text-sm space-y-1">
<div v-motion :initial="{opacity:0,x:-260}" :click-2="{opacity:1,x:0}"><span class="opacity-40 mr-3">1</span><span class="dgab-t font-bold">rg</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-3="{opacity:1,x:0}"><span class="opacity-40 mr-3">2</span><span class="dgab-t font-bold">storage</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-4="{opacity:1,x:0}"><span class="opacity-40 mr-3">3</span><span class="dgab-t font-bold">files</span><span class="opacity-40 mx-2">+</span><span class="dgab-t font-bold">cdn</span></div>
<div v-motion :initial="{opacity:0,x:-260}" :click-5="{opacity:1,x:0}"><span class="opacity-40 mr-3">4</span><span class="dgab-t font-bold">hello</span></div>
</div>
</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-6="{opacity:1,y:0}" class="mt-2 text-lg">

No call stack. <b>A count per node, and everything at zero goes at once.</b>

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
.dgbb-t { color: var(--dg-blue-bright); }
</style>

---
clicks: 7
zoom: 0.92
---

# A — the loop, and its three variables

<div class="grid grid-cols-[1.15fr_1fr] gap-8 mt-2">

<div>

```py {1-2|4-5|7-15|7-15|7-15|7-15}{lines:true}
unmet = {k: len(r["dependsOn"]) for k, r in res.items()}
waiting_on = invert(res)          # rg -> [storage], storage -> [files, cdn]

ready = [k for k in unmet if unmet[k] == 0]
out = []

while ready:
    out.append(ready)             # one wave — these go at once
    nxt = []
    for k in ready:
        for d in waiting_on[k]:
            unmet[d] -= 1         # one arrow met
            if unmet[d] == 0:
                nxt.append(d)     # last arrow met — it's ready
    ready = nxt
```

</div>

<div class="font-mono text-sm">

<div class="text-xs opacity-55 mb-1">unmet <span class="opacity-70">— arrows still owed</span></div>
<div class="space-y-0.5">
  <div><span class="inline-block w-20 opacity-70">rg</span><span class="dgbb-t font-bold">0</span></div>
  <div><span class="inline-block w-20 opacity-70">storage</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-3="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-3="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">files</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-4="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">cdn</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-4="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}">0</span></span></div>
  <div><span class="inline-block w-20 opacity-70">hello</span><span class="inline-grid align-baseline"><span class="col-start-1 row-start-1" v-motion :initial="{opacity:1}" :click-5="{opacity:0}">1</span><span class="col-start-1 row-start-1 dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-5="{opacity:1}">0</span></span></div>
</div>

<div class="text-xs opacity-55 mt-5 mb-1">ready <span class="opacity-70">— everything at zero</span></div>
<div class="relative h-6">
  <div class="absolute opacity-40" v-motion :initial="{opacity:0.4}" :click-2="{opacity:0}">[]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-2="{opacity:1}" :click-3="{opacity:0}">[rg]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-3="{opacity:1}" :click-4="{opacity:0}">[storage]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-4="{opacity:1}" :click-5="{opacity:0}">[files, cdn]</div>
  <div class="absolute dgbb-t font-bold" v-motion :initial="{opacity:0}" :click-5="{opacity:1}" :click-6="{opacity:0}">[hello]</div>
  <div class="absolute opacity-40" v-motion :initial="{opacity:0}" :click-6="{opacity:1}">[] <span class="ml-2 text-xs">— loop ends</span></div>
</div>

<div class="text-xs opacity-55 mt-4 mb-1">out <span class="opacity-70">— one entry per wave</span></div>
<div class="space-y-0.5">
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-3="{opacity:1,x:0}">[rg]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-4="{opacity:1,x:0}">[storage]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-5="{opacity:1,x:0}">[files, cdn]</div>
  <div class="dgab-t font-bold" v-motion :initial="{opacity:0,x:-40}" :click-6="{opacity:1,x:0}">[hello]</div>
</div>

</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-7="{opacity:1,y:0}" class="mt-4 text-lg">

Three variables, and the middle one is the answer. <b><span class="font-mono">ready</span> is a wave.</b>

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
.dgbb-t { color: var(--dg-blue-bright); }
</style>

---
clicks: 6
zoom: 0.9
---

# B — one row per trip round the loop

<div class="mt-4 font-mono text-sm">

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4 text-xs opacity-55 mb-2">
  <div>iter</div><div>unmet</div><div>ready</div><div>out += </div>
</div>

<div class="space-y-2">

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4" v-motion :initial="{opacity:0}" :click-1="{opacity:1}">
  <div class="opacity-40">—</div><div><span class="opacity-50">rg</span> <b class="dgbb-t">0</b> · <span class="opacity-50">storage</span> 1 · <span class="opacity-50">files</span> 1 · <span class="opacity-50">cdn</span> 1 · <span class="opacity-50">hello</span> 1</div><div><span class="dgbb-t font-bold">[rg]</span></div><div><span class="opacity-40">—</span></div>
</div>

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4" v-motion :initial="{opacity:0}" :click-2="{opacity:1}">
  <div class="opacity-40">1</div><div><span class="opacity-25">rg —</span> · <span class="opacity-50">storage</span> <b class="dgbb-t">0</b> · <span class="opacity-50">files</span> 1 · <span class="opacity-50">cdn</span> 1 · <span class="opacity-50">hello</span> 1</div><div><span class="dgbb-t font-bold">[storage]</span></div><div><span class="dgab-t font-bold">[rg]</span></div>
</div>

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4" v-motion :initial="{opacity:0}" :click-3="{opacity:1}">
  <div class="opacity-40">2</div><div><span class="opacity-25">rg — · storage —</span> · <span class="opacity-50">files</span> <b class="dgbb-t">0</b> · <span class="opacity-50">cdn</span> <b class="dgbb-t">0</b> · <span class="opacity-50">hello</span> 1</div><div><span class="dgbb-t font-bold">[files, cdn]</span></div><div><span class="dgab-t font-bold">[storage]</span></div>
</div>

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4" v-motion :initial="{opacity:0}" :click-4="{opacity:1}">
  <div class="opacity-40">3</div><div><span class="opacity-25">rg — · storage — · files — · cdn —</span> · <span class="opacity-50">hello</span> <b class="dgbb-t">0</b></div><div><span class="dgbb-t font-bold">[hello]</span></div><div><span class="dgab-t font-bold">[files, cdn]</span></div>
</div>

<div class="grid grid-cols-[3rem_1fr_10rem_10rem] gap-x-4" v-motion :initial="{opacity:0}" :click-5="{opacity:1}">
  <div class="opacity-40">4</div><div><span class="opacity-25">rg — · storage — · files — · cdn — · hello —</span></div><div><span class="opacity-40">[]</span></div><div><span class="dgab-t font-bold">[hello]</span></div>
</div>
</div>

</div>

<div v-motion :initial="{opacity:0,y:12}" :click-6="{opacity:1,y:0}" class="mt-2 text-lg">

Four trips, four waves. <b>The whole algorithm is one column emptying into the next.</b>

</div>

<style>
.dgab-t { color: var(--dg-amber-bright); }
.dgbb-t { color: var(--dg-blue-bright); }
</style>
