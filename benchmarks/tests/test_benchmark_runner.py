from pathlib import Path

import benchmark_runner as br


def test_load_results_reads_numeric_and_list_payloads(tmp_path: Path):
    commit = "1234567890abcdef"
    machine_dir = tmp_path / "bench-runner"
    machine_dir.mkdir()
    result_file = machine_dir / f"{commit[:8]}-env.json"
    result_file.write_text(
        """
{
  "results": {
    "bench_a": {"result": 1.25},
    "bench_b": {"result": [2.5, null]},
    "bench_c": {"result": [null, 3.75]}
  }
}
""".strip()
    )

    loaded = br.load_results(tmp_path, commit)

    assert loaded == {"bench_a": 1.25, "bench_b": 2.5, "bench_c": 3.75}


def test_load_results_no_files_returns_empty_dict(tmp_path: Path):
    commit = "abcdef123456"

    loaded = br.load_results(tmp_path, commit)

    assert loaded == {}


def test_load_results_ignores_invalid_entries(tmp_path: Path):
    commit = "abcdef123456"
    machine_dir = tmp_path / "bench-runner"
    machine_dir.mkdir()
    result_file = machine_dir / f"{commit[:8]}-env.json"
    result_file.write_text(
        """
{
  "results": {
    "bench_a": {"result": "invalid"},
    "bench_b": {"result": null}
  }
}
""".strip()
    )

    loaded = br.load_results(tmp_path, commit)

    assert loaded == {}


def test_run_asv_builds_expected_command(monkeypatch):
    seen = {}

    def fake_run(cmd, check, **kwargs):
        seen["cmd"] = cmd
        seen["check"] = check

    monkeypatch.setattr(br.subprocess, "run", fake_run)

    br.run_asv("HEAD", "asv.conf.json", Path("results"), machine="bench-host", bench="solve.*")

    assert seen["check"] is True
    assert len(seen["cmd"]) > 0
    assert seen["cmd"] == [
        "asv",
        "run",
        "--quick",
        "--config",
        "asv.conf.json",
        "--results-dir",
        "results",
        "--machine",
        "bench-host",
        "--bench",
        "solve.*",
        "HEAD^!",
    ]