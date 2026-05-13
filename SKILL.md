---
name: source-skill-pipeline
description: Build reliable source-specific Codex or Claude skills from any resource type supported by skill-seekers, including local codebases, GitHub repositories, documentation sites, PDFs, Word documents, EPUBs, videos, OpenAPI specs, PPTX decks, RSS feeds, Confluence, Notion, chat exports, and mixed source sets. Use this whenever the user wants to turn a repo, document, website, API spec, knowledge source, or collection of resources into a skill, improve an auto-generated skill, package source knowledge as a skill, or combine skill-seekers and skill-create into a dependable workflow.
---

# Source Skill Pipeline

Use this skill to turn a repository, document, website, API spec, knowledge source, or mixed source set into a reliable source-specific skill. The workflow has two halves:

1. Use `skill-seekers` or an equivalent source analyzer to inspect the resource and generate a draft skill.
2. Use `skill-create`, `skill-creator`, or an equivalent improvement loop to validate, refine, and package the final skill.

The important thing is not the exact command name or whether every optional helper is installed. The important thing is preserving the contract between the two phases: the analyzer produces a grounded draft from real source evidence; the optimizer turns that draft into a lean, triggerable, tested skill.

## Inputs To Gather

Before changing files, identify:

- Target source or source set. This may be a local path, GitHub repo, docs URL, PDF, Word file, EPUB, video, OpenAPI spec, PPTX, RSS feed, Confluence space, Notion page, chat export, or a multi-source config.
- Source type, or whether it should be auto-detected.
- Source access needs, such as network, credentials, API tokens, or local files.
- Three recommended skill names and whether the user wants to choose one or provide a custom name.
- Existing tool paths or commands for `skill-seekers` and `skill-create`.
- Where the final skill should be written.
- Whether the user wants evaluation runs now or only a first packaged draft.
- Whether the user is willing to install missing helper tools, if installation instructions are available.

If the user did not provide all inputs, make conservative assumptions:

- Use the current working directory as the target source only when it contains recognizable project or source files.
- Write generated skills under a sibling or explicit output directory, not inside source folders unless requested.
- Generate three recommended names from the source title, domain, repository name, document title, or user goal.
- Ask the user to pick one of the three names or provide a custom name before finalizing the skill name when interaction is possible.
- If the user is unavailable and the task must proceed, use the strongest recommendation and report the choice.
- Include eval prompts even if full execution is deferred.

## Naming Rule

The final generated skill name is selected in two steps:

1. Propose three concise kebab-case base names.
2. Let the user pick one or provide a custom base name.

The final package name must append `-skill` to the selected base name:

```text
<selected-name>-skill
```

Apply this rule to both the output directory and the `name` field in `SKILL.md` frontmatter.

Normalize the selected name first:

1. Infer candidate names from the user's explicit goal, source title, package metadata, repository name, URL domain/path, document title, or target file basename.
2. Convert it to kebab-case.
3. Append `-skill`.
4. If the normalized selected name already ends with `-skill`, do not append it a second time.

Recommended names should cover different useful angles:

- A source-name option, such as `example-app` or `stripe-api`.
- A task/workflow option, such as `frontend-maintenance` or `api-integration`.
- A broader domain option, such as `payments-docs` or `team-onboarding`.

Examples:

- `example-app` -> `example-app-skill`
- `Medtronic Portal` -> `medtronic-portal-skill`
- `Stripe OpenAPI` -> `stripe-openapi-skill`
- `Notion Team Handbook` -> `team-handbook-skill`
- `foo-skill` -> `foo-skill`

If the user asks for a different display title, keep the skill package name in this format and put the friendly title in prose or references instead.

## Supported Source Types

When `skill-seekers` is available, support every source type exposed by that installation. Common commands include:

