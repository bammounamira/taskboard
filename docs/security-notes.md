# TaskBoard — initial security notes

| Question | Our answer |
| --- | --- |
| What data does the application handle? | Task IDs, titles, descriptions and statuses, kept in memory. Later: users, task owners, and data in a PostgreSQL database. |
| Who should be able to create, update or delete a task? | Only authenticated users, and only on their own tasks. Today nothing is enforced: there is no authentication, so anyone who reaches the API can read, modify or delete any task. |
| Which inputs come from users? | The JSON body of POST and PATCH (`title`, `description`, `status`) and the `task_id` path parameter. Later: query parameters (filters, pagination) and headers (auth tokens). |
| What abuses are possible today? | Unauthorised modification or deletion of any task; enumeration of IDs (they are sequential: 1, 2, 3…); flooding the in-memory store with many tasks until the process runs out of memory (no rate limit, no quota); large request bodies; storing HTML/JS in titles that a future web front-end could render (stored XSS). |
| What secrets could appear in this project later? | Database password (`DATABASE_URL`), `SECRET_KEY` (token signing), third-party API tokens, cloud and CI/CD credentials, TLS private keys. |
| Which controls already exist, and which test proves each? | Status whitelist → `test_invalid_status_is_rejected`; trimmed, non-blank title → `test_blank_title_is_rejected`; length limits → `test_title_too_long_is_rejected`, `test_description_too_long_is_rejected`; unknown fields forbidden → `test_client_cannot_set_id_on_create`; null not allowed on PATCH → `test_patch_null_title_is_rejected`; positive IDs → `test_non_positive_id_is_rejected`. Non-tested controls: `.gitignore` for `.env`/keys, `.env.example` with placeholders only, protected `main` (PR + 1 approval, no force push), peer review. |
| What automated control should we add next? | A CI pipeline running `pytest` on every PR and blocking the merge on failure; then secret scanning (e.g. gitleaks), SAST (e.g. Bandit/Semgrep), SCA on pinned dependencies (pip-audit), and security gates. |
