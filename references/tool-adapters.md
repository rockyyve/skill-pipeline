# Tool Adapters

Use this reference when adapting the pipeline to the exact local tools installed on a machine.

## Dependency Policy

`skill-seekers` is the preferred analyzer. If it is missing, try the installation flow first. `skill-create` is an optimizer accelerator; a source-specific skill can still be produced without it.

Use this decision table:

| Available tools | Analyzer path | Optimizer path |
| --- | --- | --- |
| `skill-seekers` + `skill-create` | Run `skill-seekers` | Run `skill-create` |
| `skill-seekers` only | Run `skill-seekers` | Use skill-creator/manual optimization |
| `skill-create` only | Install `skill-seekers`; fallback to manual source inspection if install fails | Run `skill-create` |
| Neither | Install `skill-seekers`; fallback to manual source inspection if install fails | Manual skill-creator-style optimization |

## skill-seekers Installation Flow

When `skill-seekers` is missing, attempt installation before source analysis:

1. Check available Python tooling with `python3 --version`, `python3 -m pip --version`, and `command -v uv`.
2. Prefer `python3 -m pip install --user skill-seekers` for the default install.
3. Use `uv tool install skill-seekers` if `uv` is available and the user prefers isolated CLI tools.
4. Use extras when the source requires them, for example `skill-seekers[pptx]`, `skill-seekers[video]`, `skill-seekers[notion]`, `skill-seekers[confluence]`, `skill-seekers[rss]`, `skill-seekers[chat]`, or `skill-seekers[all]`.
5. Ask before installing because the command may need network access and modifies the user environment.
6. Verify with `skill-seekers --version` and `skill-seekers --help`.

If installation requires credentials, fails due to environment restrictions, or the user declines, continue with fallback instead of blocking.

If `skill-create` is missing, do not stop. Use skill-creator/manual optimization unless the user explicitly wants to install or configure a separate optimizer.

The final report should say which path was used so the user understands the confidence level and remaining setup gap.

## Naming Contract

Before finalizing, propose three recommended kebab-case base names and let the user choose one or provide a custom name. Every generated skill should then use `<selected-name>-skill` as both the folder name and the `name` frontmatter value. If the selected name already ends in `-skill`, keep it as-is rather than producing `-skill-skill`.

The three recommendations should include:

- One name based on the source title, repo, file, or domain.
- One name based on the workflow the skill enables.
- One name based on the broader domain or audience.

## Source Type Coverage

Use the exact `skill-seekers` installation on the machine as the source of truth, but common supported commands include `create`, `github`, `scrape`, `analyze`, `pdf`, `word`, `epub`, `video`, `unified`, `jupyter`, `html`, `openapi`, `asciidoc`, `pptx`, `rss`, `manpage`, `confluence`, `notion`, and `chat`.

Prefer `create` for auto-detection and `unified` for multi-source configs. Prefer a specific command when the user gives a clear source type.

## skill-seekers Adapter

Role: inspect a supported source and produce a source-grounded draft skill.

Minimum acceptable output:

- A `SKILL.md` draft.
- A folder and frontmatter name following `<selected-name>-skill`.
- A summary of source purpose.
- A list of source-specific commands, procedures, APIs, concepts, or workflows.
- A list of important directories, files, pages, sections, endpoints, or documents.
- Notes on tests, build, lint, runtime, generated artifacts, citation rules, credentials, or source update patterns where relevant.

If the tool supports configurable output, ask it to create a skill folder rather than a plain report. If it only creates a report, convert the report into a skill manually.

Good signs:

- It cites concrete files, URLs, sections, endpoints, or source identifiers.
- It distinguishes verified commands from inferred commands.
- It includes source-specific workflows rather than generic advice.

Bad signs:

- It lists commands, endpoints, or facts that do not exist in the source evidence.
- It pastes too much source code into `SKILL.md`.
- It creates a generic skill without clear source boundaries.

## skill-create Adapter

Role: improve a draft skill into a final skill that triggers well and survives repeated use.

Minimum acceptable output:

- Cleaner `SKILL.md` frontmatter and body.
- Added or improved eval prompts.
- Validation results.
- Packaging-ready folder structure.

Good optimization asks:

- "Tighten this skill so it only triggers for this source, domain, and closely related work."
- "Replace vague guidance with workflows backed by source evidence."
- "Add eval prompts for onboarding, implementation, debugging, and verification."
- "Remove instructions that duplicate general assistant behavior."

## Fallback Adapter

When either named tool is unavailable, use the manual skill-creator flow:

1. Analyze the source with the best available local or network-safe inspection method.
2. Draft `SKILL.md`.
3. Add source-specific references, such as `references/source-map.md`, `references/commands.md`, `references/architecture.md`, or `references/api.md`, only if useful.
4. Add `evals/evals.json`.
5. Validate with `quick_validate.py` if available.
6. Package with `package_skill.py` if available.

The fallback should be treated as first-class, not as a degraded answer. It often produces better output when the source is unusual or the user has source-specific conventions.
