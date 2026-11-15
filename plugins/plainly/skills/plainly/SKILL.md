---
name: plainly
description: Explain, rewrite, or check text in plain, short, clear English, using simple rules loosely inspired by the controlled technical English of aircraft maintenance manuals (ASD-STE100 style). Use this whenever the user finds an AI answer hard to follow ("I don't get it", "explain simply", "ELI5", "too dense", "TL;DR this"), asks to simplify, clarify, or plain-English a text, wants a runbook, procedure, README, PR description, error message, or prompt made clearer, asks for "Simplified Technical English" or "STE", or asks to review writing for readability — even if they do not name this skill.
argument-hint: "[explain|rewrite|check] [strict] [text or file]"
license: MIT
---

# Plainly

Make text short, clear, and easy to act on — without losing what it says.

The rules are in [references/rules.md](references/rules.md). Read them before your first output
in a session. Word swaps are in [references/words.md](references/words.md). Before/after
patterns are in [references/examples.md](references/examples.md). Read them when you are unsure
of the output shape.

## Why this works

Dense text hides its facts. Short sentences, common words, and steps that start with a verb
are faster to read and easier to check. Non-native readers and other AI agents follow them
better. The danger is that simplifying drops facts or turns a guess into a
fact. That is why **Rule 0 (keep the meaning) beats every other rule.**

## 0. Check the fit

Plainly suits text that a reader must understand and act on. It is a poor fit when the reader
must weigh, judge, or feel. Short sentences cut the links between ideas, and in that kind of
text the links are the content. Poor fits:

- arguments, critical thinking, strategy, and trade-offs
- brainstorming and early ideas
- research findings, where each hedge is an exact claim
- legal text, contracts, and policy
- persuasive, emotional, personal, or creative writing
- text by experts for experts
- certified aerospace documentation (see "What this is not")

If the text is a poor fit, say so in one line, with the reason. Then offer the middle path:
simplify only the parts that a reader acts on, such as the decision, the action items, or the
steps. Use `explain` so the user understands the text before they judge it. Do not refuse.
If the user still wants the full rewrite, do it.

## 1. Pick the mode

Use the first word of the arguments if it is a mode. Otherwise infer it:

| Mode | When | Input |
|---|---|---|
| `explain` | The user does not understand something: an earlier answer, a concept, a pasted text. | The text, or your own previous answer if none is given. |
| `rewrite` | The user wants a clearer version of a text: docs, steps, prompt, message. | The given text or file. |
| `check` | The user wants feedback on readability, not only a new version. | The given text or file. |

If there are no arguments and no text, apply `explain` to your own previous answer.

## 2. Pick the strength

- **light** (default): about 80% of the way to strict. Natural tone. For explanations, chat,
  READMEs, PR descriptions.
- **strict**: every rule. For procedures, runbooks, prompts, agent instructions, error
  messages, safety notes. Use it when the user says "strict" or the text is a procedure.

## 3. Write the output

### explain

Use this shape. Drop a section if it adds nothing.

```
**In one sentence:** <the answer, in 25 words or fewer>

**How it works** (or **The key points**)
1. <one idea per line, short sentences>

**Example:** <one small, concrete example>   (only if it helps)

**Terms**
- *<term>*: <plain meaning>                    (only terms the reader needs)

**The catch:** <limits, conditions, uncertainty from the source>   (if any)
```

Keep real technical terms — people need them to search and talk to others — but define each
one in plain words.

### rewrite

Output only the rewritten text, in the same format as the input (Markdown stays Markdown, code
stays untouched). Give one version. Do not add an intro ("Here is ...") or a second, shorter
version. The user will copy and paste the text as it is, so any extra words become their work
to delete. After the text, add a line only if needed:

- `Kept as-is: <what you did not simplify and why>`
- `Assumed: <what you had to guess, such as what an unclear "it" means>`. Confirm it with the
  user. A hidden guess breaks Rule 0.
- `Missing: <what the source does not say but a reader will need>`. For example: what to do if
  a check fails, or who to call. Do not write the missing step into the text yourself, not even
  as a placeholder. The author must supply it.

Write these lines in the same plain style as the text.

If the user asked you to change a file, edit the file in place. Otherwise, show the new text.

### check

1. If the input is long or is a file, run the checker (see below) to get the mechanical findings.
   Add `--strict` for procedures and prompts.
2. Add what the checker cannot see. Look for these problems:
   - unclear terms, or two terms for one thing
   - a missing actor
   - an "it" or "this" that can point to two things
   - "should" where the reader cannot tell if a step is required
   - a condition or warning after its action, or a warning with no reason
   - a step, limit, or expected result hidden in a note
   - a vague statement ("X affects Y") where the source knows how
   - a buried main point
3. Output a table `| # | Problem | Rule | Fix |` with at most 10 rows, most important first.
   Then give a **Rewrite:** of the text. If the text is long, rewrite only the worst paragraph.

## 4. Verify before you answer

Compare your output to the source:

- Every number, unit, name, condition, and limit is still there.
- Every "may / might / probably / not confirmed" is still uncertain. No new certainty.
- You added nothing that the source did not say. Any guess is in an `Assumed:` line.
- Steps are in the order the source needs.
- Every "it", "this", and "they" points to one thing.

If simplifying would change the meaning, keep the original wording and note it in
`Kept as-is:`.

## The checker

`scripts/plainly_check.py` flags long sentences, passive voice, long paragraphs, semicolons,
and words from the swap list. With `--strict`, it also flags contractions and complex verb
forms ("has been running"). It only checks form, not meaning. Run it with `uv` or Python 3:

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/plainly_check.py" FILE
python3 "${CLAUDE_SKILL_DIR}/scripts/plainly_check.py" FILE
```

Use `-` as FILE to read from stdin. Add `--strict` for strict mode. Add `--fail` to exit 1 when
there are findings (useful in CI).
A finding is a hint, not an order: a passive sentence with an unknown actor is fine.

## What this is not

This is not the ASD-STE100 standard. It does not use the official dictionary and does not make
text compliant with that standard. Some users need certified STE, for example for aerospace
documentation. Tell them so, and point them to the official specification from ASD at
https://www.asd-ste100.org.