- `create`: create a skill from any source with auto-detection.
- `analyze`: analyze a local codebase.
- `github`: scrape a GitHub repository.
- `scrape`: scrape a documentation website.
- `pdf`, `word`, `epub`, `pptx`: extract from document files.
- `video`: extract from YouTube or local video.
- `openapi`: extract from OpenAPI or Swagger specs.
- `html`, `asciidoc`, `jupyter`, `manpage`: extract from local technical formats.
- `rss`: extract from RSS or Atom feeds.
- `confluence`, `notion`, `chat`: extract from workspace or communication exports.
- `unified`: combine multiple source types into one skill.

Prefer `skill-seekers create` or `skill-seekers unified` when the user gives mixed or ambiguous resources. Prefer a specific command when the source type is clear and the help text shows that command is supported.

## Phase 0: Discover Tools

First discover what is actually installed. Check for commands, skill directories, and local scripts before assuming exact names.

Suggested checks:

```bash
command -v skill-seekers
command -v skill-create
command -v skill-creator
rg --files ~/.codex/skills ~/.agents/skills ~/.skills-manager/skills 2>/dev/null | rg 'skill-(seekers|create|creator)|seekers'
find . -maxdepth 4 -iname '*skill*seek*' -o -iname '*skill*create*'
```

If command discovery is noisy, run `scripts/discover_skill_tools.py` from this skill and read its summary.

Treat `skill-seekers` and `skill-create` as optional accelerators, not hard dependencies:

- **Both present**: run the full automated pipeline.
- **Only `skill-seekers` present**: use it for draft generation, then optimize manually with the `skill-creator` workflow.
- **Only `skill-create` present**: manually draft from source evidence, then pass that draft through `skill-create`.
- **Neither present**: run the fully built-in fallback workflow using filesystem inspection, eval prompts, validation, and packaging.

If a missing tool appears installable from local documentation or a known package manager, ask the user before installing it. Do not block the task while waiting for a perfect setup; if installation is declined, unavailable, or unclear, continue with the fallback path and report that choice.

If `skill-seekers` is missing, use source-appropriate inspection as the analyzer fallback:

- For repositories and local code: read README, manifests, configs, entry points, tests, and docs.
- For documents and decks: extract headings, structure, key procedures, terminology, examples, and reusable workflows.
- For websites and docs URLs: fetch or browse the relevant pages if network access is available; otherwise ask for local exports.
- For API specs: parse endpoints, auth, schemas, examples, and common integration tasks.
- For chat or workspace exports: identify recurring workflows, decisions, conventions, and support patterns.
- Capture evidence with file paths, URLs, section names, or source identifiers so the draft skill is traceable.

If `skill-create` is missing, use the `skill-creator` workflow as the optimizer fallback:

- Improve `SKILL.md` directly.
- Add realistic eval prompts.
- Validate frontmatter.
- Package with a known `package_skill.py` when available.

## Phase 1: Analyze And Draft

Run `skill-seekers` if available. Prefer an output directory that keeps all intermediate artifacts together. Use the command matching the source type:

```bash
skill-seekers create <source> --name <selected-name>
skill-seekers analyze <local-code-path> --output <workspace>/draft-skill
skill-seekers github --repo <owner/repo> --name <selected-name>
skill-seekers scrape --config <docs-config>
skill-seekers unified --config <multi-source-config>
```

If the actual CLI shape differs, inspect `--help` and adapt. Do not force this exact command if the tool exposes another interface.

If `skill-seekers` is not available, create the draft yourself:

1. Build a short evidence map from the source.
2. Infer the skill's trigger scope from the source purpose and workflows.
3. Write a first `SKILL.md` that only includes facts supported by the source.
4. Put longer findings into source-appropriate reference files when useful.
5. Mark uncertain setup steps as "verify before using" or leave them out.

The draft skill should include:

- Source purpose and when the skill should trigger.
- Common workflows the assistant should perform for this source.
- Important commands, procedures, APIs, concepts, or extraction rules supported by evidence.
- Important directories, sections, endpoints, pages, documents, or ownership boundaries.
- Safe editing, citation, access, and update rules specific to the source.
- Known pitfalls, generated files, environment setup, external services, or credential boundaries.
- References to files, URLs, source sections, or bundled reference documents instead of huge pasted source blocks.

