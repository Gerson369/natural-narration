#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quick_validate.py - natural-narration Skill package + capability checks.

Usage:
  python3 scripts/quick_validate.py <skill_root>
"""

import os
import re
import sys

REQUIRED_FILES = [
    "scripts/nn_blueprint_check.py",
    "references/reveal-beats.md",
    "tests/first-draft/clothes-origin/blueprint.md",
    "tests/first-draft/clothes-origin/blueprint-topic-thread.md",
    "tests/first-draft/clothes-origin/GREEN-first-draft.txt",
    "tests/first-draft/clothes-origin/RED-topic-list.txt",
    "references/first-draft-blueprint.md",
    "references/topic-templates.md",
    "references/self-review-loop.md",
    "references/line-protection.md",
    "tests/first-draft/ancient-games/blueprint.md",
    "tests/first-draft/ancient-games/protect.txt",
    "tests/first-draft/fidelity-fp/before.txt",
    "SKILL.md", "README.md", "VERSION.md", "CHANGELOG.md",
    "agents/openai.yaml",
    "scripts/nn_scan.py", "scripts/quick_validate.py",
    "references/anti-cliche-patterns.md",
    "references/syntax-pattern-detection.md",
    "references/natural-narration-model.md",
    "references/rhythm-rules.md",
    "references/anti-overcorrection.md",
    "references/scan-and-scoring.md",
    "references/before-after-examples.md",
    "references/failure-modes.md",
    "references/workflow.md",
    "references/quality-checklist.md",
    "references/story-engine.md",
    "references/audience-problem-scene.md",
    "references/value-chain.md",
    "references/clarity-engine.md",
    "references/practical-value-router.md",
    "references/voice-profiles.md",
    "references/expression-assets.md",
    "references/evidence-led-narration.md",
    "references/present-day-echo.md",
    "references/critical-documentary.md",
    "references/semantic-fidelity.md",
    "references/file-mode.md",
    "references/author-voice-match.md",
    "references/register-router.md",
    "scripts/nn_structure_check.py",
    "templates/write-output-template.md",
    "templates/clean-output-template.md",
    "templates/scan-report-template.md",
    "tests/test-cases.md", "tests/RESULTS.md",
]

SYNTAX_IDS = [
    "Expectation", "Reversal", "Question", "Suspense Cue", "Host Transition",
    "Three-beat Escalation", "Repeated Parallelism", "Repeated Contrast",
    "Philosophical Summary", "Superiority Contrast", "Overclaim Promise",
]

VERSION = "v0.9.0"
BAD_TYPOS = [
    "\u6247\u63cf", "\u7be2\u6539", "\u641b\u642d",
    "\u5bf9\u4ee5", "\u507f\u6539", "\u5ea7\u6807",
]
errors = []
warnings = []


def read(root, rel):
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def main():
    if len(sys.argv) < 2:
        print("usage: quick_validate.py <skill_root>")
        return 2
    root = os.path.abspath(sys.argv[1])
    name = os.path.basename(root.rstrip("/"))

    # 1. structure
    for rel in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, rel)):
            errors.append("missing file: %s" % rel)

    for sub in ("tests/baseline-red", "tests/after-green", "tests/clean-source"):
        d = os.path.join(root, sub)
        if not os.path.isdir(d):
            errors.append("missing dir: %s" % sub)
        elif len([f for f in os.listdir(d) if f.endswith(".txt")]) < (1 if sub.endswith("clean-source") else 5):
            errors.append("%s does not contain enough .txt cases" % sub)

    # 2. frontmatter
    skill = read(root, "SKILL.md") or ""
    if not skill.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter")
    fm = skill.split("---", 2)
    front = fm[1] if len(fm) >= 3 else ""
    m = re.search(r"^name:\s*(\S+)\s*$", front, re.M)
    if not m:
        errors.append("frontmatter missing name")
    else:
        skill_name = m.group(1).strip('"\'')
        if skill_name != "natural-narration":
            errors.append("frontmatter name must be natural-narration")
        if name != skill_name:
            warnings.append("directory name %r != skill name %r" % (name, skill_name))
    d = re.search(r"^description:\s*(.+)$", front, re.M)
    if not d:
        errors.append("frontmatter missing description")
    else:
        desc = d.group(1)
        if not re.search(r"^\s*Use when", desc):
            errors.append("description should start with 'Use when'")
        if len(desc) < 80:
            warnings.append("description looks too short to route well")

    # 3. agents/openai.yaml
    y = read(root, "agents/openai.yaml") or ""
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in y:
            errors.append("agents/openai.yaml missing %s" % key)
    if "interface:" not in y or "policy:" not in y:
        errors.append("agents/openai.yaml missing interface/policy sections")
    if "$natural-narration" not in y:
        errors.append("openai.yaml default_prompt should include $natural-narration")

    # 4. version consistency
    for rel in ("SKILL.md", "README.md", "VERSION.md", "CHANGELOG.md"):
        txt = read(root, rel) or ""
        if VERSION not in txt and VERSION.lstrip("v") not in txt:
            errors.append("%s does not mention %s" % (rel, VERSION))

    # 4c. v0.8.0 first-draft gate: every topic RED FAIL / GREEN PASS
    import subprocess as _sp
    _fd = os.path.join(root, "tests", "first-draft")
    _bc = os.path.join(root, "scripts", "nn_blueprint_check.py")
    _topics = [d for d in sorted(os.listdir(_fd)) if os.path.exists(os.path.join(_fd, d, "blueprint.md"))] if os.path.isdir(_fd) else []
    if len(_topics) < 4:
        errors.append("v0.8.0: tests/first-draft needs >= 4 topics with blueprint.md")
    for _t in _topics:
        _bp = os.path.join(_fd, _t, "blueprint.md")
        for _f in sorted(os.listdir(os.path.join(_fd, _t))):
            if not _f.endswith(".txt") or not (_f.startswith("RED") or _f.startswith("GREEN")):
                continue
            _rc = _sp.run([sys.executable, _bc, os.path.join(_fd, _t, _f), "--blueprint", _bp, "--gate"], capture_output=True).returncode
            if _f.startswith("GREEN") and _rc != 0:
                errors.append("v0.8.0: %s/%s should PASS structure gate" % (_t, _f))
            if _f.startswith("RED"):
                _ro = _sp.run([sys.executable, _bc, os.path.join(_fd, _t, _f), "--blueprint", _bp], capture_output=True, text=True).stdout
                if "STRUCTURE RISK: LOW" in _ro:
                    errors.append("v0.9.0: %s/%s should be MEDIUM/HIGH risk" % (_t, _f))
    # 4d. v0.8.1 concrete thread + reveal beats
    if len(_topics) < 5:
        errors.append("v0.8.1: tests/first-draft needs >= 5 topics")
    for _t in _topics:
        _bpt = open(os.path.join(_fd, _t, "blueprint.md"), encoding="utf-8").read()
        for _k in ("题目词", "揭底"):
            if ("- %s：" % _k) not in _bpt:
                errors.append("v0.8.1: %s/blueprint.md missing '%s'" % (_t, _k))
    _tt = os.path.join(_fd, "clothes-origin", "blueprint-topic-thread.md")
    _cg = os.path.join(_fd, "clothes-origin", "GREEN-first-draft.txt")
    if os.path.exists(_tt) and os.path.exists(_cg):
        _o = _sp.run([sys.executable, _bc, _cg, "--blueprint", _tt], capture_output=True, text=True).stdout
        if "主线词与题目词重叠" not in _o:
            errors.append("v0.9.0: topic-as-thread blueprint must raise overlap risk")
    _bctxt = open(_bc, encoding="utf-8").read()
    if 'VERSION = "v0.9.0"' not in _bctxt or "thread_is_topic" not in _bctxt or "reveal_positions" not in _bctxt:
        errors.append("v0.8.1: nn_blueprint_check.py lacks topic/reveal checks")
    _skill = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
    for _k in ("揭底节拍", "题目词", "不能是题目本身"):
        if _k not in _skill:
            errors.append("v0.8.1: SKILL.md missing '%s'" % _k)
    # 4e. v0.9.0 diagnostics, stop condition, listening check
    for _f in ("listening-check.md", "revision-principles.md", "structure-handoff.md", "acceptance.md"):
        if not os.path.exists(os.path.join(root, "references", _f)):
            errors.append("v0.9.0: missing references/%s" % _f)
    for _k in ("停止条件", "不是交付门槛", "听觉理解", "交回编剧", "按作用、篇幅和重复程度判断", "必查五项"):
        if _k not in _skill:
            errors.append("v0.9.0: SKILL.md missing '%s'" % _k)
    for _k in ("结构分 ≥ 85", "自问自答 ≤ 1"):
        if _k in _skill:
            errors.append("v0.9.0: SKILL.md still has hard rule '%s'" % _k)
    if "risk_level" not in _bctxt or "risks" not in _bctxt:
        errors.append("v0.9.0: nn_blueprint_check.py lacks risk diagnostics")
    for _k in ("首稿蓝图", "交稿前自审循环", "nn_blueprint_check", "CLEAN 到顶提示"):
        if _k not in _skill:
            errors.append("v0.8.0: SKILL.md missing '%s'" % _k)

    # 4b. v0.7.0 copy-only scope: no export/handoff modules inside this Skill
    for rel in ("scripts/nn_video_export.py", "references/video-handoff.md", "tests/video-handoff"):
        if os.path.exists(os.path.join(root, rel)):
            errors.append("copy-only scope violated: %s should not exist" % rel)
    sk = read(root, "SKILL.md") or ""
    if "范围边界" not in sk or "纯文案处理" not in sk:
        errors.append("SKILL.md missing 范围边界 / 纯文案处理 section")
    for tok in ("nn_video_export", "script.txt", "交给动态视频"):
        if tok in sk:
            errors.append("SKILL.md still mentions non-copy feature: %s" % tok)

    # 5. capability landing (semantic, not only structural)
    syn = read(root, "references/syntax-pattern-detection.md") or ""
    for sid in SYNTAX_IDS:
        if sid not in syn:
            errors.append("syntax-pattern-detection.md missing structure id: %s" % sid)
    for sid in ("Expectation", "Reversal", "Repeated Parallelism"):
        if sid not in skill:
            warnings.append("SKILL.md does not name structure id: %s" % sid)

    wf = read(root, "references/workflow.md") or ""
    if "MODE A" not in wf or "MODE B" not in wf:
        errors.append("workflow.md must document MODE A / MODE B")
    if "MODE A" not in skill or "MODE B" not in skill:
        errors.append("SKILL.md must document MODE A / MODE B")

    sc = read(root, "references/scan-and-scoring.md") or ""
    for token in ("Naturalness", "Clich", "AI Pattern",
                  "Information Preservation", "Clarity", "Story Strength"):
        if token not in sc:
            errors.append("scan-and-scoring.md missing score: %s" % token)
    if "\u2265 8" not in sc or "\u2264 2" not in sc:
        errors.append("scan-and-scoring.md missing pass thresholds")

    ba = read(root, "references/before-after-examples.md") or ""
    for must in ("5500", "\u4e0a\u5343\u4e07", "\u767e\u4e07",
                 "\u95ea\u7535\u901a\u9053"):
        if must not in ba:
            errors.append("before-after-examples.md missing example token: %s" % must)

    ac = read(root, "references/anti-cliche-patterns.md") or ""
    for cat in ("A.", "B.", "C.", "D.", "E.", "F.", "G.", "H."):
        if cat not in ac:
            errors.append("anti-cliche-patterns.md missing category %s" % cat)
    if "\u7981\u8bcd" not in ac:
        warnings.append("anti-cliche-patterns.md should say it is not a banned-word list")

    ao = read(root, "references/anti-overcorrection.md") or ""
    if "\u7206\u6b3e" not in ao or "\u7981\u8bcd" not in ao:
        errors.append("anti-overcorrection.md must cover both pressure scenarios")

    res = read(root, "tests/RESULTS.md") or ""
    for token in ("RED", "GREEN", "REFACTOR", "INFORMATION PRESERVATION"):
        if token not in res:
            errors.append("tests/RESULTS.md missing evidence section: %s" % token)

    # 5b. v0.2.0 capability landing: story engine + write-first questions
    se = read(root, "references/story-engine.md") or ""
    for token in ("\u53d9\u4e8b\u4e3b\u4f53", "\u573a\u666f\u8d77\u70b9",
                  "\u72b6\u6001\u53d8\u5316", "\u53d1\u73b0\u8def\u5f84",
                  "\u89c6\u89d2\u79fb\u52a8"):
        if token not in se:
            errors.append("story-engine.md missing engine: %s" % token)
    if "story_strength" not in se:
        warnings.append("story-engine.md should name the story_strength metric")

    aps = read(root, "references/audience-problem-scene.md") or ""
    for token in ("Audience", "Problem", "Scene", "Solution", "Value",
                  "Explanation Test"):
        if token not in aps:
            errors.append("audience-problem-scene.md missing item: %s" % token)

    scan_py = read(root, "scripts/nn_scan.py") or ""
    for token in ("H_overclaim_persuasion", "story_strength",
                  "Superiority Contrast", "Overclaim Promise", "--story-gate"):
        if token not in scan_py:
            errors.append("nn_scan.py missing v0.2.0 detector: %s" % token)

    for token in ("\u6545\u4e8b\u5c42", "\u5199\u524d\u4e94\u95ee"):
        if token not in skill:
            errors.append("SKILL.md must document v0.2.0 item: %s" % token)

    # 5c. v0.3.0 capability landing: value chain + clarity + voice profiles
    vc = read(root, "references/value-chain.md") or ""
    for token in ("\u771f\u5b9e\u95ee\u9898", "\u6838\u5fc3\u5224\u65ad",
                  "\u5b9e\u9645\u5f71\u54cd", "\u53ef\u6267\u884c\u52a8\u4f5c",
                  "\u9002\u7528\u8fb9\u754c"):
        if token not in vc:
            errors.append("value-chain.md missing link: %s" % token)

    ce = read(root, "references/clarity-engine.md") or ""
    for token in ("\u4e00\u53e5\u4e00\u4efb\u52a1", "\u6307\u4ee3",
                  "\u62bd\u8c61\u8bcd"):
        if token not in ce:
            errors.append("clarity-engine.md missing check: %s" % token)

    vp = read(root, "references/voice-profiles.md") or ""
    for token in ("DEFAULT_NATURAL", "PRACTICAL_EXPLAINER", "SLOW_ENTREPRENEURSHIP"):
        if token not in vp:
            errors.append("voice-profiles.md missing profile: %s" % token)
        if token not in skill:
            errors.append("SKILL.md must name voice profile: %s" % token)

    pr = read(root, "references/practical-value-router.md") or ""
    if "\u79d1\u666e" not in pr:
        errors.append("practical-value-router.md must state which topics are exempt")

    ea = read(root, "references/expression-assets.md") or ""
    if "\u91d1\u53e5\u5e93" not in ea:
        errors.append("expression-assets.md must state it is not a quote bank")

    for token in ("value_strength", "--value-gate", "GENERIC_VALUE"):
        if token not in scan_py:
            errors.append("nn_scan.py missing v0.3.0 detector: %s" % token)

    for token in ("\u4ef7\u503c\u94fe", "\u6e05\u6670\u5ea6"):
        if token not in skill:
            errors.append("SKILL.md must document v0.3.0 item: %s" % token)
    if "Value Strength" not in sc:
        errors.append("scan-and-scoring.md missing score: Value Strength")


    # 5d. v0.4.0 capability landing: evidence arc + present-day echo
    ev = read(root, "references/evidence-led-narration.md") or ""
    for token in ("Evidence Arc", "CRACK", "RANGE", "PATTERN", "LIMIT", "Evidence Gate"):
        if token not in ev:
            errors.append("evidence-led-narration.md missing item: %s" % token)
    pe = read(root, "references/present-day-echo.md") or ""
    for token in ("Same", "Changed", "Mechanism", "Boundary"):
        if token not in pe:
            errors.append("present-day-echo.md missing item: %s" % token)
    cd = read(root, "references/critical-documentary.md") or ""
    for token in ("FACT", "INFERENCE", "VALUE JUDGMENT"):
        if token not in cd:
            errors.append("critical-documentary.md missing distinction: %s" % token)
    for token in ("evidence_report", "evidence_strength", "--evidence-gate", "ANALOGY_OVERREACH"):
        if token not in scan_py:
            errors.append("nn_scan.py missing v0.4.0 detector: %s" % token)
    if "CRITICAL_DOCUMENTARY" not in skill:
        errors.append("SKILL.md must name CRITICAL_DOCUMENTARY")

    # 5e. v0.5.0 capability landing: semantic fidelity + no-op + author match + file mode
    sf = read(root, "references/semantic-fidelity.md")
    for token in ("NEGATION", "MODALITY", "STATUS", "CONDITION", "SCOPE",
                  "ATTRIBUTION", "CAUSALITY", "Semantic Fidelity"):
        if token not in sf:
            errors.append("semantic-fidelity.md missing anchor: %s" % token)
    fm = read(root, "references/file-mode.md")
    for token in ("YAML", "代码块", "行内代码", "链接目标", "标题", "表格", "有序步骤", "显式 ID"):
        if token not in fm:
            errors.append("file-mode.md missing protected item: %s" % token)
    av = read(root, "references/author-voice-match.md")
    for token in ("AUTHOR_MATCH", "不迁移", "优先级"):
        if token not in av:
            errors.append("author-voice-match.md missing item: %s" % token)
    rr = read(root, "references/register-router.md")
    for token in ("SPOKEN", "ARTICLE", "TECHNICAL", "PERSONAL"):
        if token not in rr:
            errors.append("register-router.md missing register: %s" % token)
    scan = read(root, "scripts/nn_scan.py")
    for token in ("fidelity_report", "--fidelity-gate", "--noop-gate",
                  "I_editorial_residue", "UNSOURCED_AUTHORITY"):
        if token not in scan:
            errors.append("nn_scan.py missing v0.5.0 detector: %s" % token)
    if "def compare" not in read(root, "scripts/nn_structure_check.py"):
        errors.append("nn_structure_check.py missing compare()")
    skill = read(root, "SKILL.md")
    for token in ("语义保真层", "No-op Rule", "AUTHOR_MATCH", "FILE MODE", "--fidelity-gate"):
        if token not in skill:
            errors.append("SKILL.md must document v0.5.0 item: %s" % token)
    if "No-op Rule" not in read(root, "references/anti-overcorrection.md"):
        errors.append("anti-overcorrection.md must document No-op Rule")
    if "Semantic Fidelity" not in read(root, "references/scan-and-scoring.md"):
        errors.append("scan-and-scoring.md missing score: Semantic Fidelity")
    for rel in ("tests/clean-source/Z-source.md", "tests/baseline-red/Z-structure-broken.md",
                "tests/after-green/Z-structure-kept.md"):
        if not os.path.isfile(os.path.join(root, rel)):
            errors.append("missing v0.5.0 FILE MODE fixture: %s" % rel)

    # 6. hygiene
    leaks = ["/" + "data/skill-" + "build", "/" + "home/" + "vercel"]
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [x for x in dirnames if x not in ("__pycache__", ".git")]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if fn.endswith((".pyc", ".tmp", ".bak", "~")) or fn == ".DS_Store":
                errors.append("temp/junk file present: %s" % fn)
                continue
            if fn.endswith((".md", ".py", ".yaml", ".txt")):
                try:
                    with open(p, encoding="utf-8") as fh:
                        content = fh.read()
                except UnicodeDecodeError:
                    errors.append("not valid UTF-8: %s" % fn)
                    continue
                if any(t in content for t in leaks):
                    errors.append("absolute sandbox path leaked in %s" % fn)
                if "\ufffd" in content:
                    errors.append("replacement char (mojibake) in %s" % fn)
                for bad in BAD_TYPOS:
                    if bad in content:
                        errors.append("typo %r present in %s" % (bad, fn))

    print("skill root: %s" % root)
    print("checked %d required files" % len(REQUIRED_FILES))
    for w in warnings:
        print("WARN: %s" % w)
    if errors:
        for e in errors:
            print("ERROR: %s" % e)
        print("RESULT: FAIL (%d errors, %d warnings)" % (len(errors), len(warnings)))
        return 1
    print("RESULT: PASS (0 errors, %d warnings)" % len(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
