#!/usr/bin/env python3
"""Enforce World port phase-order and owner-approval ledger, without network access.

Passing CI validates JSON/approval-field syntax only, not the authenticity of
claimed proofs or of an approval. Human review and GitHub protection are required.
"""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PHASES = [f"P{i:02d}" for i in range(13)]
OPEN = {"ACTIVE", "AWAITING_APPROVAL", "BLOCKED"}
STATES = OPEN | {"LOCKED", "APPROVED"}
OWNER = "VegettoSan"
REPO = "Hungry-Shark-World-Ps-Vita"
SOURCE = "Hungry Shark World 2.9.0 (Unity 2017.1.2p4, Mono)"
APK = "6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d"
OBB = "c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72"
APPROVAL_LINK = re.compile(
    rf"^https://github\.com/{OWNER}/{REPO}/(issues|pull)/[0-9]+"
    r"(?:#issuecomment-[0-9]+|#discussion_r[0-9]+|/files)?$"
)
UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def fail(msg):
    raise ValueError(msg)


def validate_identity(data):
    expected = {
        "schema_version": 1,
        "game": "Hungry Shark World",
        "android_package": "com.ubisoft.hungrysharkworld",
        "source_version": "2.9.0",
        "source_version_code": 132,
        "source_unity": "2017.1.2p4",
        "source_backend": "Mono",
        "source_apk_sha256": APK,
        "source_obb_filename": "main.132.com.ubisoft.hungrysharkworld.obb",
        "source_obb_sha256": OBB,
        "target_editor": "2018.2.19f1",
        "target_platform": "PSP2",
        "display_name": "Hungry Shark World Vita",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(f"config/port_identity.json: {key} mismatch")
    title = data.get("title_id")
    if title is None:
        if data.get("planned_install_directory") is not None:
            fail("Do not invent Vita install directory while title ID is unchosen")
        if data.get("identity_status") != "PENDING_OWNER_SELECTION":
            fail("Unchosen Vita title ID needs PENDING_OWNER_SELECTION")
    else:
        if not isinstance(title, str) or not re.fullmatch(r"[A-Z0-9]{9}", title):
            fail("Vita title ID must contain exactly 9 uppercase alphanumerics")
        if title == "HGSKE1178":
            fail("Do not reuse the separate Evolution Vita Title ID")
        if data.get("planned_install_directory") != f"ux0:app/{title}/":
            fail("PS Vita install directory must match World title ID")
        if data.get("identity_status") != "OWNER_APPROVED":
            fail("Title ID must be explicitly approved by repository owner")


def validate_ledger(data):
    if data.get("schema_version") != 1 or data.get("application") != SOURCE:
        fail("Wrong phase schema/game identity")
    if data.get("baseline_apk_sha256") != APK or data.get("baseline_obb_sha256") != OBB:
        fail("Wrong versionCode 132 source-pair hashes")
    phases = data.get("phases")
    if not isinstance(phases, list) or [x.get("id") for x in phases] != PHASES:
        fail("Exactly ordered P00-P12 phases are required")
    open_phase = None
    seen_unfinished = False
    approved = 0
    for p in phases:
        pid = p["id"]
        state = p.get("status")
        refs = p.get("evidence")
        auth = [p.get(k) for k in ("approved_by", "approved_at", "approval_reference")]
        if state not in STATES:
            fail(f"{pid}: invalid status {state!r}")
        if not isinstance(refs, list) or any(not isinstance(r, str) or not r.strip() for r in refs):
            fail(f"{pid}: evidence must be a list of nonempty strings")
        if state == "APPROVED":
            if seen_unfinished:
                fail(f"{pid}: cannot approve after unfinished phase")
            if len(refs) < 2 or len(set(refs)) < 2:
                fail(f"{pid}: needs two distinct evidence references")
            if auth[0] != OWNER or not isinstance(auth[1], str) or not UTC.fullmatch(auth[1]):
                fail(f"{pid}: requires {OWNER} and a UTC approval timestamp")
            try:
                datetime.datetime.strptime(auth[1], "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                fail(f"{pid}: malformed UTC approval date")
            if not isinstance(auth[2], str) or not APPROVAL_LINK.fullmatch(auth[2]):
                fail(f"{pid}: owner GitHub issue/PR approval link missing")
            approved += 1
        elif state in OPEN:
            if seen_unfinished:
                fail(f"{pid}: only the first unfinished phase can be open")
            seen_unfinished = True
            open_phase = pid
            if any(x is not None for x in auth):
                fail(f"{pid}: incomplete phase cannot have approval fields")
        else:
            if not seen_unfinished:
                fail(f"{pid}: phase locked before the first open phase")
            if refs or any(x is not None for x in auth):
                fail(f"{pid}: locked phase cannot carry evidence or approval")
    expected = open_phase if seen_unfinished else "COMPLETE"
    if data.get("current_phase") != expected:
        fail(f"current_phase must be {expected}")
    print(f"PHASE GATES OK: current={expected}; approved={approved}/13")


def main():
    try:
        identity = json.loads((ROOT / "config/port_identity.json").read_text(encoding="utf-8"))
        ledger = json.loads((ROOT / "docs/PHASE_GATES.json").read_text(encoding="utf-8"))
        validate_identity(identity)
        validate_ledger(ledger)
        print("WORLD IDENTITY OK: 2.9.0/132 Unity 2017 Mono, PSP2 title pending")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"PHASE GATES ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
