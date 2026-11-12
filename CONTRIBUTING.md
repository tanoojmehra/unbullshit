# Contributing

Unbullshit is a public, instruction-only skill collection. Contribute improvements supported by a specific user problem, rather than by adding process for its own sake.

## Small contribution loop

1. Report the exact scenario, prompt, host and observed failure (redact private material).
2. Explain the desired outcome and how a change would help.
3. Make a focused edit. Keep the four skills independently installable and preserve real safety and correctness requirements.
4. Add or update a [machine-readable behavioral scenario](tests/behavioral/cases.json) and the relevant [manual scenario](tests/scenarios.md) when useful.
5. Run the checks and state what still needs a real host or model test.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

For recordkeeping changes, follow the [record format and location precedence](docs/recordkeeping.md), add a scenario or test in [tests/test_recordkeeping.py](tests/test_recordkeeping.py), and ensure existing registers are never silently overwritten or duplicated. Documents must not become a permission authority or mandatory task ledger.

For new demonstrations, label authored examples as **illustrative** and link their benchmark case. Only call a comparison **reproduced** if raw model inputs, outputs, settings, runs and evaluation criteria are saved. Call it a **real-world case study** only with permission and anonymized evidence. Never invent adoption numbers or performance gains. See [benchmarking](docs/benchmarking.md).

For behavioral changes, test the same prompt with and without the skill where possible. Include counterexamples where a complex solution is justified. A passing structural check isn't proof of better agent judgment.

A good PR describes: original failure, intended behavior, minimal change, tests, and what could be harmed by excessive simplification. No mandatory agents, new runtime dependencies, telemetry, or permission policies.

Contributions are under the repository's [MIT license](LICENSE).
