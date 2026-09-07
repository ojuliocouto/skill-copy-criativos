# copy-criativos

A Claude Code skill that writes the **copy for short-form video creatives** (paid ads and organic pieces for Reels, Shorts, TikTok, Stories and feed) directly in the annotated script format that a deterministic video pipeline consumes. The copy leaves the copywriter's hands ready to become a finished piece, with no editing rework.

It was built for the `creative-studio` pipeline (a 9:16 video assembly engine with measured gates), but the ideas travel: every visual rule of the edit has a copy consequence, and this skill makes those consequences explicit and testable.

## What it is

- A **process** for writing one creative concept at a time: brief, block-by-block draft approved in a table, three hooks with a named tactic, then billboard words, letterings, CTA and asset directions.
- A **contract**: the copy is delivered as a package of 8 files per concept, and the central one (`roteiro.txt`) is the exact line format the pipeline parses.
- A **gate** (`scripts/gate_copy.py`): a Python checker that reads the package and rejects it block by block when the copy would break on screen (a block too short for its insert, a lettering word the voice never says, a brand name in the first 3 seconds, a CTA that does not match the mode).
- A **reference example** (`exemplos/cinco-entregas/`): a real ad rebuilt into a package that passes the gate, with a README explaining every change and why.

## What it is NOT

- It does not edit video, pick asset files or render anything. That is the pipeline's job.
- It does not choose the campaign concept or the persuasion angle. That comes from a separate methodology skill (angle library plus invisible structure).
- It does not invent proof, numbers, student names or demos. Anything not in the offer preset does not exist.
- It is opinionated for Brazilian Portuguese spoken copy and for one house voice. Rules like "no em dashes" and "numbers spelled out in speech, digits in letterings" are deliberate.

## How it works

1. **Onboarding check.** The skill refuses to write without avatar, promise, mode (`pago` or `organico`), channel and, for paid, campaign type (`frio`, `captacao`, `carrinho`, `lote`, `remarketing`). It also expects an approved angle, an offer preset with authorised proof, and the list of assets already handed over.
2. **Block table first.** The script is drafted as a table (block, speech, word count, insert, LEAD, KEY) and approved block by block before any polishing.
3. **Three hooks.** Each with a named tactic from the 29 Motion tactics grouped by cluster. Cold traffic only gets pattern-interruption or curiosity clusters; promotional hooks are allowed only for cart or batch campaigns. One of the three is "raw" (voice-note style, no lettering).
4. **Billboards, letterings, CTA, assets, matrix.** Each in its own file, each anchored to the exact words in the speech.
5. **Gate.** `gate_copy.py` runs on the package and prints rejections (exit 1) and warnings (exit 0). Nothing is called "ready" without the gate output.
6. **Handoff.** The pipeline reads `roteiro.txt` directly.

### The screen rules the copy has to know

Speech is measured at 2.9 words per second of natural delivery and the piece is sped up 1.45x, so every threshold converts into words:

| rule | number | why |
|---|---|---|
| block with an insert | 15 words or more (3.5s final) | b-roll runs at 1.0x and needs time on screen |
| block with a plate lettering | 12 words or more (2.8s + 0.25s per extra word) | reading time |
| block with a column or stamp lettering | 15 words or more (3.5s) | vertical text is slower to read |
| CTA block | 13 to 21 words (3.0s to 5.0s) | closing window |
| presenter alone, no insert, no lettering | 25 words max (6.0s) | retention |
| hook | up to 14 words; problem or promise in the first 4 words | first 1.2s of speech |
| brand, product, event name | never in the first 3 words; within the first 12 only with the event logo anchored to the speech | no brand before the promise |
| KEY (big lettering) | up to 2 content words, every word spoken in that block | legibility and voice anchoring |
| billboard word | 2 or 3 per piece, spoken, never repeating the KEY, only where the presenter is alone | it must carry copy weight, not decorate |
| insert density | 45 to 55% of each window (3 to 15s, 15s to end) with an insert | retention |

The full list, one line per decision with its source, is in `references/regras-da-tela.md`.

## Installation

```bash
git clone https://github.com/ojuliocouto/skill-copy-criativos.git ~/.claude/skills/copy-criativos
```

Claude Code picks the skill up from `~/.claude/skills/`. Trigger it with `/copy-criativos` or by asking for "copy de criativo", "roteiro de anúncio em vídeo", "hooks" or "matriz de criativos".

### Prerequisites

- Claude Code.
- Python 3.9 or newer with `pyyaml` (the gate uses only the standard library plus YAML).
- Optional: the `creative-studio` pipeline at `~/creative-studio`. The gate reads `config/gates.yaml` and `config/taticas_hook.yaml` from there when present; without them it falls back to the embedded thresholds and tactic catalogue.
- An offer preset (authorised proof, numbers, deliverables) and an angle for the concept. The skill will ask for them.

### Running the gate

```bash
python3 scripts/gate_copy.py <package-dir> \
  --gates ~/creative-studio/config/gates.yaml \
  --taticas ~/creative-studio/config/taticas_hook.yaml
```

Add `--json` for machine-readable output. Exit code 1 means at least one rejection.

```bash
python3 -m pytest scripts/tests -q   # 60 tests
```

## Contents

```
SKILL.md                          trigger, onboarding, process, rules summary, handoff
references/formato-do-pacote.md   the 8-file package contract, field by field, plus the gate table
references/regras-da-tela.md      one line per edit decision that changes the copy, with its source
references/taticas-de-hook.md     29 hook tactics by cluster, each with a house-voice example
scripts/gate_copy.py              thin CLI wrapper
scripts/gate_copy/                the gate: readers, text normalisation, one module per rule family
scripts/tests/                    60 tests (a valid package plus one mutation per rule)
exemplos/cinco-entregas/          reference package rebuilt from a real ad, passes the gate
```

### The package (one directory per concept)

```
<out>/<concept>/
  conceito.md      front matter: angle, avatar, promise, mode, channel, campaign, brands
  roteiro.txt      annotated script: [insert anchor | LEAD: ... | KEY: ...] speech, one block per line
  hooks.md         3 hooks with tactic id, cluster, anchor word, one raw
  garrafais.md     2 or 3 billboard words with the anchor phrase and colour role
  letterings.md    LEAD and KEY per block, anchor word, lettering form
  cta.md           closing by mode (paid cart: action verb + real scarcity; paid cold: verb only; organic: loop, question or share)
  assets.md        origin and framing of every insert (handed over first; created only when nothing exists)
  matriz.md        the 12 pieces: 3 hooks x 2 captions x 2 formats, named {concept}_{channel}_{format}_{hook}_{caption}_v{n}
```

## Security

The repository contains no credentials, tokens, account ids or client data. The example uses public brand names and proof already authorised for public ads. Paths inside `SKILL.md` point to the local pipeline and to public skill directories only.

## License

MIT.
