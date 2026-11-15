# Plainly rules

Our own plain-language rules. Loosely inspired by controlled technical English used in
aerospace manuals. Not the ASD-STE100 standard and not a copy of it.

Rule 0 is above all other rules. If a rule makes the text less true, break the rule.

## Rule 0 — Keep the meaning

- Keep every fact, number, unit, name, condition, limit, and exception.
- Keep uncertainty. "May fail" stays "may fail". Do not make a guess sound like a fact.
  Do not make a fact sound like a guess.
- Do not add facts, reasons, or advice that the source does not give.
- Say each hedge once, plainly. "It might possibly perhaps" becomes "It may".

## Words

1. **Use the common word.** "Use", not "utilize" or "leverage". No slang or in-group jargon
   ("nuke the cache" becomes "delete the cache"). See `words.md`.
2. **One word, one meaning.** Use one term for one thing. Do not switch between "server",
   "host", and "box" for the same machine. When the same action comes back, use the same
   wording each time.
3. **Define a technical term once.** Keep the real term (people search for it). Explain it in
   plain words the first time it appears. Write an abbreviation in full the first time:
   "time to live (TTL)".
4. **Use verbs, not noun forms.** "Decide", not "make a decision". "Check", not
   "perform a check of". Do not turn nouns into verbs: "action this" becomes "do this".
5. **No long noun stacks.** Three nouns in a row is the limit. "Database connection pool size
   limit setting" becomes "the size limit of the database connection pool".
6. **Prefer one-word verbs.** Phrasal verbs ("carry out", "come up with", "figure out") have
   many meanings and are hard for non-native readers. Use "do", "make", "find".
7. **No Latin abbreviations.** Write "for example", not "e.g." Write "that is", not "i.e."
   List the items instead of writing "etc."
8. **Say how strong a requirement is.** "Must" when it is required. "We recommend" when it is
   optional. "Should" leaves the reader to guess.

## Sentences

9. **Keep sentences short.** Steps: 20 words or fewer. Explanations: 25 words or fewer.
   This is a target. Split a long sentence. Do not cut facts to make it fit. Code, a number
   with its unit, a name, quoted text, and text in parentheses each count as one word.
10. **One idea per sentence.** One action per step, unless two actions happen together
    ("Hold the button and turn the key").
11. **Say who does what.** Use active voice: "The script deletes the file", not
    "The file is deleted". Passive is fine when the actor is unknown or does not matter.
12. **Use simple verb forms.** "The job failed", not "the job has been failing".
    "When you run the test", not "when running the test".
13. **Keep the small words.** Keep "the", "a", "is", "to". Keep "that" after "make sure" and
    "show": "Make sure that the port is open". Telegraphic text ("Check config, restart svc")
    is short but harder to read. In strict mode, do not use contractions ("do not", not "don't").
14. **Make every pointer clear.** If "it", "this", or "they" could point to two things, repeat
    the noun. For people, use "you" or "they".
15. **No semicolons.** Write two sentences.
16. **Be concrete.** Say how, how much, and in which direction, when the source gives it.
    "Load changes latency" hides the fact. "When the load goes up, latency goes up" states it.
    If the source does not give the detail, do not invent it (Rule 0).

## Structure

17. **Steps are numbered and start with a verb.** "1. Open the file." Use a list when there are
    three or more items or steps. A step may start with a short condition: "If X, do Y."
18. **One topic per paragraph.** Put the main point first. Six sentences at most.
19. **Warnings come first and say why.** Put a warning or condition before the action it is
    about. Then say what can go wrong: "Do not run this on the primary. It deletes all rows."
20. **Notes give information only.** Put actions, limits, and expected results in the step
    itself, not in a note under it. A reader who skips the notes must still do the task right.

## Strength

- **light** (default): follow the rules about 80% of the way. Keep a natural tone. Use for
  explanations, chat, READMEs, PR descriptions. Contractions are fine.
- **strict**: follow every rule. Use for procedures, runbooks, prompts, agent instructions,
  error messages, safety notes.
