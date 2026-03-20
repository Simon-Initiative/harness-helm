from __future__ import annotations

import re

from helm.models import CapabilityRequirement, CapabilitySummary


HEADING_PATTERN = re.compile(r"^(#{2,6})\s+(.*\S)\s*$")

CAPABILITY_RULES = {
    "feature_flags": {
        "positive": ("feature flag", "feature flags"),
        "negative": ("no feature flag", "no feature flags", "without feature flags"),
        "sections": ("11. feature flagging, rollout & migration",),
    },
    "telemetry": {
        "positive": ("telemetry", "observability", "analytics", "appsignal", "event"),
        "negative": (),
        "sections": (
            "8. non-functional requirements",
            "12. analytics & success metrics",
            "13. risks & mitigations",
        ),
    },
    "performance_requirements": {
        "positive": ("performance", "latency", "throughput", "p95", "benchmark", "rate limit"),
        "negative": ("no load or performance testing requirements",),
        "sections": (
            "8. non-functional requirements",
            "12. analytics & success metrics",
            "16. qa plan",
        ),
    },
}


def parse_capabilities_from_prd(prd_text: str) -> CapabilitySummary:
    normalized_text = prd_text.lower()
    sections = split_sections(prd_text)
    items: list[CapabilityRequirement] = []

    for name, rule in CAPABILITY_RULES.items():
        evidence = capability_evidence(normalized_text, sections, rule["positive"], rule["sections"])
        negative_hits = capability_negative_hits(normalized_text, sections, rule["negative"], rule["sections"])
        items.append(
            CapabilityRequirement(
                name=name,
                required=bool(evidence) and not bool(negative_hits),
                evidence=negative_hits or evidence,
            )
        )

    return CapabilitySummary(items=items)


def split_sections(prd_text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "_root"
    sections[current] = []
    for raw_line in prd_text.splitlines():
        match = HEADING_PATTERN.match(raw_line.strip())
        if match:
            current = match.group(2).strip().lower()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(raw_line)
    return {key: "\n".join(value).lower() for key, value in sections.items()}


def capability_evidence(
    full_text: str,
    sections: dict[str, str],
    positive_terms: tuple[str, ...],
    target_sections: tuple[str, ...],
) -> list[str]:
    evidence: list[str] = []
    for section_name in target_sections:
        section_body = sections.get(section_name, "")
        for term in positive_terms:
            if term in section_body:
                evidence.append(f"{section_name}: {term}")
    if evidence:
        return evidence
    return [term for term in positive_terms if term in full_text]


def capability_negative_hits(
    full_text: str,
    sections: dict[str, str],
    negative_terms: tuple[str, ...],
    target_sections: tuple[str, ...],
) -> list[str]:
    hits: list[str] = []
    for section_name in target_sections:
        section_body = sections.get(section_name, "")
        for term in negative_terms:
            if term in section_body:
                hits.append(f"{section_name}: {term}")
    if hits:
        return hits
    return [term for term in negative_terms if term in full_text]
