# SEO Machine for Codex and portable skill hosts

A portable adaptation of [TheCraigHewitt/SEOMachine](https://github.com/TheCraigHewitt/seomachine), licensed under MIT. The original content workflows and analysis modules are retained. Claude-specific discovery and invocation have been replaced with standard skill directories and host-neutral instructions.

The main package is [`.agents/skills/seo-machine`](.agents/skills/seo-machine/SKILL.md). It includes workflow references, customer-context templates, Python modules and optional provider integrations. The other marketing skills remain individually selectable in `.agents/skills/`.

## Use in Codex

Clone this repository and open it in Codex. Select `seo-machine` or request the relevant content workflow. Codex discovers `.agents/skills/*/SKILL.md`. Other hosts can import the main directory as one pinned skill package; source paths and installed paths are different. Run Python with the customer's workspace as the working directory. Store customer files in `context/`, `drafts/`, `research/` and `output/`, outside the installed package.

```sh
python3 .agents/skills/seo-machine/scripts/preflight.py
python3 .agents/skills/seo-machine/scripts/analyze_file.py article.md --keyword "content planning" --output output/report.json
```

The local report uses the existing quality, intent and text-scrubbing modules. It makes no provider calls and refuses to overwrite a report. Scores are heuristics, not proof of ranking or citation improvement. Readability, clustering and live-provider workflows require the additional packages reported by preflight. Provider setup examples are under `.agents/skills/seo-machine/data_sources/config/`; never commit credentials. Host-managed connections are inspected through the host, independently of this environment check.

## Customer context and memory

Supply your own brand voice, audience, product claims and target terms. Templates contain no customer facts. On hosts with durable memory, explicitly ask to remember a lasting preference and review the exact statement and scope. The skill requires a real save receipt before claiming persistence. A request for one draft does not change future preferences. Account permissions, approvals and memory storage belong to the host.

Original workflows are references under `.agents/skills/seo-machine/references/commands/`; slash-command names describe procedures rather than installed executable commands. Specialist procedures are under `references/agents/`. Tool availability is determined by the host. Publication requires an authorized destination and explicit approval.

## Verify

```sh
python3 -m unittest discover -s tests
```

The optional Docker image installs the original provider requirements; the core supplied-text analysis needs only Python 3.11+. Provider-backed workflows require your own account configuration and may incur charges.
