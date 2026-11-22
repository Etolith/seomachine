# SEO Machine workspace

This fork adapts TheCraigHewitt/seomachine for Codex and portable Agent Skills.
The main workflow is `.agents/skills/seo-machine/SKILL.md`; the adjacent folders
contain the existing marketing skills. Read the relevant skill and references.

Run Python helpers by their skill-directory path, with the user's workspace as
the working directory. Customer context and generated files belong to that
workspace, never inside the installed skill. Do not fill brand templates with
invented customer facts. Ask for missing facts or use explicitly saved context.

Inspect readiness before provider-dependent work. Missing credentials or packages
are setup blockers, not empty analytics results. Use approved connected tools
when available; a downloaded skill grants no account access. Confirm the scope
and allowance before charged provider calls. External publishing requires the
owner's approval of the destination and content.

Heuristic content scores do not establish ranking, citation visibility or lift.
Run `python3 -m unittest discover -s tests` after changing Python behavior.
