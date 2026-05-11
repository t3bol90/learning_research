#!/usr/bin/env python3
"""One-shot: walk the manifest and assign English slug + target_path for every
ok page, then refresh image final_path entries.

Edit MAPPING below if a slug or location needs adjusting.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / ".notion-cache" / "manifest.json"

# id -> (relative target path under repo root, English title for index)
MAPPING = {
    # Depth 0 - main seeds
    "1713fe292ff1808eb33be93ea2d79ad9": ("docs/sebastian-starke.md", "A model PhD student: Sebastian Starke"),
    "b43507ef26d044bd888ac29f4736e116": ("docs/research-project.md", "How to do a research project"),
    "c13c7e52aab64c1a8e3576b97fcb9851": ("docs/paper-writing/practising.md", "How to practise paper writing"),
    "c1a22465a0fa4b15a12985223916048e": ("docs/paper-writing/template.md", "Paper writing template"),
    "74aef88b9187439fa4e301704f6eb49a": ("docs/paper-writing/high-level-researchers.md", "Writing experience from high-level researchers"),
    "af99ce47103e4917b6a5bd1fd4b3c022": ("docs/rebuttal.md", "How to do a rebuttal"),
    "810f02670691444f8c94cc3d5b76dcbc": ("docs/academic-talk-slides.md", "How to make slides for an academic talk"),
    "8911dcc5922b4442a80d4407926e65bf": ("docs/getting-started/stage-two-study-plan-example.md", "Stage-two study plan example"),
    "59569d7b66954578b21bf1dc6ea35776": ("docs/getting-started/common-tools-and-configs.md", "Common tools and configurations"),
    "a3fe9f17b8af46558cd1112627009c83": ("docs/getting-started/mental-prep-stage-three.md", "Mental preparation for stage three"),
    "da6ce171c13846b7a7ffaa7473ffa6ea": ("docs/getting-advanced/coming-up-with-ideas.md", "How to build the ability to come up with ideas"),
    "d192db870bc64436ae4a4a590b36772a": ("docs/getting-advanced/reading-papers.md", "How to read papers effectively"),
    "d697ef578d784c869d4f8314f0d617da": ("docs/getting-advanced/weekly-meeting-slides.md", "Weekly meeting slides"),
    "1aee6e718de6472f834d13da8f4ff097": ("docs/getting-advanced/why-experiment-isnt-working.md", "How to find out why an experiment isn't working"),
    "caf34717f4c046c69ee7e14ea953c46f": ("docs/getting-advanced/keeping-experiment-notes.md", "How to write experiment notes"),
    "c278dab7e4764d61a92c1fd1ef3135b1": ("docs/find-papers.md", "How to find papers"),
    "1753fe292ff180948215cf82cd2b30ae": ("docs/project-core-technical-problem-analysis.md", "Project core technical problem analysis template"),
    "1d13fe292ff180de91afcb7f2eb57b69": ("docs/interview-questions-reflection.md", "Reflecting on research from interview questions"),
    # Depth 1 - children
    "1b69debf803a4c268fc8a09a9a748bbf": ("docs/debug.md", "How to debug an algorithm or code"),
    "2bd4d371117a45e1af4021ccc25e0515": ("docs/paper-writing/figures-template.md", "Paper figure template"),
    "492bf030bc8a48fcbe9dfd1a246678b1": ("docs/getting-advanced/experiment-notes-example-march-24.md", "Experiment notes example: 24 March"),
    "903b997097d343dbaba6d5e0780eab0f": ("docs/distilling-knowledge-from-mentors.md", "Extracting knowledge from supervisors and senior students"),
    "997f611cd2e24ef1a62210ff099948e2": ("docs/designing-solutions.md", "Improving your ability to design solutions"),
    "a7b846d0082b458e8eb366f506f10182": ("docs/getting-advanced/experiment-notes-template.md", "Experiment notes template"),
    "d820794145a041be9599e45dc0cdb3b5": ("docs/demos-and-applications.md", "How to make appealing demos and applications"),
    "d9c6556326e84962a2d7ae190e2705af": ("docs/idea-vs-goal-driven-research.md", "Idea-driven vs goal-driven research"),
    "eed9ed1e9dc44a1c9437b114e6d5d9fd": ("docs/paper-writing/reviewing-papers.md", "How to review papers"),
    "f1e4f77f0f3943e39dd1210bd3fe71ea": ("docs/ppt-layout-and-design.md", "PPT layout and design"),
    "f8b36e484b344a2893a94e4608b72ec2": ("docs/literature-tree.md", "How to build a literature tree"),
    # Depth 2 - grand-children
    "456746ed8fd24cf38d301b7f4144f70d": ("docs/checking-module-outputs.md", "Are the intermediate outputs of each module what you expect?"),
    "4be609919b914b7587a5477bddc83001": ("docs/ten-classic-experiment-questions.md", "Ten classic questions for analysing experimental results"),
    "55fde3b6317f4660b72e90ce790f13e5": ("docs/specific-approach.md", "A specific approach"),
    "85a701d9f0c34d03a9f7cdebf71b3f47": ("docs/paper-writing/adversarial-writing.md", "Adversarial writing: review your own paper"),
    "ae78ad320d314bc5859f572e26e143a7": ("docs/planning-research-direction.md", "Planning a general goal and roadmap for a research direction"),
    "b0e7940f3b8b4a3e951ec672eaf4632e": ("docs/paper-writing/experiments.md", "Writing the Experiments section"),
    "b89f47bc35da4a3ca1bed59616f11189": ("docs/idea-generation-process.md", "A specific process for coming up with ideas (goal-driven research)"),
    "c8013937e2c24dfab39695cf05d70101": ("docs/which-applications-demos.md", "Which applications and demos to make"),
    "cd9c4f2e0cb147ab9e1e1c98dc1a5055": ("docs/paper-writing/figures.md", "Drawing figures for the paper"),
}


def main() -> None:
    m = json.load(MANIFEST.open("r", encoding="utf-8"))
    pages = m["pages"]
    missing_in_mapping = []
    for pid, page in pages.items():
        if page.get("fetch_status") != "ok":
            continue
        if pid not in MAPPING:
            missing_in_mapping.append((pid, page.get("title_zh", "")))
            continue
        target, title_en = MAPPING[pid]
        page["target_path"] = target
        page["title_en"] = title_en
        page["slug"] = Path(target).stem
        # Recompute image final paths.
        if page.get("images"):
            target_dir = Path(target).parent
            for img in page["images"]:
                img["final_path"] = str(
                    target_dir / "assets" / page["slug"] / f"{img['index']:03d}{img['ext']}"
                )
    json.dump(m, MANIFEST.open("w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    print(f"Assigned targets for {sum(1 for p in pages.values() if p.get('target_path'))} pages")
    if missing_in_mapping:
        print(f"WARNING: {len(missing_in_mapping)} ok pages without a mapping entry:")
        for pid, t in missing_in_mapping:
            print(f"  {pid}  {t!r}")
    else:
        print("All ok pages mapped.")


if __name__ == "__main__":
    main()
