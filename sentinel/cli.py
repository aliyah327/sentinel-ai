"""Sentinel-AI command-line interface.

Subcommands (mirrors the Promptfoo/Garak feel):
  sentinel list-strategies         show available strategies (buffs)
  sentinel list-probes   -c CONF   show the probes a config will run
  sentinel validate      -c CONF   check a config loads and is well-formed
  sentinel run           -c CONF   run the evaluation and write reports

Run with no model installed and it uses the mock target, so it always works.
Point it at Ollama with:  sentinel run -c config.yaml --model llama3.2
"""

import argparse
import sys

from . import __version__
from .config import load_config, apply_overrides
from .targets import build_target
from .probes import STRATEGIES, load_probes
from .evaluators import Evaluator
from .reporting import write_json, write_html


def _cmd_list_strategies(args):
    print("Available strategies (buffs):")
    for name in STRATEGIES:
        print(f"  - {name}")


def _cmd_list_probes(args):
    config = load_config(args.config)
    for p in load_probes(config):
        print(f"  [{p['category']}] {p['id']}: {p['intent']}")


def _cmd_validate(args):
    config = load_config(args.config)
    config = apply_overrides(config, args)
    probes = load_probes(config)
    strategies = config.get("strategies", [])
    unknown = [s for s in strategies if s not in STRATEGIES]
    if unknown:
        print(f"INVALID: unknown strategies {unknown}")
        sys.exit(1)
    print("Config OK.")
    print(f"  target     : {config['target'].get('type')}")
    print(f"  probes     : {len(probes)}")
    print(f"  strategies : {', '.join(strategies)}")
    print(f"  repeat     : {config.get('repeat', 3)}")
    print(f"  total cases: {len(probes) * len(strategies) * int(config.get('repeat', 3))}")


def _cmd_run(args):
    config = load_config(args.config)
    config = apply_overrides(config, args)
    target = build_target(config["target"])

    print(f"Running Sentinel-AI against target: {getattr(target, 'name', '?')}")

    def progress(case):
        mark = "FAIL(leak)" if case.failed else "ok"
        print(f"  [{mark:>10}] {case.probe_id} / {case.strategy} #{case.repetition}")

    evaluator = Evaluator(target, config)
    try:
        result = evaluator.run(progress=progress)
    except RuntimeError as exc:
        print(f"\nERROR: {exc}")
        sys.exit(2)

    json_path = write_json(result, args.json)
    html_path = write_html(result, args.html)

    s = result.summary()
    print("\n=== Summary ===")
    print(f"  total cases     : {s['total_cases']}")
    print(f"  attacks succeeded: {s['total_successes']}")
    print(f"  overall ASR     : {s['overall_asr']*100:.1f}%")
    print(f"\nReports written:\n  {json_path}\n  {html_path}")


def build_parser():
    p = argparse.ArgumentParser(
        prog="sentinel",
        description="Sentinel-AI: a small, auditable LLM guardrail red-teaming tool.",
    )
    p.add_argument("--version", action="version", version=f"sentinel {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("list-strategies", help="list available strategies")
    sp.set_defaults(func=_cmd_list_strategies)

    sp = sub.add_parser("list-probes", help="list probes for a config")
    sp.add_argument("-c", "--config", required=True)
    sp.set_defaults(func=_cmd_list_probes)

    sp = sub.add_parser("validate", help="validate a config")
    sp.add_argument("-c", "--config", required=True)
    _common_overrides(sp)
    sp.set_defaults(func=_cmd_validate)

    sp = sub.add_parser("run", help="run the evaluation")
    sp.add_argument("-c", "--config", required=True)
    sp.add_argument("--json", default="reports/report.json", help="JSON output path")
    sp.add_argument("--html", default="reports/report.html", help="HTML output path")
    _common_overrides(sp)
    sp.set_defaults(func=_cmd_run)
    return p


def _common_overrides(sp):
    sp.add_argument("--target", choices=["mock", "ollama"], help="override target type")
    sp.add_argument("--model", help="Ollama model name (implies --target ollama)")
    sp.add_argument("--repeat", type=int, help="repetitions per case")
    sp.add_argument("--strategies", help="comma list, e.g. plain,base64,rot13,leetspeak")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
