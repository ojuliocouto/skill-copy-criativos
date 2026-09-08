# copy-criativos

A Claude Code skill that writes the **copy for short-form video creatives** (paid ads and organic
pieces for Reels, Shorts, TikTok, Stories and feed) directly in the annotated script format that a
video assembly pipeline can consume. The copy leaves the copywriter's hands ready to become a
finished piece, with no editing rework.

It was built alongside a deterministic 9:16 assembly engine with measured gates, but the ideas
travel and the skill is self-contained: every visual rule of the edit has a copy consequence, and
this skill makes those consequences explicit and testable. **You do not need that pipeline to use
this skill.**

The skill and its documentation are written in Brazilian Portuguese, because that is the language
of the copy it produces. This README is the only English document in the repository.

## What it is

- A **method** (`references/metodo-de-copy.md`): three layers (angle, invisible structure, format),
  an avatar diagnosis by temperature and awareness level, the anatomy of an ad broken into block
  roles, the valid sequences per temperature, and a structure checklist that runs before the gate.
- A **process** for writing one creative concept at a time: brief, a block plan run through a
  planner *before* any writing, a block-by-block draft approved in a table, three hooks with named
  tactics, then billboard words, letterings, CTA and asset directions.
- A **contract**: the copy is delivered as a package of 8 files per concept, and the central one
  (`roteiro.txt`) is a line format an editor or a pipeline parses directly.
- A **gate** (`scripts/gate_copy.py`): a Python checker that reads the package and rejects it block
  by block when the copy would break on screen (a block too short for its insert, a lettering word
  the voice never says, a brand name in the first 3 seconds, a CTA that does not match the mode).
- A **planner** (`scripts/planejar_blocos.py`): tells you how many words fit in each block and
  whether insert density per window closes, before you spend any writing on a shape that cannot
  work.
- **Two reference packages**: a clean one that passes with a single declared warning, and a real
  one rebuilt from an approved ad that carries thirteen acknowledged warnings.

## What it is NOT

- It does not edit video, pick asset files or render anything.
- It does not choose the campaign concept or the persuasion angle. That is a strategy decision made
  with the client, using the angle library shipped in `references/angulos-e-estrutura.md`.
- It does not invent proof, numbers, client names or demos. Anything not in the offer preset does
  not exist.
- It is opinionated for Brazilian Portuguese spoken copy. Rules like "no em dashes" and "numbers
  spelled out in speech, digits in letterings" are deliberate.

## Onboarding: what you need before your first run

1. **Claude Code**, with this repository cloned into `~/.claude/skills/copy-criativos/`.
2. **Python 3.9 or newer.** The `/usr/bin/python3` that ships with macOS is fine.
3. **`pyyaml` is optional.** Without it the gate runs on thresholds and a hook-tactic catalogue
   embedded in the code. Install it only if you have an external pipeline whose YAML config you
   want to point at with `--gates` and `--taticas`:
   ```bash
   python3 -m pip install --user pyyaml
   ```
4. **An offer preset**: the document that authorises every number, proof, price and client name the
   copy is allowed to state. If your client does not have one, build it with them using
   `references/modelo-preset-oferta.md`. A filled-in fictional example is in
   `references/preset-oferta-exemplo.md`.
5. **A brief** with four mandatory fields: avatar (who it speaks to), promise (one sentence), mode
   (`pago` or `organico`) and channel (`reels`, `stories`, `feed_4x5`, `feed_1x1`, `tiktok`,
   `shorts`). For paid, also the campaign type (`frio`, `captacao`, `perpetuo_frio`, `carrinho`,
   `lote`, `remarketing`), which decides whether the CTA may carry scarcity and price.
6. **The assets already handed over** for the concept. If the brief arrives as a Google Doc with
   comments, read every comment first: each link inside a comment is one asset for that block.

Nothing else. No other skill, no external repository, no credentials.

### Verify the install

```bash
cd ~/.claude/skills/copy-criativos
python3 scripts/gate_copy.py exemplos/agenda-cheia
```

You should see the per-block summary and exactly one warning (58% insert density in the closing
window), with no rejections. If you get an import error, fix that before writing anything: a broken
gate means delivering without proof.

## Installation

```bash
git clone https://github.com/ojuliocouto/skill-copy-criativos.git ~/.claude/skills/copy-criativos
```

Claude Code picks the skill up from `~/.claude/skills/`. Trigger it with `/copy-criativos` or by
asking for "copy de criativo", "roteiro de anúncio em vídeo", "hooks" or "matriz de criativos".

## How it works

0. **Plan the blocks first.** `planejar_blocos.py` takes the intended shape of the piece (`I`
   insert, `L` plate lettering, `LC` column or stamp, `A` presenter alone, `P` bridge, `C` CTA;
   the block before `C` must be `P` or `I`, the two that can carry the bridge line) and
   returns min and max words per block, a timeline and insert density per window. Two of the
   constraints (density per window, and the ceiling on two neighbouring insert-free blocks) depend
   on the accumulated timeline and cannot be worked out on paper.
1. **Onboarding check.** The skill refuses to write without avatar, promise, mode, channel and, for
   paid, campaign type. It also expects an approved angle, an offer preset, and the asset list.
2. **Role sequence, then the block table.** Before any writing, the piece is laid out as a sequence
   of block roles (`H` hook, `D` pain, `P` proof with insert, `M` mechanism, `I` identification, `O`
   offer, `T` bridge, `C` CTA), declared in `conceito.md`. Cold traffic runs `H D P M T C` or
   `H P I M T C`; warm runs `H P O T C`. Only then is the script drafted as a table (block, role,
   speech, word count, final duration, required minimum, insert, LEAD, KEY, form) and approved block
   by block before any polishing.
