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
    "1703fe292ff1809e92d2ff48f47e06de": ("docs/phase-for-character-control.md", "Phase for character control"),
    "1723fe292ff18053ade0d7afa6c0328a": ("docs/paper-writing/writing-flow-example.md", "Examples of writing flow"),
    # Newly accessible (May 2026 reprobe) — re-fetched after fixing the URL-vs-ID lookup
    "1053fe292ff18015b2f3cde4498a5f0f": ("docs/getting-advanced/natural-science-definition.md", "Defining natural science: maths vs science"),
    "1053fe292ff180b59bbfe55c0961a796": ("docs/getting-advanced/clean-code.md", "Clean code"),
    "1143fe292ff180feb5d0fe76d05e085b": ("docs/paper-writing/copilot-and-gpt-for-english-writing.md", "Using Copilot and GPT to support English writing"),
    "1293fe292ff180bfa5deeed526821d78": ("docs/paper-writing/revising-paper-writing.md", "How to revise paper writing"),
    "1363fe292ff1805b84a6c97e3601ac4d": ("docs/getting-advanced/broad-paper-survey-importance.md", "Why doing a broad, self-directed paper survey matters"),
    "13f822dc3a5e4242ab1282789a47c346": ("docs/getting-advanced/help-from-senior-researchers.md", "Getting help from senior researchers more effectively"),
    "1533fe292ff18090ba8bd603b4fcf64e": ("docs/getting-started/should-you-do-research.md", "Whether to do research and how to choose a direction"),
    "1773fe292ff1802ebb83c2baaae5529d": ("docs/getting-advanced/good-work-state.md", "What a good working state looks like"),
    "1fa3fe292ff1807e98c5e3513045cbab": ("docs/getting-advanced/research-taboos.md", "What things are taboo in research"),
    "24f2a9617d2f475c9be20139d5c49a1a": ("docs/getting-advanced/learning-paper-code.md", "How to learn the code of a paper or algorithm"),
    "27409ef7cd1c4e7d8b6365cd732348e2": ("docs/getting-advanced/search-skills-for-research.md", "Why search skills matter for research"),
    "2863fe292ff180759413f51ed1d1fdc3": ("docs/getting-advanced/minimum-viable-exploratory-experiments.md", "Exploratory experiments should follow minimum viability"),
    "2d01e7e2a36f4860acc655c78c57cf4f": ("docs/getting-advanced/mental-fatigue.md", "What mental fatigue is and how to handle it"),
    "2d4db9a1e86346068ecb59bb57c0f9fd": ("docs/getting-advanced/solving-method-design-pitfalls.md", "Failures in the solving-method-design phase and how to avoid them"),
    "31d3fe292ff1801a97aceb84f067a0ed": ("docs/getting-advanced/goal-management.md", "The role of goal management in research and life"),
    "33275442af8d40fb9d09b335106a8595": ("docs/getting-advanced/project-page.md", "How to make a project page"),
    "4a4a6aa51614420eb146e8cf82c32bd4": ("docs/getting-advanced/research-taste.md", "How to cultivate research taste"),
    "4db27521e7014e7a925a0f07e4f5c80f": ("docs/getting-started/undergrad-vs-grad-education.md", "Undergraduate vs graduate education"),
    "5828f74458ee4e3fa32c20100c6855ec": ("docs/getting-advanced/discussion-importance.md", "Why discussion and conversation matter for research"),
    "5dae86dfa4b0446fbe69c490e1165815": ("docs/paper-writing/paper-writing-pitfalls.md", "Problems in the paper-writing phase and how to avoid them"),
    "849f6606e5fb49b5b73a3778de64e43e": ("docs/getting-advanced/designing-exploratory-experiments.md", "Given an idea, how to design exploratory experiments"),
    "8beb455efdd54cf8bc6de579bca3c211": ("docs/getting-advanced/classic-code-bug-causes.md", "Some classic causes of code bugs"),
    "afe9ef02def04f6f992d0ad6070076ce": ("docs/getting-advanced/exploratory-experiment-pitfalls.md", "Problems in the exploratory-experiment phase and how to avoid them"),
    "b3697365df674503b38e8265489fb336": ("docs/getting-started/joining-the-lab-pitfalls.md", "Common problems when joining a new lab and how to avoid them"),
    "c5549978134a4b348a49fc387c500578": ("docs/getting-started/getting-to-know-labmates.md", "How to get to know your labmates after joining the lab"),
    "e5cc4f108cc4414d82abbf7b8e31dfae": ("docs/getting-advanced/first-principles-method-design.md", "Designing methods from first principles"),
    "e94fd42c49614acc98d8457cf00d5903": ("docs/getting-advanced/impactful-work.md", "How to produce impactful work"),
    "ff09e6f41b394f56835591db70b4980f": ("docs/getting-advanced/bad-student-mindsets.md", "Student mindsets that don't suit research"),
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
