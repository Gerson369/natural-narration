#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nn_blueprint_check.py - v0.9.0 结构诊断（Structure Diagnostics）

v0.9.0：从「85 分硬门槛」改为「风险提示」。输出 LOW / MEDIUM / HIGH 与
        带位置的风险清单，由人判断段落关系；--gate 只在 HIGH 时返回 1（回归测试用），
        不作为交稿门槛。主线离场、揭底间距、连续讲解、主线即题目等 v0.8.1 项
        只进风险清单，不再扣分：问题链式结构不靠同一个词也能成立。

只检查文案结构，不改文字。用于 MODE A WRITE 交稿前的内部自审。

v0.8.0：主线是否一直在场、解释是否压过了发生、结尾是否靠总结句收、
        是否回扣开头、相邻句是否只在复述、动作句是否太少。
v0.8.1：
  1. 主线必须是具体的人 / 物 / 场景，不能是题目本身（题目词 vs 主线词）。
  2. 主线贯穿：开头 15% 出现、中段（30%-85%）至少 2 次、结尾 15% 回到它。
  3. 揭底节拍：蓝图列出 >=3 个揭底点；主揭底落在全文 20%-60%；
     相邻揭底间距 <= 35%；揭底之间不能连着一长串讲解句。

用法：
  python3 scripts/nn_blueprint_check.py draft.txt --blueprint blueprint.md [--gate] [--json]
  python3 scripts/nn_blueprint_check.py draft.txt --thread "体虱,接缝" --topic "衣服,穿衣服" \
      --reveals "8.3万|骨针|人口"

blueprint.md 中的三行：
  主线词：词1,词2,词3        （具体的人 / 物 / 场景）
  题目词：词1,词2            （题目本身的词，主线词不能与之相同或互相包含）
  揭底：关键词A/同义词|关键词B|关键词C   （第一个是主揭底，按出现顺序写）
