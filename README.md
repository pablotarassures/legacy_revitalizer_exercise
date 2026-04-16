# AI Prompting Practice — Spaghetti Code Refactoring

## Exercise Brief

Refactor an intentionally messy Python script using AI prompting tools (GitHub Copilot).  
The goal is to develop effective prompting habits — not just get working code.

## Resources

- VS Code
- GitHub Copilot Extension
- Python 3.x

## Deliverable

A GitHub repository containing:
- A **"Before" commit** with the original `process_data.py`
- An **"After" commit** with the fully refactored module structure
- A `LOG.md` file detailing the 3 prompts that yielded the best results

## The Starting File

`before/process_data.py` — intentionally contains:

| Problem | Description |
|---|---|
| Global mutable state | `l`, `d` at module level |
| Cryptic names | `l`, `d`, `fn`, `a`, `b`, `u`, `p` |
| Mixed responsibilities | `fn()` handles add, show, and save |
| Hardcoded credentials | `{"u": "admin", "p": "12345"}` |
| No error handling | File I/O, input validation |
| No context manager | `open()` without `with` |
| Bare script execution | Runs on import |
| Dead code | `calculate_something_else()` never called |

## The Refactored Structure

```
after/
├── models.py        ← Item dataclass
├── auth.py          ← AuthService (timing-safe, attempt-limited)
├── repository.py    ← FileRepository (error handling, load + save)
├── store.py         ← DataStore (validation, in-memory state)
└── process_data.py  ← main() entry point only
```

## Suggested Prompting Sequence

1. **Plan first** — ask for a full SOLID-based refactoring plan before writing any code
2. **Rename** — ask for better variable/function names with rationale for each
3. **Modularize** — extract classes into separate files with explicit file names
4. **Error handling** — target file I/O and input validation specifically
5. **Security** — ask for the production-level fix for each vulnerability found

See `LOG.md` for the 3 prompts that produced the most valuable results.
