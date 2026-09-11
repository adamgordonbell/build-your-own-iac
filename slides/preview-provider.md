---
theme: default
colorSchema: both
highlighter: shiki
mdc: true
lineNumbers: false
title: Where it gets hairy — provider side-by-side
---

# Prototype — "and this is where it gets hairy"

<div class="mt-8 text-xl opacity-80">

A candidate slide (or two) for late in Act II / early Act III:
<br>the moment we admit the real provider is not 165 lines.

</div>

<div class="mt-10 text-lg opacity-60">

Source: <code>pulumi/pulumi-azure-native</code> ·
<code>provider/pkg/resources/customresources/</code>
<br>Nothing here is wired into the real deck.

</div>

<div class="mt-10 text-base opacity-60 font-mono">
2 — the promise, and the one that breaks it (KeyVault AccessPolicy)<br>
3 — the 15 the generator gave up on
</div>

---

# Our whole talk rests on one sentence

<div class="grid grid-cols-2 gap-10 mt-6">

<div>

<div class="text-lg dgbb-t font-semibold mb-3">Our engine — every resource, one shape</div>

```python
# create / update
call("PUT",    url_for(res), res["properties"])
# read
call("GET",    url_for(res))
# destroy
call("DELETE", url_for(res))
```

<div class="mt-5 text-lg opacity-80">
Every Azure resource is a <strong>URL</strong> you
<code>PUT</code> / <code>GET</code> / <code>DELETE</code>.
<br>That uniformity <em>is</em> the engine.
</div>

</div>

<div>

<div class="text-lg dgab-t font-semibold mb-2">azure-native · KeyVault <code>AccessPolicy</code></div>

<div class="text-base opacity-90 leading-snug">

<div v-click class="mb-2">⬦ It <strong>isn't a resource.</strong> Azure has no PUT/GET/DELETE for one policy — it's a slice of the vault.</div>

<div v-click class="mb-2">⬦ <strong>read</strong> = GET the entire vault, loop every policy hunting for your <code>objectId</code>.</div>

<div v-click class="mb-2">⬦ <strong>create vs. update?</strong> Azure only offers "Replace." So the provider reads first and <em>fakes the distinction itself.</em></div>

<div v-click class="mb-2">⬦ <strong>delete</strong> = a "Remove" op on the parent vault.</div>

<div v-click class="mb-2">⬦ permissions: 4 categories, hand-marshalled <strong>both directions</strong> (~70 lines).</div>

<div v-click class="mb-2">⬦ the ID shape changed once — and can <strong>never</strong> change again, or every import breaks. It carries both formats forever.</div>

</div>
</div>

</div>

<div v-click class="mt-3 text-center text-xl dgab-t font-semibold">
~340 lines. For a thing with three fields.
</div>

---

# Not one exception — a whole drawer of them

<div class="text-lg opacity-80 mt-4 mb-6">
The resources the code generator <strong>couldn't</strong> generate —
each one a real edge case someone hit in production:
</div>

<div class="grid grid-cols-3 gap-x-8 gap-y-1 text-base font-mono opacity-90">
<div>KeyVault</div>
<div>KeyVault AccessPolicy</div>
<div>RoleAssignment</div>
<div>StorageAccount blob</div>
<div>StorageAccount StaticWebsite</div>
<div>BlobContainer LegalHold</div>
<div>ServiceBus DefaultRule</div>
<div>RecoveryServices</div>
<div>Postgres Config</div>
<div>Portal Dashboard</div>
<div>PIM (eligibility)</div>
<div>WebApp</div>
<div>TagScope</div>
<div>SecurityInsights SourceControl</div>
<div class="opacity-50">…and more</div>
</div>

<div v-click class="mt-8 text-xl">
<span class="dgbb-t font-semibold">Our 165 lines</span> assumed every resource behaves.
<br><span class="dgab-t font-semibold">These 15</span> are the price of assuming it doesn't.
</div>

<div v-click class="mt-4 text-lg opacity-70">
That gap — clean model vs. the drawer of exceptions — <em>is</em> what you're paying a provider for.
</div>
