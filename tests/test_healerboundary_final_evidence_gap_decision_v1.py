import hashlib
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.resolve()
DECISION = REPO_ROOT / "docs/experiments/reports/healerboundary_final_evidence_gap_decision_v1.md"
FINAL_REPORT = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

FINAL_REPORT_SHA256 = "d77eb8c4e1d7ccae03e276adb60bbe5f8a71ef38deef6246ae842ed840fe2fdd"
EVIDENCE_COMPLETE_SHA256 = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_single_valid_evidence_gap_decision():
    text = DECISION.read_text(encoding="utf-8")
    decisions = [
        "DECISION 1: NO_ADDITIONAL_EXPERIMENT_REQUIRED_BEFORE_FINAL",
        "DECISION 2: SMALL_CONFIRMATORY_VALIDATION_RECOMMENDED",
        "DECISION 3: ADDITIONAL_EXPERIMENT_REQUIRED_BEFORE_FINAL",
    ]
    assert sum(decision in text for decision in decisions) == 1
    assert "COMPLETE=5" in text
    assert "SUFFICIENT_WITH_LIMITATION=5" in text
    assert "REQUIRED_BEFORE_FINAL=0" in text
    assert "OPTIONAL_FUTURE_WORK=2" in text


def test_decision_preserves_scope_and_formal_accounts():
    text = DECISION.read_text(encoding="utf-8")
    for value in ["Primary=5", "Corrected=6", "231/242", "外部獨立驗證", "不得為增加 rescues"]:
        assert value in text
    assert "已完成跨資料集、跨模型或公開benchmark的外部泛化驗證" not in text.replace(
        "不主張已完成跨資料集、跨模型或公開benchmark的外部泛化驗證", ""
    )


def test_protected_evidence_hashes_unchanged():
    assert sha256(FINAL_REPORT) == FINAL_REPORT_SHA256
    assert sha256(EVIDENCE_COMPLETE) == EVIDENCE_COMPLETE_SHA256
