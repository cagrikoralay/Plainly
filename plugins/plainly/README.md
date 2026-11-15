# Plainly

**Make AI answers plain, short, and clear — without losing the facts.**

Plainly is a Claude Code plugin. It explains, rewrites, or checks text with a small set of
plain-language rules. The rules are loosely inspired by the controlled English that aircraft
maintenance manuals use. The idea: a technician must understand an instruction on the first
read, under pressure, even if English is not their first language. That works for AI answers
too.

> Andrej Karpathy suggested asking models to write about 80% of the way to ASD-STE100 to make
> their output easier to read. Plainly packages that idea as a skill, with one extra rule on top:
> **never lose the meaning.**

## What you get

| Part | What it does |
|---|---|
| `/plainly` skill | Three modes: **explain**, **rewrite**, **check**. Two strengths: **light** (default) and **strict**. Claude also uses it on its own when you say "I don't get it" or "simplify this". |
| Output style | Turn on plain answers for the whole session with `/output-style`. |
| Checker script | `plainly_check.py` flags long sentences, passive voice, long paragraphs, semicolons, and wordy or "AI-speak" words. `--strict` also flags contractions and complex verb forms. Standard-library Python. Works in CI. |
| Lite snippet | Six lines you can paste into `CLAUDE.md`, `AGENTS.md`, ChatGPT, or Gemini. No install. |
| Skill zip | The same skill as a zip, for claude.ai and Claude Desktop. |

