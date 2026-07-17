# Empire V2 migration plan

A step-by-step path from the current V1 codebase to the layered V2 architecture, built one working piece at a time. The rule for every milestone: **the game must still run at the end of it.** We never leave things half-broken between sessions.

Keep your current V1 files untouched and working in a separate folder or branch until the final swap-in step. We build V2 files alongside, not on top of, V1.

---

## Milestone 1 — `resources.py` (data only, no logic)

**Goal:** Define what resources exist, as data, in one place.

**Tasks:**
- Create `resources.py` with a dictionary of resource definitions — name and any static properties (e.g. category: `basic` vs `luxury`, if that distinction matters later).
- No classes yet, no logic. Just the registry.

**Verify:** You can `import resources` and print the dictionary. That's it — nothing to test beyond "it loads."

**Why first:** Every other file will eventually read from this registry instead of hardcoding resource names.

---

## Milestone 2 — `economy.py` (the pool + core mechanics)

**Goal:** Rebuild `Economy` to be resource-agnostic, and give it the methods that gatekeep every transaction.

**Tasks:**
- `Economy.__init__` builds its internal dict from `resources.py`'s registry instead of a fixed constructor signature.
- Add methods: `add(resource, amount)`, `spend(resource, amount)`, `can_afford(costs_dict)`, `pay(costs_dict)`, `apply_upkeep(costs_dict)`.
- Write a small standalone test script (just a few lines in a scratch file, not part of the game yet) that creates an `Economy`, adds gold, tries to pay a multi-resource cost, and prints the result.

**Verify:** The test script runs and behaves correctly — affordable payments succeed, unaffordable ones are rejected without crashing.

**Why second:** Population, buildings, and army all depend on this. Nothing above should be built until this is solid.

---

## Milestone 3 — `population.py` (new file)

**Goal:** Turn population from a loose `int` into a real pool.

**Tasks:**
- `Population` class: `total`, `housed_capacity`, `committed_to_army`, `committed_to_jobs` (or similar breakdown — decide the exact fields together when we get here).
- Methods for growth, and for checking how many people are "available" to recruit or assign to jobs.

**Verify:** Standalone test — create a `Population`, grow it, commit some to army, confirm "available" shrinks correctly.

---

## Milestone 4 — `buildings.py` (registry + upgraded class)

**Goal:** Split building *definitions* from the `Buildings` class, and add the missing fields.

**Tasks:**
- Add a `BUILDING_TYPES` registry (dictionary of definitions: cost, upkeep, category, effect).
- Add `upkeep` and `category` fields to the `Buildings` class itself.
- Buildings now call `economy.pay()` to be constructed, instead of the game loop doing resource math directly.

**Verify:** Standalone test — build a building from the registry, confirm cost is deducted correctly via `Economy`, confirm upkeep is tracked.

---

## Milestone 5 — `army.py` (richer unit types, pool-based army)

**Goal:** Extend `UnitType` with the fields V2 needs, and make `Army` handle any unit type generically instead of a fixed 3-key dict.

**Tasks:**
- `UnitType` gains: `recruit_cost` (resources), `population_cost`, `recruit_time`, `upkeep`.
- `Army` becomes a generic pool keyed by whatever unit types exist, not hardcoded to Archer/Infantry/Cavalry.
- Recruiting now costs population (via `population.py`) and resources (via `economy.py`) together.

**Verify:** Standalone test — recruit a unit, confirm population and resources both deduct correctly, confirm upkeep is queryable.

---

## Milestone 6 — Wire the four together (still no `empire.py` yet)

**Goal:** Prove the systems talk to each other correctly before touching the game loop.

**Tasks:**
- One small test script: create economy + population + buildings + army, run a few fake "turns," apply upkeep across buildings and army in one call, confirm shortfalls behave sensibly.

**Verify:** A few turns run cleanly with realistic numbers — this is the real integration test, so take your time here.

---

## Milestone 7 — Rebuild `empire.py` (thin orchestration only)

**Goal:** Replace the old main loop with one that only calls into the systems above — no resource math, no building logic, no combat math directly in the loop.

**Tasks:**
- Turn loop: get player input → route to the right system's method → apply upkeep → check shortfall consequences → show status → next turn.
- Save/load updated to serialize the new class instances instead of loose variables.

**Verify:** Full playthrough — build, recruit, survive several turns, save, reload, confirm state matches.

---

## Milestone 8 — `territory.py` adaptation

**Goal:** Update territory/conquest logic to use the new `Army` and `Economy` APIs instead of the old direct dict access.

**Tasks:**
- Replace repeated per-territory `elif` blocks with a single `attempt_conquest(territory)` function (the refactor you'd already identified).

**Verify:** Conquest still works for all territories through the one function.

---

## Milestone 9 — `trade.py` (new system, once the above is stable)

**Goal:** Add buy/sell mechanics as a system that reads/writes to `Economy` but owns its own state (prices, maybe a simple market).

**Tasks:**
- Start minimal: fixed exchange rates, one or two tradeable resources.
- Expand later toward dynamic prices or a rival trader reacting to supply/demand.

---

## Milestone 10 — `progression.py` (ages/tiers)

**Goal:** Add a tier/age system that gates which buildings and units are unlocked.

**Tasks:**
- Add `tier` fields to building/unit definitions (already anticipated in the registries from Milestones 4–5).
- `progression.py` just filters registries by current age — no new branching logic elsewhere.

---

## Working rhythm

- One milestone per session (or split further if a milestone still feels big once we're in it).
- Every milestone ends with something you can run and see work, even if it's just a scratch test script.
- Old V1 code stays untouched and playable until Milestone 7 replaces it — so you're never without a working game while we rebuild underneath it.