3. **Three hooks.** Each with a named tactic from the 29 tactics grouped by cluster. Cold traffic
   only gets pattern-interruption or curiosity clusters; promotional hooks are allowed only for
   cart or batch campaigns. At least one of the three is a question or a paradox the viewer has to
   resolve. One of the three is "raw" (voice-note style, no lettering).
4. **Billboards, letterings, CTA, assets, matrix.** Each in its own file, each anchored to the
   exact words in the speech.
5. **Gate.** `gate_copy.py` runs on the package and prints rejections (exit 1) and warnings
   (exit 0). Nothing is called "ready" without the gate output pasted into the delivery.
6. **Handoff.** Whoever edits the video reads `roteiro.txt` directly.

### The screen rules the copy has to know

Speech is measured at 2.9 words per second of natural delivery and the piece is sped up 1.45x, so
every threshold converts into words. **Those 2.9 words per second were measured on one specific
presenter's voice.** Measure your own (count the words in a minute of natural recorded speech) and
set `palavras_por_segundo` in `conceito.md`; every minimum below recomputes from it.

| rule | number | why |
|---|---|---|
| block with an insert | 15 words or more (3.5s final) | b-roll runs at 1.0x and needs time on screen |
| block with a plate lettering | 12 words or more (2.8s) | reading time |
| block with a column or stamp lettering | 15 words or more (3.5s) | vertical text is slower to read |
| each KEY word past the second | +0.25s, meaning +1 word | reading time per extra word |
| CTA block | 13 to 21 words (3.0s to 5.0s) | closing window |
| presenter alone, no insert, no lettering | 25 words max (6.0s) | retention |
| hook | up to 14 words; problem or promise in the first 4 words | first 1.2s of speech |
| brand, product, event name | never in the first 3 words; within the first 12 only with the event logo anchored to the speech | no brand before the promise |
| KEY (big lettering) | up to 2 content words, every word spoken in that block | legibility and voice anchoring |
| billboard word | 2 or 3 per piece, spoken, never repeating the KEY, only where the presenter is alone | it must carry copy weight, not decorate |
| insert density | 45 to 55% of each window (3 to 15s, 15s to end) covered by an insert | retention |
| bridge before the CTA | mandatory: the block before the CTA, or the CTA's first sentence, says what the click delivers and ties it to the proof just shown | a benefit followed by "tap learn more" out of nowhere leaves the click with no object |
| hook shape | at least one of the three hooks is a question or a paradox the viewer has to resolve | an agreeable statement stops nobody |

Note that the KEY has **two different counts**: the 2-word limit counts content words only
(digits and function words do not count), while reading time counts every non-numeric word.
`SKILLS DO ZERO` is 2 for the limit and 3 for the timing, so its minimum is 3.05s.

The full list, one line per rule with its source, is in `references/regras-da-tela.md`.

### Running the gate

```bash
python3 scripts/gate_copy.py <package-dir>
```

Add `--json` for machine-readable output. Exit code 1 means at least one rejection. If you do have
an external pipeline, you can point the gate at its config (both flags optional):

```bash
python3 scripts/gate_copy.py <package-dir> --gates <config>/gates.yaml --taticas <config>/taticas_hook.yaml
```

```bash
python3 -m pytest scripts/tests -q
```

## Contents

```
SKILL.md                          trigger, glossary, prerequisites, onboarding, process, rules, handoff
references/metodo-de-copy.md      the METHOD: three layers, avatar diagnosis, block roles, valid sequences, structure checklist
references/regras-da-tela.md      one line per edit rule that changes the copy, with its source
references/formato-do-pacote.md   the 8-file package contract, field by field, plus the gate table
references/taticas-de-hook.md     29 hook tactics by cluster, each with an example
references/angulos-e-estrutura.md the 78 angles in 5 categories and the 8 invisible-structure elements
references/voz-e-anti-ia.md       spoken Brazilian Portuguese voice and the anti-AI gate
references/modelo-preset-oferta.md  blank offer-preset template
references/preset-oferta-exemplo.md a filled-in fictional preset
scripts/gate_copy.py              thin CLI wrapper
scripts/gate_copy/                the gate: readers, text normalisation, one module per rule family
scripts/planejar_blocos.py        block planner: words per block, timeline, density per window
scripts/tests/                    tests (a valid package plus one mutation per rule)
exemplos/agenda-cheia/            the clean reference package: zero rejections, one declared warning
exemplos/cinco-entregas/          a real approved ad rebuilt: zero rejections, 13 acknowledged warnings
```

### The two examples

They have different jobs. **`exemplos/agenda-cheia/`** is fictional, six blocks long, and passes
with **zero rejections and one declared warning**: copy it while you are learning the format. Its
README also compares it against a first version that the methodology owner rejected, for a generic
hook and a CTA with no bridge. **`exemplos/cinco-entregas/`** rebuilds a
**real ad that ran and was approved**, so it carries **13 acknowledged warnings** (a 40.7s runtime and
99% insert density in the body window among them): read it to understand why an approved piece can
carry warnings, and how to declare them honestly instead of hiding them.

### The package (one directory per concept)

Default output directory: `./copy/<concept>/`, relative to your working directory.

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

The repository contains no credentials, tokens, account ids or client data. Every path referenced
by `SKILL.md` lives inside the skill directory itself. The clean example is entirely fictional; the
real example uses public brand names and proof already authorised for public advertising.

## License

MIT.
