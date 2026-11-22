"""Analyze supplied text using SEO Machine's existing modules; no provider calls."""

import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data_sources"))
from modules.seo_quality_rater import SEOQualityRater
from modules.search_intent_analyzer import SearchIntentAnalyzer
from modules.content_scrubber import ContentScrubber


def analyze(content, keyword):
    _, scrub = ContentScrubber().scrub(content)
    result = {
        "evidence": "supplied_text",
        "word_count": len(content.split()),
        "quality": SEOQualityRater().rate(content, primary_keyword=keyword),
        "intent": SearchIntentAnalyzer().analyze(keyword),
        "scrubbing_observations": scrub,
        "provider_data": "not_collected",
        "ranking_or_citation_lift_established": False,
    }
    if importlib.util.find_spec("textstat") is None:
        result["readability"] = {"status": "unavailable", "missing_package": "textstat"}
    else:
        from modules.readability_scorer import ReadabilityScorer
        result["readability"] = {"status": "available", "analysis": ReadabilityScorer().analyze(content)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    content = args.article.read_text(encoding="utf-8")
    if not content.strip():
        parser.error("Supply a nonempty article.")
    result = analyze(content, args.keyword)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(json.dumps({"saved": str(args.output), "evidence": result["evidence"]}))


if __name__ == "__main__":
    main()
