# LOG.md — AI Prompting Exercise: Spaghetti Code Refactoring

**Date**: 2026-04-15
**Tools**: VS Code, GitHub Copilot, Python 3.x

---

## Prompt 1 — Broad Refactoring Plan

**Prompt used**:
> "How can I refactor `process_data.py` to follow SOLID principles and remove global variables?"

**Why it worked**:
Starting broad forces the AI to produce a structured plan before touching any code. It prevents jumping straight into line-level fixes and ensures every change has a principled reason. The response mapped each SOLID letter to a concrete violation in the file and proposed a class structure before writing a single line of code.

**Key output**:
- Identified 3 classes needed: `DataStore`, `FileRepository`, `AuthService`
- Proposed a command dispatch pattern to satisfy Open/Closed
- Flagged hardcoded credentials as a Dependency Inversion violation
- Ordered the refactoring steps (rename → extract → wire → guard)

**Lesson**: Always get a plan before asking for code. It makes subsequent prompts faster and more targeted.

---

## Prompt 2 — Modularization

**Prompt used**:
> "Extract the `DataStore`, `FileRepository`, and `AuthService` classes into separate files, keeping `process_data.py` as the entry point."

**Why it worked**:
The prompt was specific about the outcome (separate files) and the constraint (keep `process_data.py` as entry point). Vague modularization prompts often produce a single refactored file. Naming the target files and the relationship between them removed all ambiguity.

**Key output**:
- `models.py` — `Item` dataclass with no dependencies
- `store.py` — `DataStore` importing from `models`
- `repository.py` — `FileRepository` importing from `models`
- `auth.py` — `AuthService` with no dependencies
- `process_data.py` — `main()` only, importing all four

**Lesson**: Name the files and the dependency direction explicitly. The AI respects stated constraints when they are precise.

---

## Prompt 3 — Security with Design Discussion

**Prompt used**:
> "Address hardcoded credentials in `auth.py` and `process_data.py`. Identify any other security vulnerabilities and explain the production-level fix for each."

**Why it worked**:
Asking for "the production-level fix" elevated the response beyond just fixing the immediate code. It triggered a design discussion on timing attacks (`hmac.compare_digest`), secrets management (env vars vs. secrets manager), password hashing (bcrypt/argon2), and brute force protection. The phrase "explain... for each" ensured every fix came with a rationale, not just a code change.

**Key output**:
- Removed hardcoded fallback defaults — fails fast at startup instead
- Replaced `==` with `hmac.compare_digest()` — timing-safe comparison
- Added `MAX_LOGIN_ATTEMPTS = 3` with lockout and attempt counter
- Documented why env vars are still not production-safe (crash dumps, process listings)
- Provided the upgrade path to a secrets manager

**Lesson**: Append "explain the production-level fix" to any security prompt. It turns a patch into a learning artifact.

---

## Summary

| # | Prompt pattern | Best for |
|---|---|---|
| 1 | Broad plan first ("how can I refactor X to follow Y?") | Scoping work before writing code |
| 2 | Explicit structure ("extract X into separate files, keep Y as entry point") | Modularization tasks |
| 3 | Fix + rationale ("identify vulnerabilities and explain the production fix") | Security reviews and design discussions |
