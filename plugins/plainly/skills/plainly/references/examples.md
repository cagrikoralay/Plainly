# Before and after

All examples are original. Use them to copy the pattern, not the content.

## 1. Explain a dense AI answer (explain, light)

**Before**

> Retrieval-augmented generation essentially leverages a vector store to semantically
> retrieve contextually relevant chunks, which are subsequently injected into the prompt,
> thereby grounding the model's output and mitigating hallucinations, although retrieval
> quality is crucially contingent upon chunking strategy and embedding fidelity.

**After**

> **In one sentence:** RAG finds relevant parts of your documents and gives them to the model
> with your question.
>
> **How it works**
> 1. Your documents are cut into small parts, called *chunks*.
> 2. Each chunk is turned into a list of numbers, called an *embedding*. Similar meanings get
>    similar numbers.
> 3. When you ask a question, the system finds the chunks with the closest embeddings.
> 4. It adds those chunks to the prompt.
>
> **Why it helps:** The model answers from your text, so it invents fewer facts.
>
> **The catch:** The answer is only as good as the chunks it finds. Bad chunking or weak
> embeddings give bad results.

What changed: one-sentence answer first; terms kept and defined; one idea per sentence;
"leverages", "essentially", "crucially" removed; the limit (the catch) is kept.

## 2. Rewrite a procedure (rewrite, strict)

**Before**

> Before the migration is performed it should be ensured that a backup has been taken, and
> the service should be stopped, unless it's a read replica in which case it can stay up,
> then run the migration and restart once done, waiting about 30s for health checks.

**After**

> 1. Make a backup of the database.
> 2. If the server is not a read replica, stop the service.
> 3. Run the migration.
> 4. Start the service.
> 5. Wait about 30 seconds for the health checks to pass.

What changed: numbered steps; each step starts with a verb; passive "should be ensured"
became an action; the condition comes before its action; "about 30s" kept as "about 30
seconds" — the uncertainty and the number stay.

## 3. Keep uncertainty (rewrite, light)

**Before**

> It seems likely that the memory leak could potentially be related to the caching layer,
> though this hasn't been fully confirmed yet.

**Bad after** (breaks Rule 0 — a guess became a fact)

> The caching layer causes the memory leak.

**Good after**

> The memory leak is probably in the caching layer. We have not confirmed this.

## 4. Simplify a prompt to an AI (rewrite, strict)

**Before**

> I'd like you to kind of go through my code and maybe look for anything that could be
> improved performance-wise, but don't change the API, and also it would be great if you
> could explain things and not just do them.

**After**

> Review my code for performance problems.
> - Do not change the public API.
> - For each change, explain why it is faster.

## 5. Check (check mode output format)

**Input**

> The configuration file is utilized by the deployment pipeline to facilitate environment
> specific overrides which are applied at build time.

**Output**

> | # | Problem | Rule | Fix |
> |---|---|---|---|
> | 1 | "is utilized by" — passive, and "utilize" | 11, 1 | "The deployment pipeline uses ..." |
> | 2 | "to facilitate" | 1 | "to allow" |
> | 3 | "environment specific overrides" — what are they? | 3 | name or define them |
>
> **Rewrite:** The deployment pipeline uses the configuration file to set different values for
> each environment. It applies these values at build time.

## 6. Warning with a reason, and a note that hid a step (rewrite, strict)

**Before**

> 3. Truncate the staging tables.
>
> Note: make sure you're not connected to prod when doing this, it'll wipe everything; also
> the truncate should take <1 min.

**After**

> 3. Make sure that you are connected to the staging database, not production. Truncating
>    deletes all rows in the tables.
> 4. Truncate the staging tables. This takes less than 1 minute.

What changed: the check was hidden in a note, so it became a step, before the action (rules
19, 20). The warning says what goes wrong. The expected time moved into the step. The
semicolon and the contractions are gone (rules 13, 15).

## 7. Unclear pointer and a vague requirement (check)

**Input**

> The cache stores results from the database. When it gets slow, you should restart it.

**Output**

> | # | Problem | Rule | Fix |
> |---|---|---|---|
> | 1 | "it" (two times) can mean the cache or the database | 14 | Name the thing. The text does not say which, so confirm with the author. |
> | 2 | "you should" — required or optional? | 8 | "Restart ..." if required. "We recommend that you restart ..." if optional. |
>
> **Rewrite:** The cache stores results from the database. When the cache gets slow, restart
> the cache.
>
> Assumed: "it" means the cache in both places, and the restart is required. Confirm this.

What changed: the rewrite had to pick a meaning, so it says what it assumed (Rule 0). It does
not hide the guess.