Tested with `claude plugin eval`, with and without the plugin. See [How it was tested](#how-it-was-tested).

## Install

In Claude Code:

```text
/plugin marketplace add cagrikoralay/Plainly
/plugin install plainly@cagrikoralay
```

To try a local copy without installing, point Claude Code at the plugin folder:

```bash
claude --plugin-dir path/to/plainly
```

For claude.ai or Claude Desktop, download the skill zip from the
[downloads folder](https://github.com/cagrikoralay/Plainly/tree/main/downloads) and upload it as
a skill.

## Use

```text
/plainly                          # explain your last answer again, plainly
/plainly explain <text>           # "I don't get this" — re-explain a dense answer
/plainly rewrite strict <text>    # turn a messy note into clear steps
/plainly check README.md          # list readability problems and fixes
```

You can also just talk: "I don't get this, explain it simply", "make this runbook clearer",
"is this PR description easy to read?"

For plain answers all the time: run `/output-style` and pick **Plainly**, or set
`"outputStyle": "plainly:Plainly"` in your Claude Code `settings.json`.

## Before and after

**Before** (a typical AI answer):

> Retrieval-augmented generation essentially leverages a vector store to semantically retrieve
> contextually relevant chunks, which are subsequently injected into the prompt, thereby
> grounding the model's output and mitigating hallucinations.

**After** (`/plainly explain`):

> **In one sentence:** RAG finds relevant parts of your documents and gives them to the model
> with your question.
>
> 1. Your documents are cut into small parts, called *chunks*.
> 2. The system finds the chunks that are closest in meaning to your question.
> 3. It adds those chunks to the prompt.
>
> **Why it helps:** The model answers from your text, so it invents fewer facts.

More examples: [skills/plainly/references/examples.md](skills/plainly/references/examples.md).

## The rules

Rule 0 is above all others: **keep the meaning.** Keep every fact, number, and condition. Keep
uncertainty as uncertainty. Add nothing.

Then come 20 short rules about words, sentences, and structure. For example: use common
words, use one term per thing, keep sentences short, and put warnings first.
Full list: [skills/plainly/references/rules.md](skills/plainly/references/rules.md).

## How Plainly compares to ASD-STE100

ASD-STE100 (Issue 9, 2025) has 53 writing rules and a dictionary of 875 approved words. It
also lists 1,274 words that are not approved. Plainly takes the main ideas, writes them in its
own words, and adapts them for AI answers.

| | ASD-STE100 | Plainly |
|---|---|---|
| Goal | Certified aerospace and defense documentation | Clear AI answers, docs, runbooks, and prompts |
| Vocabulary | Only approved words, each with one meaning and one part of speech | Plain-word swaps and "AI-speak" to cut, as hints |
| Sentence length | 20 words for procedures, 25 for descriptions | The same targets, with Rule 0 first: never cut facts |
| Verbs | A small set of simple tenses, no "-ing" clauses, no phrasal verbs | The same ideas, followed strictly in strict mode only |
| Uncertainty | Not its focus | Rule 0: keep every hedge, add nothing, state every guess |
| Explaining | Not covered | An explain mode: one-sentence answer, steps, terms, the catch |
| Checking | People, or tools that ASD does not endorse | A form-only checker plus a review by the model |

Plainly does not replace the standard. For real STE work, use the official specification.

## The checker

```bash
uv run skills/plainly/scripts/plainly_check.py docs/runbook.md
python3 skills/plainly/scripts/plainly_check.py docs/runbook.md --strict --fail   # exit 1 on findings
```

Example output:

```text
L1    passive         "is utilized" - say who does it
L1    word            "utilize" -> use
L1    word            "leverage" -> use
3 findings | 2 sentences | average 5.5 words per sentence
```

It checks form, not meaning. Treat each finding as a hint.

## When to use Plainly

Use it when the reader must **understand and act**:

- explanations of hard topics, and AI answers you do not understand
- runbooks, procedures, and checklists
- prompts and instructions for AI agents
- error messages and tool descriptions
- READMEs and PR descriptions
- text for non-native readers or for translation
- documents for RAG

## When not to use Plainly

Do not use it when the reader must **weigh, judge, or feel**. Plainly breaks text into short
sentences with one idea each. That makes text clear, but it also cuts the links between ideas.
Some text needs those links.

| Do not use it for | Why |
|---|---|
| Critical thinking and debate | An argument lives in "because", "although", and "unless". Short sentences turn reasoning into a list of claims and hide the weak links. |
| Strategy and trade-offs | Strategy weighs options against an unknown future. "Main point first" pushes one confident answer too early. |
| Brainstorming and early ideas | Early thinking is meant to be messy. Making it clear too soon makes it look finished. |
| Research and science | "Suggests" and "is associated with" are exact claims, not filler. Plainly keeps them, but short sentences can split a finding from its limits. |
| Legal text, contracts, and policy | The exact wording is the point. A rewrite can change what it means legally. |
| Persuasive, emotional, or personal writing | A pitch, an apology, or feedback to a colleague sounds cold in a flat, procedure-like tone. |
| Creative writing and brand voice | Rhythm, metaphor, and personality are the value. Plainly removes them on purpose. |
| Experts writing for experts | Two specialists share terms. Defining every term wastes their time. |
| Certified aerospace documentation | Plainly is not ASD-STE100. Real STE needs the official dictionary and a trained writer. |

**A simple test:** if the reader must act, use Plainly. If the reader must weigh, judge, or
feel, do not.

**A middle path:** think in normal prose, then use Plainly on the result. For example, explore
a strategy freely. Then run `/plainly rewrite` on the decision and the action plan. Or run
`/plainly explain` to understand a dense answer before you judge it yourself.

## How it was tested

`claude plugin eval`, 3 runs per case, with and without the plugin, judged by Claude Sonnet.
Score is the share of graders passed. The graders check facts, numbers, commands, step order,
and hedges against the source text.

| Case | What it tests | With Plainly | Without | Δ |
|---|---|---|---|---|
| explain-dense-answer | Explain a dense LoRA answer. Keep all six facts and their qualifiers. | 1.00 | 0.00 | +1.00 |
| runbook-strict | Turn a messy failover note into steps. Keep every command and number. | 1.00 | 0.56 | +0.44 |
| keep-uncertainty | Simplify an incident update. Do not turn a guess into a fact. | 1.00 | 0.67 | +0.33 |
| note-hides-step | Move a safety check out of a note, before the action, with the reason. Add no new steps. | 1.00 | 0.00 | +1.00 |

The skill fired on its own in every run, with no slash command. Four cases is a small sample.
Treat these numbers as a smoke test, not a benchmark.

## Plugin layout

```text
.claude-plugin/        plugin.json, icon.png
skills/plainly/        SKILL.md, references/ (rules, words, examples), scripts/plainly_check.py
output-styles/         plainly.md
snippets/              plainly-lite.md
```

## License and trademark

- Plainly is MIT licensed. See [LICENSE](LICENSE).
- Plainly is **not** ASD-STE100 and is not affiliated with or endorsed by ASD or the STEMG.
  ASD-STE100 Simplified Technical English is a registered trademark of ASD. The specification is
  © ASD.
- Plainly does not copy the specification's rules, dictionary, or examples. All rules, word
  lists, and examples here are original and follow general plain-language practice.
- Plainly does not make text STE-compliant. For certified STE, get the official specification
  from [asd-ste100.org](https://www.asd-ste100.org).
- AI output can look plain and still be wrong. A person stays responsible for checking it.

## Credits

- The idea of prompting in controlled technical English: Andrej Karpathy, and the
  [Menon Lab write-up](https://blog.themenonlab.com/blog/asd-ste100-simplified-technical-english-prompting).
- The "keep the hedge" lesson: community tests showing that strict simplification can drop
  facts.
