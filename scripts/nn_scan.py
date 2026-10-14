#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NATURAL NARRATION SCAN (nn_scan)

Semantic-lexical + syntax-structural + rhythm scanner for Chinese narration /
spoken-video scripts. Not a banned-word list: lexical hits are only one of three
layers. The scanner also detects repeated SYNTAX patterns (same structure with
different words) and rhythm failures, then prints internal scores.

Usage:
  python3 nn_scan.py FILE [FILE ...] [--json] [--quiet] [--story-gate] [--value-gate] [--evidence-gate]
  python3 nn_scan.py --baseline BEFORE.txt --after AFTER.txt   # CLEAN-mode diff
  python3 nn_scan.py --baseline BEFORE.txt --after AFTER.txt --fidelity-gate   # v0.5.0
  python3 nn_scan.py --baseline BEFORE.txt --after AFTER.txt --noop-gate       # v0.5.0
"""

import argparse
import json
import re
import statistics
import sys
from difflib import SequenceMatcher

SENT_SPLIT = re.compile(r"[^。！？!?…\n]+[。！？!?…]*")
CLAUSE_SPLIT = re.compile(r"[，,。；;！？!?、…]")
ARABIC = re.compile(r"\d+(?:\.\d+)?")
CN_SCALE = ["上千万", "上百万", "几十亿", "上万", "百万", "千万", "几亿", "数亿"]

# ---------------------------------------------------------------- lexical layer
LEXICAL = {
    "A_binary_reversal": [
        r"(?:不是|并非|并不是)[^。！？\n]{0,25}(?:而是|而更是)",
        r"不是[^。！？\n]{0,20}[，,]?\s*更不是",
        r"真正(?:的)?[^。！？\n]{0,12}(?:不是|的不是)",
        r"你以为[^。！？\n]{0,25}(?:其实|实际上|事实上)",
        r"看似[^。！？\n]{0,25}(?:实际上|其实|背后却|却)",
        r"(?:表面上|表面看|看起来|听起来)[^。！？\n]{0,25}(?:实际|其实|背后|却)",
        r"与其说[^。！？\n]{0,25}不如说",
        r"它不是[^。！？\n]{0,25}它只是",
    ],
    "B_fake_suspense": [
        r"真正(?:可怕|恐怖|要命|致命)的是",
        r"更(?:不可思议|离谱|夸张|可怕|惊人)的(?:是|还在后面)",
        r"(?:但|可)?事情(?:还没有结束|远?没有(?:那么|这么)简单|并不简单)",
        r"这(?:还)?只是(?:一个)?开始",
        r"更(?:大|难)的(?:问题|麻烦)(?:还)?在后面",
        r"答案(?:可能)?(?:超出|远超)你的想象",
        r"(?:但)?别急", r"先别急", r"别急着",
        r"直到这里[^。！？\n]{0,15}才(?:真正)?开始",
        r"接下来发生的(?:事情|一切)",
        r"故事(?:才)?(?:真正)?(?:刚)?开始",
    ],
    "C_fake_question": [
        r"问题来了", r"那么问题(?:又)?来了",
        r"这(?:到底)?意味着什么",
        r"为什么会(?:这样|如此)",
        r"到底有多(?:夸张|大|热|快|远|可怕)",
        r"科学家(?:是)?怎么知道",
        r"你(?:能)?想(?:象|像)(?:得到)?吗",
    ],
    "D_host_transition": [
        r"值得注意的是", r"需要注意的是", r"有意思的是", r"更重要的是",
        r"事实上", r"说到这里", r"简单来说", r"换句话说", r"也就是说",
        r"所以你会发现", r"我们不妨", r"我们(?:来|再)看", r"接下来(?:我们)?(?:看看|来看)",
        r"这就是为什么", r"不难发现",
    ],
    "E_pseudo_aphorism": [
        r"虽然[^。！？\n]{0,20}却",
        r"只[^。！？\n]{0,12}却足以",
        r"短短[^。！？\n]{0,12}却",
        r"从某种意义上(?:来)?说",
        r"也许真正值得(?:思考|深思|记住)的是",
        r"人类终于(?:意识到|明白|懂得)",
        r"(?:宇宙|自然|大自然|时间)(?:再次|又一次)?(?:告诉|提醒|教会)(?:我们|人类)",
        r"大自然从来不会",
        r"这既是[^。！？\n]{0,25}也是",
        r"真正让人(?:震撼|敬畏|动容)的(?:不是|是)",
    ],
    "G_forced_grandiosity": [
        r"这场发生在[^。！？\n]{0,20}的",
        r"这一刻[^。！？\n]{0,20}(?:被|将|才)",
        r"(?:人类|文明|命运)(?:有多)?(?:渺小|伟大|终将|注定)",
        r"时间的(?:礼物|馈赠)",
        r"(?:永恒|敬畏|宿命)",
    ],
    # v0.2.0 新增：说服腔 / 绝对化承诺 / 身份优越。
    # 讲师型、方法论型口播的主要模板来源，词汇层与 G 类同权重计分。
    "H_overclaim_persuasion": [
        r"一定(?:能|会|可以)(?:赚到?钱|成功|做到|实现|改变)",
        r"(?:一定|必然|绝对|百分之百|100%)(?:能|会|可以)(?:赚|成功|做到|改变)",
        r"(?:彻底|完全)改变(?:你的)?(?:人生|生活|命运)",
        r"照我说的(?:去)?做",
        r"(?:我|咱)(?:和|跟|同)(?:你|你们)(?:是)?不(?:一样|同)",
        r"(?:我们俩?|咱们)(?:不在一个|不是一个)(?:档次|层次|级别)",
        r"(?:你|你们)(?:永远|根本)(?:做不到|不懂|不明白)",
        r"(?:收藏|点赞|关注)(?:起来|一下)?[^。！？\n]{0,8}(?:反复|认真|多听)",
        r"(?:记住|听懂)(?:我)?(?:这句话|我说的)",
        r"(?:你|你们)的(?:生活|人生)一定会",
    ],
    # v0.5.0 新增：编辑过程残留与万能背景。成稿里出现即说明改写流程漏进了正文。
    "I_editorial_residue": [
        r"希望(?:这篇|本文|以上|这些|这条)?[^。！？\n]{0,8}(?:对你|对大家)(?:有所)?帮助",
        r"下面是(?:优化|修改|改写|润色|调整)(?:后|过)的",
        r"(?:根据|按照)(?:你|您)的要求",
        r"如果(?:你|您)(?:愿意|需要)[^。！？\n]{0,8}我(?:还)?可以",
        r"我将从以下几个方面",
        r"在当今[^。！？\n]{0,12}(?:时代|社会)",
        r"随着[^。！？\n]{0,10}(?:飞速|快速|迅猛|不断)发展",
        r"在[^。！？\n]{0,8}(?:大|新)(?:背景|时代)下",
    ],
}

EXPECT_MARKERS = ["你以为", "你可能以为", "很多人以为", "大家都以为", "都以为", "看似",
                  "表面上", "表面看", "看起来", "听起来", "印象中", "很多人认为",
                  "大家都说", "我们总以为"]
REVERSAL_MARKERS = ["其实", "实际上", "实际", "事实上", "真相是", "而是", "背后却",
                    "却是", "真正"]
SUSPENSE_CUES = ["别急", "事情还没有结束", "这还只是开始", "只是开始", "更夸张",
                 "更不可思议", "更可怕", "答案", "接下来发生", "后面", "还没完",
                 "远没有那么简单", "更大的问题"]
HOST_STARTERS = ["值得注意的是", "需要注意的是", "有意思的是", "更重要的是", "事实上",
                 "说到这里", "简单来说", "换句话说", "也就是说", "所以你会发现",
                 "我们不妨", "我们来看", "接下来我们看看", "这就是为什么", "不难发现"]
GRAND_WORDS = ["人类", "宇宙", "文明", "命运", "永恒", "渺小", "敬畏", "意义",
               "终于意识到", "值得思考", "提醒我们", "告诉我们", "从某种意义",
               "时间的礼物", "大自然"]
CONTRAST_MARKERS = ["却", "然而", "但是", "但", "反而", "相反", "其实", "实际上"]

# ------------------------------------------------- v0.2.0 说服腔 + 故事层词表
SUPERIORITY_SELF = ["我", "咱"]
SUPERIORITY_OTHER = ["你", "你们", "大多数人", "普通人", "别人"]
SUPERIORITY_GAP = ["不一样", "不同", "档次", "层次", "级别", "差距"]
PROMISE_WORDS = ["一定", "必然", "绝对", "永远", "百分之百", "100%"]
PROMISE_OUTCOME = ["赚", "成功", "改变", "做到", "实现", "翻倍", "暴涨"]
HEDGE_WORDS = ["大约", "大概", "可能", "通常", "一般", "多数情况", "常见资料",
               "早期研究", "目前", "未必", "不等于"]
SCENE_MARKERS = ["那天", "当时", "现场", "屋里", "屋外", "桌上", "门口", "路上",
                 "电梯", "教室", "实验室", "屏幕", "窗外", "手里", "身后", "眼前",
                 "夜里", "清晨", "会议室", "车上", "地面", "空中", "海里", "地下",
                 "通道", "舱内", "台上"]
TIME_MARKERS = ["那一年", "那天", "当时", "后来", "几分钟", "几秒", "几年", "多年",
                "年", "月", "小时", "分钟", "秒", "世纪", "凌晨", "夜里", "如今"]
ACTION_VERBS = ["走", "推", "拉", "打开", "关上", "拿起", "放下", "发现", "记录",
                "测量", "改", "写", "画", "看到", "听到", "撞", "掉", "停", "跑",
                "加热", "膨胀", "冷却", "断裂", "移动", "穿过", "落下", "升起",
                "聚集", "拆", "装", "敲", "翻", "点亮", "抬头"]
ABSTRACT_WORDS = ["底层逻辑", "思维方式", "认知", "维度", "格局", "体系", "方法论",
                  "本质上", "价值感", "意义感", "赋能", "抓手", "闭环", "生态位",
                  "范式", "心智模型"]

# --------------------------------------------- v0.3.0 价值与清晰度层词表
# 空泛价值句：听起来在给结论，实际上没有交付任何信息
GENERIC_VALUE = ["非常重要", "很重要", "至关重要", "值得我们", "值得深思",
                 "值得思考", "带来启示", "提升认知", "提高认知", "改变认知",
                 "意义重大", "巨大的影响", "提升自己", "保持长期主义",
                 "持续积累", "建立自己的系统", "建立自己的体系", "找到热爱",
                 "重要抓手", "更有价值感", "答案自然会出现", "都应该",
                 "每个人都应该", "所有人都", "任何团队都", "任何人都"]
# 模糊行动词：无法回答「先做什么 / 什么时候做 / 怎么算做完」
VAGUE_ACTION = ["努力", "坚持", "提升自己", "多学习", "多输出", "持续积累",
                "深耕", "慢慢建立", "不断提升", "保持对", "保持好奇"]
# 指代词：听到的那一秒必须能对应上具体对象
REFERENCE_WORDS = ["这", "它"]
# 边界 / 限定表达：它们属于信息本身，不是含糊
BOUNDARY_MARKERS = HEDGE_WORDS + ["不适用", "前提", "条件下", "例外", "仅限",
                                  "取决于", "不一定", "不只是", "有出入"]
# 泛指主语：金句堆叠的典型特征
GENERALIZING_WORDS = ["人", "你", "时间", "选择", "努力", "机会", "生活",
                      "世界", "成长", "命运", "耐心"]

# v0.4.0 证据与类比边界层
EVIDENCE_MARKERS = ["研究", "数据显示", "记录", "遗址", "出土", "样本", "考古",
                    "实验", "论文", "报告", "档案", "测量", "发现"]
INFERENCE_MARKERS = ["支持", "说明", "表明", "由此", "因此", "意味着", "只能证明"]
EVIDENCE_BOUNDARY = ["不能证明", "不足以", "不等于", "仅能", "只支持", "适用范围"]
ANALOGY_OVERREACH = ["本质完全一样", "完全相同", "直接证明", "必然导致",
                      "从未改变，所以", "早就决定了"]

# v0.5.0 中文补充检查：无来源权威、“进行+动词”、长定语
UNSOURCED_AUTHORITY = re.compile(r"(?:有|一些|很多|不少)?(?:专家|业内人士|权威人士|科学家们)(?:认为|表示|指出|普遍认为)|有研究表明|研究表明|数据显示")
SOURCE_SPECIFIC = re.compile(r"\d|《|大学|研究所|研究院|期刊|团队|实验室|机构|协会|报告|论文|档案|未具名|没有给出|没有提供|尚未|不能证明|只能说明")
JINXING_VERB = re.compile(r"(?:进行|加以|予以)(?:了)?(?:深入|全面|系统|有效)?(?:的)?(?:分析|讨论|优化|调整|研究|处理|操作|探讨|改进|梳理|总结)")

# v0.5.0 语义保真层：七类语义锚点（按词组计数，同组同义词互相抵扣）
FIDELITY_GROUPS = {
    "NEGATION": r"尚未|没有|没|并非|并不|无法|不能|不会|未(?!来|必)|不(?!同|仅|但|断|久|少|如|论|过|管)",
    "MODALITY": r"可能|或许|也许|大概|大约|据称|疑似|似乎|估计|未必|不一定",
    "CERTAINTY": r"一定|必然|肯定|(?<!不)确定|就是因为|就是|证明了|毫无疑问|显然|必定",
    "STATUS_PENDING": r"正在|计划|准备|打算|将于|还在|仍在|未完成|没完成|还没|尚未开始|待定",
    "STATUS_DONE": r"已经|(?<!尚)已(?!被)|完成了|已完成|上线了|发布了|落地了",
    "CONDITION": r"如果|假如|只有|除非|前提|一旦|否则|只要|条件|才能|才可以|才会",
    "SCOPE": r"至少|超过|不到|不足|仅|只有|只|部分|其中|左右|最多|以上|以内|将近|接近|约",
    "ATTRIBUTION": r"认为|声称|宣称|表示|指出|据称|据|报告|提到|称|觉得|说法",
    "CAUSAL_STRONG": r"导致|造成|引起|使得|因为|所以|因此|致使",
    "CAUSAL_WEAK": r"有关|相关|关联|伴随|同时出现|共同出现",
}
FIDELITY_CRITICAL = ("negation_loss", "certainty_strengthened",
                     "status_changed", "attribution_loss")
NOOP_MAX_CHANGE = 0.15


def load_text(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    keep = []
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("<!--") or s.startswith(">"):
            continue
        keep.append(s)
    return "\n".join(keep)


def sentences_of(text):
    out = []
    for m in SENT_SPLIT.findall(text):
        s = m.strip()
        if s:
            out.append(s)
    return out


def clauses_of(text):
    return [c.strip() for c in CLAUSE_SPLIT.split(text) if len(c.strip()) >= 2]


def has_number(s):
    return bool(ARABIC.search(s)) or any(w in s for w in CN_SCALE)


def lexical_hits(sentences):
    hits = []
    for cat, pats in LEXICAL.items():
        for pat in pats:
            rx = re.compile(pat)
            for i, s in enumerate(sentences):
                for m in rx.finditer(s):
                    hits.append({"layer": "lexical", "category": cat,
                                 "sentence": i + 1, "excerpt": m.group(0)[:40]})
    return hits


def structural_hits(sentences, text):
    hits = []

    def add(name, idx, excerpt):
        hits.append({"layer": "structural", "category": name,
                     "sentence": idx + 1, "excerpt": excerpt[:46]})

    # Expectation -> Reversal (word-independent)
    for i, s in enumerate(sentences):
        if any(e in s for e in EXPECT_MARKERS) and any(r in s for r in REVERSAL_MARKERS):
            add("Expectation->Reversal", i, s)

    # Negation A -> Reveal B
    rx_neg = re.compile(r"(?:不是|并非|并不是)[^。！？\n]{0,25}(?:而是|更不是|它只是)")
    for i, s in enumerate(sentences):
        if rx_neg.search(s):
            add("Negation A->Reveal B", i, s)

    # Question -> Immediate Answer
    for i, s in enumerate(sentences):
        if s.rstrip().endswith(("？", "?")) and i + 1 < len(sentences):
            nxt = sentences[i + 1]
            if not nxt.rstrip().endswith(("？", "?")):
                add("Question->Immediate Answer", i, s + " / " + nxt)

    # Suspense Cue -> Fact (cue carries no new information itself)
    for i, s in enumerate(sentences):
        core = s.strip("。！？!?… ")
        if i + 1 < len(sentences) and any(c in s for c in SUSPENSE_CUES) \
                and not has_number(s) and len(core) <= 16:
            add("Suspense Cue->Fact", i, s)

    # Host Transition -> Fact
    for i, s in enumerate(sentences):
        head = s.lstrip("“\"’‘ ")
        if any(head.startswith(h) for h in HOST_STARTERS):
            add("Host Transition->Fact", i, head[:20])

    # Three-beat escalation / repeated parallelism (clause-prefix repetition)
    cl = clauses_of(text)
    for i in range(len(cl) - 2):
        pre = [c[:2] for c in cl[i:i + 3]]
        if len(set(pre)) == 1 and len(pre[0]) == 2:
            add("Three-beat Escalation", 0, "/".join(c[:8] for c in cl[i:i + 3]))
    # REFACTOR (v0.1.0, round 2): a repeated clause prefix alone is NOT
    # parallelism. A repeated technical subject ("蓝光 ... / 蓝光 ... / 蓝光 ...")
    # is normal Chinese exposition. Real parallelism also has near-equal clause
    # lengths, so only flag when the repeated clauses are close in length.
    # REFACTOR round 3: real parallelism is also LOCAL. Three same-prefix
    # clauses spread across a whole script is just a repeated subject, so the
    # occurrences must fall inside a window of 5 consecutive clauses.
    prefix_pos = {}
    for idx, c in enumerate(cl):
        prefix_pos.setdefault(c[:2], []).append((idx, len(c)))
    for pre, items in prefix_pos.items():
        for i in range(len(items) - 2):
            window = items[i:i + 3]
            span = window[-1][0] - window[0][0]
            lens = [n for _, n in window]
            if span <= 4 and (max(lens) - min(lens)) <= 6:
                hits.append({"layer": "structural",
                             "category": "Repeated Parallelism",
                             "sentence": 0,
                             "excerpt": "%s x3 (span %d, len %d-%d)"
                                        % (pre, span, min(lens), max(lens))})
                break

    # Repeated Contrast (density based)
    body = text.replace("\n", "")
    per100 = max(1.0, len(body) / 100.0)
    contrast = sum(body.count(m) for m in ("却", "然而", "反而", "相反"))
    if contrast / per100 > 1.2:
        hits.append({"layer": "structural", "category": "Repeated Contrast",
                     "sentence": 0, "excerpt": "contrast=%d/%.0f chars" % (contrast, len(body))})

    # Fact -> Artificial Philosophical Summary (ending check)
    for i in range(max(0, len(sentences) - 2), len(sentences)):
        s = sentences[i]
        if any(g in s for g in GRAND_WORDS) and not has_number(s):
            add("Fact->Artificial Philosophical Summary", i, s)

    # v0.2.0: Superiority Contrast（我 vs 你 的身份高低对立）
    for i, s in enumerate(sentences):
        if any(a in s for a in SUPERIORITY_SELF) \
                and any(b in s for b in SUPERIORITY_OTHER) \
                and any(g in s for g in SUPERIORITY_GAP):
            add("Superiority Contrast", i, s)

    # v0.2.0: Overclaim Promise（承诺结果且不带任何限定词）
    for i, s in enumerate(sentences):
        if any(p in s for p in PROMISE_WORDS) \
                and any(o in s for o in PROMISE_OUTCOME) \
                and not any(h in s for h in HEDGE_WORDS):
            add("Overclaim Promise", i, s)

    return hits


def rhythm_report(sentences, flagged):
    lens = [len(re.sub(r"[，,。；;！？!?、…\"“”‘’ ]", "", s)) for s in sentences]
    lens = [n for n in lens if n > 0]
    mean = statistics.mean(lens) if lens else 0.0
    std = statistics.pstdev(lens) if len(lens) > 1 else 0.0
    cv = (std / mean) if mean else 0.0

    def max_run(flags):
        best = run = 0
        for f in flags:
            run = run + 1 if f else 0
            best = max(best, run)
        return best

    short_run = max_run([n <= 9 for n in lens])
    climax_run = max_run(flagged)
    long_ratio = (sum(1 for n in lens if n > 45) / len(lens)) if lens else 0.0
    return {
        "sentences": len(sentences),
        "mean_len": round(mean, 1),
        "stdev_len": round(std, 1),
        "length_cv": round(cv, 3),
        "mechanical_uniformity": bool(len(lens) >= 6 and cv < 0.22),
        "max_short_run": short_run,
        "choppy": bool(short_run >= 4),
        "max_climax_run": climax_run,
        "climax_rewrite_trigger": bool(climax_run >= 3),
        "long_sentence_ratio": round(long_ratio, 2),
    }


def clamp(x, lo=0, hi=10):
    return max(lo, min(hi, x))


def story_report(sentences):
    """v0.2.0 故事层：内容是在解释，还是正在发生。"""
    total = max(1, len(sentences))

    def concrete(s):
        return (any(w in s for w in SCENE_MARKERS)
                or any(w in s for w in ACTION_VERBS)
                or any(w in s for w in TIME_MARKERS)
                or has_number(s))

    scene = sum(1 for s in sentences if any(w in s for w in SCENE_MARKERS))
    action = sum(1 for s in sentences if any(w in s for w in ACTION_VERBS))
    timed = sum(1 for s in sentences if any(w in s for w in TIME_MARKERS))
    numeric = sum(1 for s in sentences if has_number(s))
    abstract = sum(1 for s in sentences if any(w in s for w in ABSTRACT_WORDS))

    streak = best = 0
    for s in sentences:
        streak = 0 if concrete(s) else streak + 1
        best = max(best, streak)

    scene_r, action_r = scene / total, action / total
    time_r, num_r = timed / total, numeric / total
    abstract_r = abstract / total

    score = (min(3.0, scene_r * 12) + min(3.0, action_r * 8)
             + min(2.0, time_r * 8) + min(2.0, num_r * 6)
             - min(3.0, abstract_r * 10)
             - (1.0 if best >= 4 else 0.0))
    return {
        "scene_ratio": round(scene_r, 2),
        "action_ratio": round(action_r, 2),
        "time_ratio": round(time_r, 2),
        "number_ratio": round(num_r, 2),
        "abstract_ratio": round(abstract_r, 2),
        "max_abstract_streak": best,
        "no_scene": bool(scene == 0),
        "story_strength": clamp(int(round(score))),
    }


def _ngrams(s, n=4):
    s = re.sub(r"[\s\u3000\uff0c\u3002\uff01\uff1f\u3001\uff1a\uff1b]", "", s)
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def _unresolved_ref(s):
    """句子靠指代词支撑，却没有任何具体对象可以挂靠。"""
    if has_number(s):
        return False
    starts = s[:1] in REFERENCE_WORDS
    multi = sum(s.count(w) for w in REFERENCE_WORDS) >= 2
    concrete = (any(w in s for w in SCENE_MARKERS)
                or any(w in s for w in ACTION_VERBS))
    return bool((starts or multi) and not concrete)


def _aphorism_like(s):
    """短、泛指、无事实——可以直接截图的那种句子。"""
    if len(s) > 16 or has_number(s):
        return False
    if any(w in s for w in SCENE_MARKERS) or any(w in s for w in ACTION_VERBS):
        return False
    return any(w in s for w in GENERALIZING_WORDS)


def value_report(sentences):
    """v0.3.0 价值与清晰度层：这篇稿子到底交付了什么，听一遍能不能懂。

    脚本只判形式。「主判断是否明确」「证据是否支持判断」属于语义审稿，
    不写成数字（见 references/clarity-engine.md）。
    """
    total = max(1, len(sentences))
    generic = sum(1 for s in sentences if any(w in s for w in GENERIC_VALUE))
    vague = sum(1 for s in sentences if any(w in s for w in VAGUE_ACTION))
    boundary = sum(1 for s in sentences if any(w in s for w in BOUNDARY_MARKERS))
    abstract = sum(1 for s in sentences if any(w in s for w in ABSTRACT_WORDS))
    unresolved = sum(1 for s in sentences if _unresolved_ref(s))
    long_clause = sum(1 for s in sentences
                      for c in clauses_of(s) if len(c) > 28)
    concrete = sum(1 for s in sentences
                   if has_number(s)
                   or any(w in s for w in SCENE_MARKERS)
                   or any(w in s for w in ACTION_VERBS)
                   or any(w in s for w in TIME_MARKERS))
    action = sum(1 for s in sentences if any(w in s for w in ACTION_VERBS))

    run = best_run = 0
    for s in sentences:
        run = run + 1 if _aphorism_like(s) else 0
        best_run = max(best_run, run)

    repeated = 0
    grams = [_ngrams(s) for s in sentences]
    for i in range(len(grams)):
        for j in range(i + 1, len(grams)):
            if not grams[i] or not grams[j]:
                continue
            overlap = len(grams[i] & grams[j]) / min(len(grams[i]), len(grams[j]))
            if overlap > 0.6:
                repeated += 1
                break

    concrete_r, abstract_r = concrete / total, abstract / total
    score = (3.0
             + min(3.0, concrete_r * 5)
             + min(2.0, boundary * 1.0)
             + (1.0 if action >= 1 else 0.0)
             - min(4.0, generic * 2.0)
             - min(3.0, vague * 1.5)
             - min(2.0, abstract_r * 5)
             - (1.0 if long_clause >= 2 else 0.0)
             - (1.5 if best_run >= 3 else 0.0)
             - (1.0 if repeated >= 1 else 0.0)
             - (1.0 if unresolved >= 3 else 0.0))
    return {
        "generic_value": generic,
        "vague_action": vague,
        "boundary_marker": boundary,
        "unresolved_ref": unresolved,
        "long_clause": long_clause,
        "aphorism_run": best_run,
        "repeated_conclusion": repeated,
        "abstract_term_density": round(abstract_r, 2),
        "concrete_ratio": round(concrete_r, 2),
        "value_strength": clamp(int(round(score))),
    }


def evidence_report(sentences):
    """v0.4.0：检查证据是否承担推论作用，以及现实类比是否越界。"""
    evidence = sum(1 for x in sentences if has_number(x) or any(w in x for w in EVIDENCE_MARKERS))
    inference = sum(1 for x in sentences if any(w in x for w in INFERENCE_MARKERS))
    boundary = sum(1 for x in sentences if any(w in x for w in EVIDENCE_BOUNDARY))
    overreach = sum(1 for x in sentences if any(w in x for w in ANALOGY_OVERREACH))
    unsourced = sum(1 for x in sentences
                    if UNSOURCED_AUTHORITY.search(x) and not SOURCE_SPECIFIC.search(x))
    score = min(4, evidence) + min(3, inference) + min(2, boundary) + (1 if evidence and inference else 0) - min(6, overreach * 3)
    return {
        "evidence_units": evidence,
        "inference_links": inference,
        "boundary_markers": boundary,
        "analogy_overreach": overreach,
        "unsourced_authority": unsourced,
        "evidence_strength": clamp(int(round(score))),
    }

def scan(path, story_gate=False, value_gate=False, evidence_gate=False):
    text = load_text(path)
    sents = sentences_of(text)
    lex = lexical_hits(sents)
    stru = structural_hits(sents, text)
    flagged = [False] * len(sents)
    for h in lex + stru:
        idx = h["sentence"] - 1
        if 0 <= idx < len(sents):
            flagged[idx] = True
    rhythm = rhythm_report(sents, flagged)
    story = story_report(sents)
    value = value_report(sents)
    evidence = evidence_report(sents)

    body = text.replace("\n", "")
    per100 = max(1.0, len(body) / 100.0)
    lex_density = len(lex) / per100
    stru_density = len(stru) / per100

    cliche = clamp(round(lex_density * 3.2))
    ai_pattern = clamp(round(stru_density * 3.2
                             + (2 if rhythm["climax_rewrite_trigger"] else 0)
                             + (1 if rhythm["mechanical_uniformity"] else 0)
                             + (1 if rhythm["choppy"] else 0)))
    naturalness = clamp(round(10 - 0.7 * cliche - 0.7 * ai_pattern
                              - (1 if rhythm["choppy"] else 0)))
    clarity = 10
    if rhythm["mean_len"] > 34:
        clarity -= 2
    if rhythm["long_sentence_ratio"] > 0.15:
        clarity -= 1
    if rhythm["mean_len"] and rhythm["mean_len"] < 7:
        clarity -= 1
    # v0.3.0 清晰度引擎：一句一任务 + 指代检查（轻度惩罚，不抢旧门禁的权重）
    if value["long_clause"] >= 2:
        clarity -= 1
    if value["unresolved_ref"] >= 3:
        clarity -= 1
    # v0.5.0 中文补充检查：长定语、“进行+动词”名词化（轻度惩罚）
    long_attr = sum(1 for c in clauses_of(text) if len(c) >= 22 and c.count("的") >= 3)
    jinxing = sum(len(JINXING_VERB.findall(x)) for x in sents)
    if long_attr >= 2:
        clarity -= 1
    if jinxing >= 2:
        clarity -= 1
    clarity = clamp(clarity)
    head = "".join(sents[:2])
    hook = 4 + (3 if has_number(head) else 0) + \
        (2 if re.search(r"(摄氏度|度|倍|米|公里|年|微秒|秒|亿|万)", head) else 0)
    hook = clamp(hook)

    by_cat = {}
    for h in lex + stru:
        by_cat[h["category"]] = by_cat.get(h["category"], 0) + 1

    # v0.2.0: 说服腔属于零容忍项，命中即 FAIL（与配额分开）
    overclaim = sum(n for c, n in by_cat.items()
                    if c in ("H_overclaim_persuasion", "Overclaim Promise",
                             "Superiority Contrast"))
    passed = (naturalness >= 8 and cliche <= 2 and ai_pattern <= 2
              and clarity >= 8 and overclaim == 0)
    if story_gate and story["story_strength"] < 6:
        passed = False
    # v0.3.0 价值门禁：空泛价值句零容忍，模糊行动词最多 1 处
    if value_gate and (value["value_strength"] < 6
                       or value["generic_value"] > 0
                       or value["vague_action"] > 1):
        passed = False
    if evidence_gate and (evidence["evidence_strength"] < 6
                          or evidence["analogy_overreach"] > 0
                          or evidence["unsourced_authority"] > 0):
        passed = False
    return {
        "file": path,
        "chars": len(body),
        "counts": {"lexical": len(lex), "structural": len(stru)},
        "by_category": by_cat,
        "rhythm": rhythm,
        "story": story,
        "value": value,
        "evidence": evidence,
        "chinese_editorial": {"long_attributive": long_attr, "jinxing_verb": jinxing},
        "overclaim_hits": overclaim,
        "story_gate": bool(story_gate),
        "value_gate": bool(value_gate),
        "evidence_gate": bool(evidence_gate),
        "scores": {"naturalness": naturalness, "cliche_risk": cliche,
                   "ai_pattern_risk": ai_pattern, "clarity": clarity,
                   "hook_strength": hook,
                   "story_strength": story["story_strength"],
                   "value_strength": value["value_strength"],
                   "evidence_strength": evidence["evidence_strength"]},
        "verdict": "PASS" if passed else "FAIL",
        "hits": lex + stru,
    }


def info_preservation(before_path, after_path):
    b, a = load_text(before_path), load_text(after_path)
    tokens = ARABIC.findall(b) + [w for w in CN_SCALE if w in b]
    missing = sorted({t for t in tokens if t not in a})
    score = clamp(10 - 2 * len(missing))
    return {"baseline": before_path, "after": after_path,
            "fact_tokens_in_baseline": sorted(set(tokens)),
            "missing_in_after": missing,
            "information_preservation": score,
            "verdict": "PASS" if score >= 9 else "FAIL"}


# v0.8.0：“已经 + 时长 / 数量 / 程度”是描述，不是完成事件，不计入 STATUS_DONE
DONE_FALSE_POSITIVE = re.compile(
    r"已经(?=(?:有|过了|超过|快|将近|整整)?[0-9一二三四五六七八九十百千万两几半]+多?"
    r"(?:年|个月|月|天|周|个?小时|分钟|岁|代|次|件|个|万|千|百)|很|足够|相当|十分|非常|挺)")


def _anchor_counts(text):
    out = {k: len(re.findall(v, text)) for k, v in FIDELITY_GROUPS.items()}
    out["STATUS_DONE"] = len(re.findall(FIDELITY_GROUPS["STATUS_DONE"],
                                        DONE_FALSE_POSITIVE.sub("", text)))
    return out


def _norm(s):
    return re.sub("[\\s，。！？、；：,.!?;:“”‘’\"']", "", s)


def protected_lines_report(protect_path, after_path):
    """v0.8.0：好句保护。protect 文件每行一句，改写后必须原样存在（忽略标点空白）。"""
    with open(protect_path, encoding="utf-8") as fh:
        lines = [l.strip() for l in fh if l.strip() and not l.strip().startswith("#")]
    after = _norm(load_text(after_path))
    lost = [l for l in lines if _norm(l) not in after]
    return {"protected": len(lines), "lost": lost,
            "verdict": "PASS" if not lost else "FAIL"}


def fidelity_report(before_path, after_path):
    """v0.5.0：语义保真层。比较改写前后七类语义锚点，找出被删、被强化或被改写的含义。"""
    b_text, a_text = load_text(before_path), load_text(after_path)
    b, a = _anchor_counts(b_text), _anchor_counts(a_text)
    numbers = info_preservation(before_path, after_path)
    issues = {
        "number_loss": len(numbers["missing_in_after"]),
        "negation_loss": max(0, b["NEGATION"] - a["NEGATION"]),
        "certainty_strengthened": max(0, a["CERTAINTY"] - b["CERTAINTY"])
        + max(0, b["MODALITY"] - a["MODALITY"]),
        "status_changed": max(0, b["STATUS_PENDING"] - a["STATUS_PENDING"])
        + max(0, a["STATUS_DONE"] - b["STATUS_DONE"]),
        "condition_loss": max(0, b["CONDITION"] - a["CONDITION"]),
        "scope_loss": max(0, b["SCOPE"] - a["SCOPE"]),
        "attribution_loss": max(0, b["ATTRIBUTION"] - a["ATTRIBUTION"]),
        "causal_upgrade": (max(0, a["CAUSAL_STRONG"] - b["CAUSAL_STRONG"])
                           if b["CAUSAL_WEAK"] > a["CAUSAL_WEAK"] else 0),
    }
    bad = [k for k, v in issues.items() if v > 0]
    score = clamp(10 - 2 * len(bad))
    critical = sum(issues[k] for k in FIDELITY_CRITICAL)
    change = 1 - SequenceMatcher(None, b_text, a_text).ratio()
    return {"baseline": before_path, "after": after_path,
            "anchors_before": b, "anchors_after": a,
            "issues": issues, "failed_checks": bad,
            "critical_issues": critical,
            "semantic_fidelity": score,
            "change_ratio": round(change, 3),
            "verdict": "PASS" if score >= 9 and critical == 0 else "FAIL"}


def print_report(r, quiet=False):
    s = r["scores"]
    print("=" * 72)
    print("FILE: %s  (%d chars, %d sentences)" % (r["file"], r["chars"], r["rhythm"]["sentences"]))
    print("lexical hits: %d | structural hits: %d" % (r["counts"]["lexical"], r["counts"]["structural"]))
    if r["by_category"]:
        for cat, n in sorted(r["by_category"].items(), key=lambda kv: -kv[1]):
            print("   - %-42s %d" % (cat, n))
    rh = r["rhythm"]
    print("rhythm: mean=%.1f cv=%.2f short_run=%d climax_run=%d uniform=%s choppy=%s"
          % (rh["mean_len"], rh["length_cv"], rh["max_short_run"], rh["max_climax_run"],
             rh["mechanical_uniformity"], rh["choppy"]))
    st = r["story"]
    print("story: scene=%.2f action=%.2f time=%.2f abstract=%.2f streak=%d strength=%d"
          % (st["scene_ratio"], st["action_ratio"], st["time_ratio"],
             st["abstract_ratio"], st["max_abstract_streak"], st["story_strength"]))
    va = r["value"]
    print("value: generic=%d vague=%d boundary=%d ref=%d long_clause=%d "
          "aphorism_run=%d repeat=%d strength=%d"
          % (va["generic_value"], va["vague_action"], va["boundary_marker"],
             va["unresolved_ref"], va["long_clause"], va["aphorism_run"],
             va["repeated_conclusion"], va["value_strength"]))
    ev = r["evidence"]
    print("evidence: units=%d inference=%d boundary=%d overreach=%d unsourced=%d strength=%d"
          % (ev["evidence_units"], ev["inference_links"], ev["boundary_markers"],
             ev["analogy_overreach"], ev["unsourced_authority"], ev["evidence_strength"]))
    ce = r["chinese_editorial"]
    print("editorial: long_attributive=%d jinxing_verb=%d"
          % (ce["long_attributive"], ce["jinxing_verb"]))
    print("scores: Naturalness=%d Cliche=%d AIPattern=%d Clarity=%d Hook=%d "
          "Story=%d Value=%d Evidence=%d overclaim=%d -> %s"
          % (s["naturalness"], s["cliche_risk"], s["ai_pattern_risk"],
             s["clarity"], s["hook_strength"], s["story_strength"],
             s["value_strength"], s["evidence_strength"], r["overclaim_hits"], r["verdict"]))
    if not quiet:
        for h in r["hits"][:14]:
            print("      [%s] %s :: %s" % (h["layer"][:4], h["category"], h["excerpt"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--baseline")
    ap.add_argument("--after")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--story-gate", action="store_true",
                    help="叙事 / 人物 / 纪录片 / 方法论类任务：Story Strength >= 6 才 PASS")
    ap.add_argument("--value-gate", action="store_true",
                    help="方法论 / 商业 / 成长 / 慢创业类题材：Value Strength >= 6 且无空泛价值句才 PASS")
    ap.add_argument("--evidence-gate", action="store_true",
                    help="科普 / 历史 / 人物 / 纪录片：Evidence Strength >= 6、无类比越界、无无来源权威才 PASS")
    ap.add_argument("--fidelity-gate", action="store_true",
                    help="v0.5.0 CLEAN：Semantic Fidelity >= 9 且否定 / 确定性 / 状态 / 归因零问题才 PASS（需 --baseline 与 --after）")
    ap.add_argument("--protect",
                    help="v0.8.0 好句保护：每行一句必须在 --after 中原样保留，丢失即 FAIL")
    ap.add_argument("--noop-gate", action="store_true",
                    help="v0.5.0：原稿已通顺时，改动比例 <= 0.15 且语义保真 PASS 才 PASS")
    args = ap.parse_args()

    results = [scan(p, story_gate=args.story_gate, value_gate=args.value_gate,
                    evidence_gate=args.evidence_gate) for p in args.files]
    compare = None
    fidelity = None
    exit_code = 0
    if args.baseline and args.after:
        compare = info_preservation(args.baseline, args.after)
        fidelity = fidelity_report(args.baseline, args.after)
        if args.noop_gate and fidelity["change_ratio"] > NOOP_MAX_CHANGE:
            fidelity["verdict"] = "FAIL"
            fidelity["noop_violation"] = True
        if args.protect:
            fidelity["protected_lines"] = protected_lines_report(args.protect, args.after)
            if fidelity["protected_lines"]["lost"]:
                fidelity["verdict"] = "FAIL"
        if (args.fidelity_gate or args.noop_gate or args.protect) and fidelity["verdict"] == "FAIL":
            exit_code = 1
    elif args.fidelity_gate or args.noop_gate:
        print("ERROR: --fidelity-gate / --noop-gate need --baseline and --after")
        return 2

    if args.json:
        print(json.dumps({"results": results, "compare": compare, "fidelity": fidelity},
                         ensure_ascii=False, indent=2))
    else:
        for r in results:
            print_report(r, args.quiet)
        if compare:
            print("=" * 72)
            print("INFORMATION PRESERVATION: %d/10 (%s)"
                  % (compare["information_preservation"], compare["verdict"]))
            print("missing fact tokens: %s" % (compare["missing_in_after"] or "none"))
        if fidelity:
            print("SEMANTIC FIDELITY: %d/10 critical=%d change_ratio=%.3f (%s)"
                  % (fidelity["semantic_fidelity"], fidelity["critical_issues"],
                     fidelity["change_ratio"], fidelity["verdict"]))
            print("fidelity issues: %s" % (", ".join("%s=%d" % (k, fidelity["issues"][k])
                                                   for k in fidelity["failed_checks"]) or "none"))
            if fidelity.get("protected_lines"):
                pl = fidelity["protected_lines"]
                print("PROTECTED LINES: %d locked, %d lost (%s)" % (pl["protected"], len(pl["lost"]), pl["verdict"]))
                for l in pl["lost"]:
                    print("   LOST: %s" % l)
            if fidelity.get("noop_violation"):
                print("NO-OP VIOLATION: change_ratio > %.2f" % NOOP_MAX_CHANGE)
        if results:
            fails = [r["file"] for r in results if r["verdict"] == "FAIL"]
            print("=" * 72)
            print("SUMMARY: %d files, %d PASS, %d FAIL"
                  % (len(results), len(results) - len(fails), len(fails)))
            for f in fails:
                print("   FAIL: %s" % f)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