"""
import argparse
import json
import re
import sys

VERSION = "v0.9.0"
GATE = 85          # LOW 风险线（参考，不是交付门槛）
HIGH_RISK = 60     # 低于此值为 HIGH

EXPLAIN = re.compile(r"规则|版本|要求|玩法|研究者|研究|是指|也就是|意思是|原理|定义|称为|叫做|说明|线索|属于|概念|理论|机制|原因是|之所以|本质")
ACTION = re.compile(r"掷|走|落|停|推|赶|拿|放|翻|收|吵|喊|看着|等|追|输|赢|打开|关上|写下|按下|点开|回复|删|拖|拆|装|泡|煮|烤|切|咬|摸|闻|倒|递|抬|跑|坐|站|躲|冲|扔|捡|交|试|测|滴|加热|冷却|提取|揉|塞|挪|掏|划|抄|翻开|合上|签|贴|拨|接|挂|摆|配|喝|吃|吐|抓|握|缝|爬|搬|磨|裹|钻|系上|包住|出土|捏")
SUMMARY_END = re.compile(r"所以说|总之|总而言之|总的来说|让我们看见|让我们看到|告诉我们|启示|意义在于|本质上|说到底|归根结底|可以发生在|这就是.{0,6}的(力量|意义|魅力)|值得我们|我们应该|不正是")
SPLIT = re.compile(r"[^。！？!?\n]+[。！？!?…”」]*")
STOP = set("我们 你们 他们 一个 这个 那个 这样 那样 可以 没有 就是 还是 因为 所以 如果 但是 不过 自己 时候 什么 怎么".split())

EXPLAIN_RUN_LIMIT = 4
MAIN_REVEAL_WINDOW = (0.20, 0.60)
REVEAL_GAP_LIMIT = 0.35
MIN_REVEALS = 3


def load(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    paras, cur = [], []
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("#") or s.startswith(">") or s.startswith("<!--"):
            continue
        if not s:
            if cur:
                paras.append(cur)
                cur = []
            continue
        for m in SPLIT.findall(s):
            if m.strip():
                cur.append(m.strip())
    if cur:
        paras.append(cur)
    return paras


def _words(text):
    return [w.strip() for w in re.split(r"[,，、]", text) if w.strip()]


def parse_blueprint(path):
    out = {"thread": [], "topic": [], "reveals": []}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"\s*[-*]?\s*(主线词|题目词|揭底)\s*[:：]\s*(.+)", line)
            if not m:
                continue
            key, val = m.group(1), m.group(2).strip()
            if key == "主线词":
                out["thread"] = _words(val)
            elif key == "题目词":
                out["topic"] = _words(val)
            else:
                out["reveals"] = parse_reveals(val)
    return out


def parse_reveals(val):
    items = []
    for it in re.split(r"[|｜]", val):
        kws = [k.strip() for k in it.split("/") if k.strip()]
        if kws:
            items.append(kws)
    return items


def bigrams(s):
    t = re.sub(r"[^\u4e00-\u9fff0-9A-Za-z]", "", s)
    return {t[i:i + 2] for i in range(len(t) - 1)}


def split_thread(thread, topic):
    """主线词与题目词相同或互相包含 -> 视为『主线就是题目』。"""
    bad = [w for w in thread if any(w in t or t in w for t in topic)]
    good = [w for w in thread if w not in bad]
    return good, bad


def check(path, thread, topic=None, reveals=None):
    topic = topic or []
    reveals = reveals or []
    paras = load(path)
    sents = [s for p in paras for s in p]
    n = len(sents)
    notes = []

    good_thread, topic_thread = split_thread(thread, topic)
    if not topic:
        notes.append("蓝图缺『题目词』，无法确认主线不是题目本身")
    if topic_thread:
        notes.append("主线词就是题目本身：%s" % "、".join(topic_thread))
    use = good_thread
    has = [any(w in s for w in use) for s in sents] if use else [False] * n

    gap = run = 0
    for h in has:
        run = 0 if h else run + 1
        gap = max(gap, run)
    gap_limit = max(6, round(n * 0.12))

    detached = [i + 1 for i, p in enumerate(paras) if not any(any(w in s for w in use) for s in p)]

    # v0.8.1 主线贯穿
    def band(lo, hi):
        a, b = int(n * lo), max(int(n * lo) + 1, int(round(n * hi)))
        return sum(1 for i in range(a, min(b, n)) if has[i])
    arc = {"opening": band(0, 0.15) >= 1, "middle": band(0.30, 0.85) >= 2, "ending": band(0.85, 1.0) >= 1}

    explain_flags = [bool(EXPLAIN.search(s) and not ACTION.search(s)) for s in sents]
    explain_ratio = sum(explain_flags) / n if n else 0
    action_ratio = sum(1 for s in sents if ACTION.search(s)) / n if n else 0
    explain_run = r = 0
    for f in explain_flags:
        r = r + 1 if f else 0
        explain_run = max(explain_run, r)

    tail = sents[-3:]
    summary_end = [s for s in tail if SUMMARY_END.search(s)]

    head_bg = set()
    for s in sents[:3]:
        head_bg |= {b for b in bigrams(s) if b not in STOP}
    tail_bg = set()
    for s in sents[-6:]:
        tail_bg |= bigrams(s)
    callback = len(head_bg & tail_bg) >= 2 or any(w in " ".join(sents[-6:]) for w in use)

    first = sents[0] if sents else ""
    hook = bool(re.search(r"[？?]|如果|假如|你|\d|[一二三四五六七八九十百千万]+(年|天|岁|个|次|号)", first))

    restate = []
    for i in range(1, n):
        cur = {b for b in bigrams(sents[i]) if b not in STOP}
        if len(cur) < 6:
            continue
        prev = set()
        for j in range(max(0, i - 2), i):
            prev |= bigrams(sents[j])
        if len(cur & prev) / len(cur) >= 0.6 and not re.search(r"\d", sents[i]):
            restate.append(sents[i])

    # v0.8.1 揭底节拍
    beat_pos, missing = [], []
    for kws in reveals:
        idx = next((i for i, s in enumerate(sents) if any(k in s for k in kws)), None)
        if idx is None:
            missing.append("/".join(kws))
            beat_pos.append(None)
        else:
            beat_pos.append(round(idx / n, 3) if n else 0)
    found = sorted(p for p in beat_pos if p is not None)
    main_pos = beat_pos[0] if beat_pos else None
    gaps = []
    if found:
        pts = found + [1.0]
        gaps = [round(b - a, 3) for a, b in zip(pts, pts[1:])]
    wide_gaps = [g for g in gaps if g > REVEAL_GAP_LIMIT]

    score = 100
    score -= min(30, 4 * max(0, gap - gap_limit))
    score -= 8 * max(0, len(detached) - 1)
    score -= min(30, round(100 * max(0, explain_ratio - 0.22)))
    score -= 10 * len(summary_end)
    score -= 0 if callback else 10
    score -= 0 if hook else 10
    score -= 4 * len(restate)
    score -= min(25, round(150 * max(0, 0.2 - action_ratio)))
    # v0.9.0: 以下只进风险清单，不扣分
    risks = []
    if topic_thread:
        risks.append("主线词与题目词重叠（%s）：确认正文是否有具体的人/物/场景或问题链在推进" % "、".join(topic_thread))
    for k, v in arc.items():
        if not v:
            risks.append("主线在%s不在场：人工看这一段是否仍在回答主问题" % {"opening": "开头", "middle": "中段", "ending": "结尾"}[k])
    if reveals and len(reveals) < MIN_REVEALS:
        risks.append("蓝图揭底点少于 %d 个" % MIN_REVEALS)
    for m in missing:
        risks.append("蓝图揭底『%s』在正文里没找到" % m)
    if main_pos is not None and not (MAIN_REVEAL_WINDOW[0] <= main_pos <= MAIN_REVEAL_WINDOW[1]):
        risks.append("主揭底在 %.0f%% 处（参考区间 20%%-60%%）" % (100 * main_pos))
    for g in wide_gaps:
        risks.append("有一段约 %.0f%% 篇幅没有新揭底：看这段是否交付了新理解" % (100 * g))
    if explain_run > EXPLAIN_RUN_LIMIT:
        risks.append("连续 %d 句讲解：检查是否脱离主问题，必要讲解可以保留" % explain_run)
    if detached:
        risks.append("第 %s 段未出现主线词：人工判断它承担理解/证据/节奏/幽默/情感中的哪一项" % "、".join(map(str, detached)))
    if summary_end:
        risks.append("结尾 %d 句像总结句" % len(summary_end))
    if restate:
        risks.append("%d 句疑似复述上文" % len(restate))
    score = max(0, score)
    return {
        "file": path, "version": VERSION, "sentences": n, "paragraphs": len(paras),
        "thread_words": use, "topic_words": topic, "thread_is_topic": topic_thread,
        "thread_gap": gap, "thread_gap_limit": gap_limit,
        "detached_paragraphs": detached,
        "thread_arc": arc,
        "explain_ratio": round(explain_ratio, 3),
        "explain_run": explain_run,
        "action_ratio": round(action_ratio, 3),
        "summary_ending": summary_end,
        "callback_to_opening": callback,
        "hook_ok": hook,
        "restatements": restate,
        "reveal_positions": beat_pos,
        "reveal_missing": missing,
        "reveal_gaps": gaps,
        "notes": notes,
        "risks": risks,
        "structure_score": score,
        "risk_level": "LOW" if score >= GATE else ("MEDIUM" if score >= HIGH_RISK else "HIGH"),
        "verdict": "LOW" if score >= GATE else ("MEDIUM" if score >= HIGH_RISK else "HIGH"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--thread", help="主线词，逗号分隔")
    ap.add_argument("--topic", help="题目词，逗号分隔")
    ap.add_argument("--reveals", help="揭底关键词，| 分隔，同义词用 /")
    ap.add_argument("--blueprint", help="含『主线词 / 题目词 / 揭底』的蓝图文件")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    bp = parse_blueprint(a.blueprint) if a.blueprint else {"thread": [], "topic": [], "reveals": []}
    thread = _words(a.thread) if a.thread else bp["thread"]
    topic = _words(a.topic) if a.topic else bp["topic"]
    reveals = parse_reveals(a.reveals) if a.reveals else bp["reveals"]
    if not thread:
        print("ERROR: 需要 --thread 或含『主线词：』的 --blueprint")
        return 2
    r = check(a.file, thread, topic, reveals)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("FILE: %s (%d sentences, %d paragraphs)" % (r["file"], r["sentences"], r["paragraphs"]))
        print("thread=%s topic=%s thread_is_topic=%s" % (",".join(r["thread_words"]) or "-", ",".join(r["topic_words"]) or "-", ",".join(r["thread_is_topic"]) or "none"))
        print("thread_gap=%d (limit %d) detached_paragraphs=%s arc=%s"
              % (r["thread_gap"], r["thread_gap_limit"], r["detached_paragraphs"] or "none", r["thread_arc"]))
        print("explain_ratio=%.2f explain_run=%d action_ratio=%.2f summary_ending=%d callback=%s hook=%s restatements=%d"
              % (r["explain_ratio"], r["explain_run"], r["action_ratio"], len(r["summary_ending"]), r["callback_to_opening"], r["hook_ok"], len(r["restatements"])))
        print("reveals=%s missing=%s gaps=%s" % (r["reveal_positions"], r["reveal_missing"] or "none", r["reveal_gaps"]))
        for s in r["notes"]:
            print("   [note] %s" % s)
        for s in r["summary_ending"]:
            print("   [summary] %s" % s)
        for s in r["restatements"]:
            print("   [restate] %s" % s)
        for s in r["risks"]:
            print("   [risk] %s" % s)
        print("STRUCTURE RISK: %s (%d/100, 诊断参考，不是交付门槛)" % (r["risk_level"], r["structure_score"]))
    return 1 if (a.gate and r["risk_level"] == "HIGH") else 0


if __name__ == "__main__":
    sys.exit(main())
