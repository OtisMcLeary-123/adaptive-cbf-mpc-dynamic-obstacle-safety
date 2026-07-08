#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import shutil
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


METRICS = [
    "success_rate",
    "collision_rate",
    "control_failure_rate",
    "min_clearance_mean",
    "path_length_mean",
    "completion_time_mean",
    "mean_solve_time_ms",
    "p95_solve_time_ms",
    "solver_failure_rate",
    "infeasible_rate",
    "fallback_rate",
    "collision_after_fallback_rate",
]


def rows_from_summary(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text())
    common = {
        "summary_path": str(path.relative_to(ROOT)),
        "suite": str(path.parent.relative_to(ROOT / "results")) if (ROOT / "results") in path.parents else "",
        "experiment_id": data.get("experiment_id", ""),
        "method": data.get("method", ""),
        "scenario_id": data.get("scenario_id", ""),
        "backend": data.get("backend", "random_shooting"),
        "solver": data.get("solver", ""),
    }
    rows: list[dict[str, Any]] = []
    if "aggregate" in data:
        rows.append({**common, "label": data.get("method", ""), "aggregate": data["aggregate"]})
    for label, item in data.get("results", {}).items():
        rows.append({**common, "label": label, "aggregate": item["aggregate"]})
    return rows


def collect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((ROOT / "results").glob("**/summary.json")):
        if not is_publishable_result(path):
            continue
        rows.extend(rows_from_summary(path))
    return rows


def fmt_ci(aggregate: dict[str, Any], source_key: str) -> str:
    ci_key = {
        "success_rate": "success",
        "collision_rate": "collision",
        "control_failure_rate": "control_failure",
        "min_clearance_mean": "min_clearance",
        "path_length_mean": "path_length",
        "completion_time_mean": "completion_time",
        "mean_solve_time_ms": "mean_solve_time_ms",
        "solver_failure_rate": "solver_failure_rate",
        "infeasible_rate": "infeasible_rate",
        "fallback_rate": "fallback_rate",
        "collision_after_fallback_rate": "collision_after_fallback",
    }[source_key]
    stats = aggregate.get("ci", {}).get(ci_key)
    if not stats:
        return f"{aggregate.get(source_key, '')}"
    low = stats["mean"] - stats["ci95"]
    high = stats["mean"] + stats["ci95"]
    if source_key.endswith("_rate") or source_key in {"success_rate", "collision_rate"}:
        low = max(0.0, low)
        high = min(1.0, high)
    return f"{stats['mean']:.3f} ± {stats['std']:.3f} [{low:.3f}, {high:.3f}]"