After generation, inspect the draft before optimizing. Remove stale, speculative, or over-broad claims that are not supported by source evidence.

## Phase 2: Normalize The Draft

Make the generated skill fit the standard shape:

```text
selected-name-skill/
├── SKILL.md
├── references/
├── scripts/
└── evals/
```

Keep `SKILL.md` focused and under control:

- Put always-needed workflow guidance in `SKILL.md`.
- Put long source summaries in `references/source-map.md`.
- Put architecture notes in `references/architecture.md` for code sources.
- Put command maps in `references/commands.md` when commands matter.
- Put API maps in `references/api.md` for API specs.
- Put deterministic helpers in `scripts/`.
- Put test prompts in `evals/evals.json`.

The description field is the trigger surface. Make it concrete and a little assertive. It should mention the selected skill name's source/domain, the source type, and the situations where the skill should be used.

Before optimizing, check that the draft skill's directory name and frontmatter `name` both follow `<selected-name>-skill`. If an analyzer generated the selected name without the suffix, rename the directory and update frontmatter before continuing.

## Phase 3: Optimize With Skill-Create

Run `skill-create` if available. The optimizer should treat the analyzer output as a draft, not as truth.

Expected optimization goals:

- Sharpen the trigger description.
- Remove duplicated or generic advice.
- Convert vague source facts into actionable workflows.
- Add missing verification and rollback cautions.
- Add eval prompts that represent real user requests.
- Ensure the skill can be packaged and installed cleanly.

Suggested command shape:

```bash
skill-create improve <draft-skill-path> --source <source> --output <final-skill-path>
```

If the actual CLI differs, inspect `--help` and adapt.

If `skill-create` is not available but a `skill-creator` skill or directory is available, use that workflow as the optimizer. If neither is available, still do the same steps manually:

1. Snapshot the generated draft.
2. Add 3 to 5 realistic eval prompts in `evals/evals.json`.
3. Run with-skill and baseline evals when subagents or an equivalent runner are available.
4. Generate a review viewer with `eval-viewer/generate_review.py` before revising based on subjective quality.
5. Update the skill based on feedback, then rerun the same evals.

When no eval runner or viewer is available, keep the eval prompts and do a lightweight review inline:

- Check that each prompt would trigger the generated source skill.
- Check that the skill tells an agent what source files, pages, sections, or references to read first.
- Check that commands, procedures, APIs, and source facts are evidence-backed.
- Check that verification steps are clear.
- Record the limitation in the final report.

## Phase 4: Reliability Checks

Before calling the skill final, verify:

- `SKILL.md` has valid YAML frontmatter with `name` and `description`.
- The skill name is kebab-case, matches the directory, and ends with `-skill`.
- The description is specific enough to trigger for this source and not for unrelated sources.
- Instructions cite real files, URLs, sections, endpoints, or references where appropriate.
- Commands, API details, procedures, and source facts are copied from evidence, not guessed.
- The skill tells future agents how to handle dirty worktrees and generated files.
- Eval prompts cover onboarding, implementation, debugging, and verification workflows.
- Packaging excludes root `evals/` unless the packager intentionally includes them.

Use a quick validation script if available:

```bash
python <skill-creator-path>/scripts/quick_validate.py <final-skill-path>
```

Then package:

```bash
python <skill-creator-path>/scripts/package_skill.py <final-skill-path> <dist-dir>
```

## Output Format

When finished, report:

- Final skill directory.
- Packaged `.skill` file path, if created.
- Which analyzer and optimizer were used.
- Any missing tools, whether installation was attempted, and which fallback was used.
- Validation and packaging results.
- Recommended next eval or installation step.

Keep the report short and practical. The user mainly needs to know where the skill is, how it was built, and what confidence checks passed.

## When Tool Behavior Is Unknown

Do not invent exact CLI flags beyond examples. If a command exists but usage is unclear:

1. Run its help command.
2. Prefer documented flags.
3. Record the observed command in the final report.
4. If help is unavailable, use the fallback workflow rather than blocking.

The goal is a reliable source-specific skill, not loyalty to a specific command spelling.
