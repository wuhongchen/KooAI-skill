# KooAI Skills

Public, reusable skills for KooAI market research and ecommerce analysis.

## Included skills

| Skill | Purpose |
| --- | --- |
| `kooai-selection-standalone` | Use authenticated KooAI MCP data to analyze Coupang categories, products and reviews; screen opportunities with a seven-gate funnel; then create a local, filterable and exportable report. |

## Install a skill

Clone this repository and copy the desired directory into your Codex skills folder:

```bash
git clone https://github.com/wuhongchen/KooAI-skill.git
python3 KooAI-skill/skills/kooai-selection-standalone/scripts/install.py --dry-run
python3 KooAI-skill/skills/kooai-selection-standalone/scripts/install.py
```

Restart or open a new Codex session after installation. Invoke the first skill with `$kooai-selection-standalone`.

## Data and security boundary

- KooAI MCP is the data source; skills must not embed, print or persist API keys, OAuth tokens, cookies or database credentials.
- The standalone selection skill consumes authenticated Coupang market data and writes only credential-free report snapshots to a local loopback page.
- 1688/Ego checks are explicit candidate-level follow-up actions. A displayed 1688 price is a sourcing lead, not a confirmed procurement cost.

## Repository layout

```text
skills/<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/
```

New public skills should be self-contained, include no private project data, and follow the same layout.

## License

MIT. See [LICENSE](LICENSE).