def write_summary_tables(rows: list[dict[str, Any]]) -> None:
    out = ROOT / "docs/tables"
    out.mkdir(parents=True, exist_ok=True)
    fieldnames = ["suite", "experiment_id", "scenario_id", "backend", "label", *METRICS, "summary_path"]
    with (out / "summary_metrics.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            agg = row["aggregate"]
            writer.writerow(
                {
                    "suite": row["suite"],
                    "experiment_id": row["experiment_id"],
                    "scenario_id": row["scenario_id"],
                    "backend": row["backend"],
                    "label": row["label"],
                    **{metric: agg.get(metric, "") for metric in METRICS},
                    "summary_path": row["summary_path"],
                }
            )

    with (out / "summary_metrics.md").open("w") as handle:
        handle.write("# Summary Metrics\n\n")
        handle.write("Values are `mean ± std [95% CI]` when per-seed run data is available.\n\n")
        handle.write("| Suite | Experiment | Scenario | Backend | Method | Success | Collision | Infeasible | Fallback | Clearance | Path | Time | Solve |\n")
        handle.write("|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            agg = row["aggregate"]
            handle.write(
                "| {suite} | {experiment} | {scenario} | {backend} | {label} | {success} | {collision} | {infeasible} | {fallback} | {clearance} | {path} | {time} | {solve} |\n".format(
                    suite=row["suite"],
                    experiment=row["experiment_id"],
                    scenario=row["scenario_id"],
                    backend=row["backend"],
                    label=row["label"],
                    success=fmt_ci(agg, "success_rate"),
                    collision=fmt_ci(agg, "collision_rate"),
                    infeasible=fmt_ci(agg, "infeasible_rate"),
                    fallback=fmt_ci(agg, "fallback_rate"),
                    clearance=fmt_ci(agg, "min_clearance_mean"),
                    path=fmt_ci(agg, "path_length_mean"),
                    time=fmt_ci(agg, "completion_time_mean"),
                    solve=fmt_ci(agg, "mean_solve_time_ms"),
                )
            )


def write_scenario_table(rows: list[dict[str, Any]]) -> None:
    out = ROOT / "docs/tables"
    table_rows = [
        row
        for row in rows
        if row["suite"].startswith("extended/scenarios/")
        and row["experiment_id"] == "E6"
        and row["backend"] == "random_shooting"
    ]
    with (out / "scenario_comparison.csv").open("w", newline="") as handle:
        fieldnames = ["scenario_id", "method", "seeds", "success", "collision", "clearance", "path_length", "completion_time", "solve_time"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in table_rows:
            agg = row["aggregate"]
            writer.writerow(
                {
                    "scenario_id": row["scenario_id"],
                    "method": row["label"],
                    "seeds": agg.get("runs", ""),
                    "success": agg.get("success_rate", ""),
                    "collision": agg.get("collision_rate", ""),
                    "clearance": agg.get("min_clearance_mean", ""),
                    "path_length": agg.get("path_length_mean", ""),
                    "completion_time": agg.get("completion_time_mean", ""),
                    "solve_time": agg.get("mean_solve_time_ms", ""),
                }
            )
    with (out / "scenario_comparison.md").open("w") as handle:
        handle.write("# E6 Per-Scenario Comparison\n\n")
        handle.write("| Scenario | Method | Seeds | Success | Collision | Clearance | Path | Time | Solve |\n")
        handle.write("|---|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in table_rows:
            agg = row["aggregate"]
            handle.write(
                "| {scenario} | {method} | {runs} | {success:.2f} | {collision:.2f} | {clearance:.3f} | {path:.3f} | {time:.2f} | {solve:.3f} |\n".format(
                    scenario=row["scenario_id"],
                    method=row["label"],
                    runs=int(agg.get("runs", 0)),
                    success=float(agg.get("success_rate", 0.0)),
                    collision=float(agg.get("collision_rate", 0.0)),
                    clearance=float(agg.get("min_clearance_mean", 0.0)),
                    path=float(agg.get("path_length_mean", 0.0)),
                    time=float(agg.get("completion_time_mean", 0.0)),
                    solve=float(agg.get("mean_solve_time_ms", 0.0)),
                )
            )


def write_paired_delta_table() -> None:
    out = ROOT / "docs/tables"
    table_rows: list[dict[str, Any]] = []
    for summary_path in sorted((ROOT / "results").glob("**/summary.json")):
        if not is_publishable_result(summary_path):
            continue
        data = json.loads(summary_path.read_text())
        if data.get("experiment_id") != "E6" or "results" not in data:
            continue
        adaptive = data["results"].get("Rule adaptive CBF")
        if not adaptive:
            continue
        adaptive_runs = {int(run["seed"]): run for run in adaptive["runs"]}
        for label, item in data["results"].items():
            if not label.startswith("Fixed CBF"):
                continue
            fixed_runs = {int(run["seed"]): run for run in item["runs"]}
            seeds = sorted(set(fixed_runs) & set(adaptive_runs))
            if not seeds:
                continue
            row = {
                "suite": str(summary_path.parent.relative_to(ROOT / "results")),
                "scenario_id": data.get("scenario_id", ""),
                "backend": data.get("backend", "random_shooting"),
                "baseline": label,
                "seeds": len(seeds),
                "summary_path": str(summary_path.relative_to(ROOT)),
            }
            for key, metric in [
                ("delta_success", "success"),
                ("delta_collision", "collision"),
                ("delta_clearance", "min_clearance"),
                ("delta_path_length", "path_length"),
                ("delta_solve_time", "mean_solve_time_ms"),
            ]:
                values = [float(adaptive_runs[s][metric]) - float(fixed_runs[s][metric]) for s in seeds]
                row.update({f"{key}_{k}": v for k, v in mean_std_ci(values).items()})
            table_rows.append(row)

    fieldnames = [
        "suite",
        "scenario_id",
        "backend",
        "baseline",
        "seeds",
        "delta_success_mean",
        "delta_success_std",
        "delta_success_ci95",
        "delta_collision_mean",
        "delta_collision_std",
        "delta_collision_ci95",
        "delta_clearance_mean",
        "delta_clearance_std",
        "delta_clearance_ci95",
        "delta_path_length_mean",
        "delta_path_length_std",
        "delta_path_length_ci95",
        "delta_solve_time_mean",
        "delta_solve_time_std",
        "delta_solve_time_ci95",
        "summary_path",
    ]
    with (out / "paired_delta.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table_rows)

    with (out / "paired_delta.md").open("w") as handle:
        handle.write("# E6 Paired Delta Table\n\n")
        handle.write("Deltas are matched by seed and computed as `Rule adaptive CBF - fixed baseline`.\n\n")
        handle.write("| Suite | Scenario | Backend | Baseline | Seeds | Δsuccess | Δcollision | Δclearance | Δpath length | Δsolve time |\n")
        handle.write("|---|---|---|---|---:|---:|---:|---:|---:|---:|\n")
        for row in table_rows:
            handle.write(
                "| {suite} | {scenario} | {backend} | {baseline} | {seeds} | {success} | {collision} | {clearance} | {path} | {solve} |\n".format(
                    suite=row["suite"],
                    scenario=row["scenario_id"],
                    backend=row["backend"],
                    baseline=row["baseline"],
                    seeds=row["seeds"],
                    success=fmt_mean_ci(row, "delta_success"),
                    collision=fmt_mean_ci(row, "delta_collision"),
                    clearance=fmt_mean_ci(row, "delta_clearance"),
                    path=fmt_mean_ci(row, "delta_path_length"),
                    solve=fmt_mean_ci(row, "delta_solve_time"),
                )
            )


def copy_key_figures() -> None:
    out = ROOT / "docs/figures/extended"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    overlay_paths = [
        path for path in sorted((ROOT / "results").glob("**/figures/seed_000_overlay.png"))
        if is_publishable_result(path)
    ]
    clearance_paths = [
        path for path in sorted((ROOT / "results").glob("**/figures/seed_000_clearance_curve.png"))
        if is_publishable_result(path)
    ]
    for path in overlay_paths[:20]:
        target = out / f"{figure_prefix(path)}_trajectory.png"
        shutil.copy(path, target)
    for path in clearance_paths[:20]:
        target = out / f"{figure_prefix(path)}_clearance.png"
        shutil.copy(path, target)


def write_paper_section(rows: list[dict[str, Any]]) -> None:
    e6_rows = [row for row in rows if row["suite"] == "paper_main/e6_adaptive_50_seed"]
    out = ROOT / "docs/paper_section_results.md"
    with out.open("w") as handle:
        handle.write("# Block B Results Section Draft\n\n")
        handle.write("## Experimental Setup\n\n")
        handle.write(
            "Block B evaluates non-LLM adaptive CBF baselines on the same dynamic obstacle point-mass task as Block A. "
            "E5 compares obstacle prediction assumptions, and E6 compares fixed CBF gamma values against a rule-adaptive CBF controller.\n\n"
        )
        handle.write("## E6 Main Comparison\n\n")
        if e6_rows:
            handle.write("| Method | Runs | Success | Collision | Clearance | Solve time |\n")
            handle.write("|---|---:|---:|---:|---:|---:|\n")
            for row in e6_rows:
                agg = row["aggregate"]
                handle.write(
                    "| {label} | {runs} | {success:.3f} | {collision:.3f} | {clearance:.3f} | {solve:.3f} |\n".format(
                        label=row["label"],
                        runs=int(agg.get("runs", 0)),
                        success=float(agg.get("success_rate", 0.0)),
                        collision=float(agg.get("collision_rate", 0.0)),
                        clearance=float(agg.get("min_clearance_mean", 0.0)),
                        solve=float(agg.get("mean_solve_time_ms", 0.0)),
                    )
                )
            handle.write("\n")
        handle.write(
            "The paired-delta table reports matched-seed changes from each fixed gamma baseline to the rule-adaptive CBF controller.\n\n"
        )
        handle.write("## Tables\n\n")
        handle.write("See `docs/tables/summary_metrics.md`, `docs/tables/scenario_comparison.md`, and `docs/tables/paired_delta.md`.\n\n")
        handle.write("## Reproducibility\n\n")
        handle.write("Run `scripts/reproduce_all.sh` to regenerate Block B paper outputs.\n")


def mean_std_ci(values: list[float]) -> dict[str, float]:
    mean = sum(values) / len(values)
    if len(values) <= 1:
        return {"mean": mean, "std": 0.0, "ci95": 0.0}
    std = math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))
    return {"mean": mean, "std": std, "ci95": 1.96 * std / math.sqrt(len(values))}


def fmt_mean_ci(row: dict[str, Any], prefix: str) -> str:
    return f"{float(row[f'{prefix}_mean']):.3f} ± {float(row[f'{prefix}_ci95']):.3f}"


def figure_prefix(path: Path) -> str:
    run_dir = path.parent.parent
    parts = run_dir.relative_to(ROOT / "results").parts
    return "_".join(parts[-2:]) if len(parts) >= 2 else parts[0]


def is_publishable_result(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts if path.is_relative_to(ROOT) else path.parts
    if "checks" in parts:
        return False
    try:
        result_parts = path.relative_to(ROOT / "results").parts
    except ValueError:
        return True
    if result_parts and result_parts[0] in {"exp_e5", "exp_e6"}:
        return False
    return True


def main() -> None:
    rows = collect_rows()
    write_summary_tables(rows)
    write_scenario_table(rows)
    write_paired_delta_table()
    copy_key_figures()
    write_paper_section(rows)
    print(f"Wrote {len(rows)} Block B table rows.")


if __name__ == "__main__":
    main()
