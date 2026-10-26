#!/usr/bin/env python3
"""Mechanical scorer for xu-reliability-design eval runs.

Usage:
  aggregate.py --run-dir RUN --evals evals.json [--judge-dir RUN/judge] [--as-of YYYY-MM-DD]
               [--skill-dir DIR]

RUN/cases.json: one row per case; each response label maps either to a version string
  ("old" = seven-question skill, "new" = eight-question skill) with condition "routed", or to
  {"version": "old|new|none", "condition": "routed|main-only|noskill"}.
RUN/out/<case>-<label>.md and .meta.json ({"files_read": [...], "selected_questions": [...]}).
RUN/judge/<case>.json: judge output per evals/rubric.md (content scores; raw selections fallback).

Rules (mirror EVALS.md):
- material selected = TP; optional = neither; anything else = FP; missing material = FN.
- label map, seven-question versions only, never for no-skill: when gold Q8 is material a selected
  Q7 also satisfies Q8 and leaves the FP set unless Q7 is itself material or optional; when gold
  Q8 is optional a selected Q7 is untallied; otherwise labels are scored as written.
- empty-gold cases: P = R = 1.0 when nothing is selected, else 0.0. When material questions exist
  and none is selected, P = 0.0.
- selections come from the meta file; if absent, from the judge's reported set; a meta without the
  key, a files_read path that does not exist, and an unknown version or condition are errors.
- --as-of reverts gold_history entries whose effective_from is later than the date; it errors when
  a reported case has a non-relabel entry in force that was recorded on or after the as-of date
  (frozen-gold rule), and warns when replayed must_cover wording differs from what the judges saw.
- a routed run is flagged when files_read contains a route file for a question that is not in
  selected_questions (the 2026-09-01 all-routes mislabel).
- summaries are macro per (condition, version, set); every skipped response and every row without
  a context count is printed; the decision-quality gate is evaluated per set when a noskill
  condition exists.
"""
import argparse, datetime as dt, json, math, os, statistics as st

VERSIONS = {"old": "seven-question taxonomy", "new": "eight-question taxonomy", "none": "no skill"}
CONDITIONS = {"routed", "main-only", "noskill"}

def golds_as_of(evals, as_of, reported):
    out, warn = {}, []
    today = dt.date.today().isoformat()
    for e in evals["evals"]:
        mat, opt, mc = list(e["gold"]["material"]), list(e["gold"]["optional"]), list(e["gold"]["must_cover"])
        for h in e.get("gold_history", []):
            if not as_of and e["case"] in reported and h["effective_from"] > today:
                warn.append(f"{e['case']}: gold entry {h['question']} is dated {h['effective_from']}, later than today; pass --as-of to score under a defined gold")
            in_force = h["effective_from"] <= as_of if as_of else True
            if h.get("kind", "change") != "relabel" and "recorded_on" not in h:
                raise SystemExit(f"{e['case']}: gold_history entry {h['question']} has no recorded_on; the frozen-gold guard cannot run")
            if as_of and e["case"] in reported and in_force and h.get("kind", "change") != "relabel" and h["recorded_on"] >= as_of:
                raise SystemExit(f"frozen-gold rule: {e['case']} is reported in this run but its gold change {h['question']} (effective {h['effective_from']}) was recorded on {h.get('recorded_on')}, not before the round (as-of {as_of})")
        if as_of:
            for h in reversed(e.get("gold_history", [])):
                if h["effective_from"] > as_of:
                    mat, opt = list(h["previous_material"]), list(h["previous_optional"])
            for h in reversed(e.get("must_cover_history", [])):
                if h["effective_from"] > as_of:
                    mc = list(h["previous_must_cover"])
        out[e["case"]] = dict(material=mat, optional=opt, must_cover=mc, boundary=e.get("boundary", False), set=e.get("set"))
    return out, warn

ROUTE_Q = {"q1-intent": "Q1", "q2-state": "Q2", "q3-change": "Q3", "q4-seams": "Q4", "q5-correctness": "Q5",
           "q6-control": "Q6", "q7-fidelity": "Q7", "q7-evidence": "Q7", "q8-diagnosability": "Q8"}

def selections(md, meta, judge, label, run_dir, skill_dir):
    if os.path.exists(meta):
        d = json.load(open(meta))
        if "selected_questions" not in d:
            raise SystemExit(f"{meta}: missing selected_questions")
        if "files_read" not in d or not d["files_read"]:
            return set(d["selected_questions"]), None, []
        loaded = 0
        known = set(d["selected_questions"]) | set(d.get("unknown_questions", []))
        extra = sorted({q for f in d["files_read"] for stem, q in ROUTE_Q.items() if stem in os.path.basename(f) and q not in known})
        for f in d["files_read"]:
            cands = [f] if os.path.isabs(f) else [os.path.join(x, f) for x in ([skill_dir] if skill_dir else []) + [run_dir]]
            hit = next((c for c in cands if os.path.exists(c)), None)
            if hit is None:
                raise SystemExit(f"{meta}: files_read path does not exist: {f}")
            loaded += len(open(hit).read().split())
        return set(d["selected_questions"]), loaded, extra
    if judge and label in judge.get("responses", {}) and "selected" in judge["responses"][label]:
        return set(judge["responses"][label]["selected"]), None, []
    raise SystemExit(f"no selection source for {md}")

def score(sel, gold, version, condition):
    mat, opt = set(gold["material"]), set(gold["optional"]); eff = set(sel); untallied = set()
    if version == "old" and condition != "noskill" and "Q7" in eff:
        if "Q8" in mat:
            eff.add("Q8")
            if "Q7" not in mat | opt:
                eff.discard("Q7")
        elif "Q8" in opt and "Q7" not in mat | opt:
            eff.discard("Q7"); untallied.add("Q7")
    tp = mat & eff
    fp = sorted(q for q in eff if q not in mat and q not in opt)
    fn = sorted(mat - eff)
    if not mat:
        P = R = (1.0 if not eff else 0.0)
    else:
        P = round(len(tp) / (len(tp) + len(fp)), 2) if (tp or fp) else 0.0
        R = round(len(tp) / len(mat), 2)
    return P, R, fn, fp, sorted(untallied)

def parse_label(v):
    if isinstance(v, str):
        return v, "routed"
    return v["version"], v.get("condition", "routed")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True); ap.add_argument("--evals", required=True)
    ap.add_argument("--judge-dir"); ap.add_argument("--as-of"); ap.add_argument("--skill-dir")
    a = ap.parse_args()
    cases = {c["case"]: c for c in json.load(open(os.path.join(a.run_dir, "cases.json")))}
    evals = json.load(open(a.evals))
    golds, warns = golds_as_of(evals, a.as_of, set(cases))
    for w in warns:
        print("WARNING:", w)
    if a.as_of:
        current = {e["case"]: e["gold"]["must_cover"] for e in evals["evals"]}
        drift = [c for c in cases if golds[c]["must_cover"] != current[c]]
        if drift:
            print(f"WARNING: must_cover wording as of {a.as_of} differs from the current wording the judges scored for {drift}; coverage columns reflect current wording")
    jdir = a.judge_dir or os.path.join(a.run_dir, "judge")
    rows = []
    for case, m in cases.items():
        g = golds[case]
        jp = os.path.join(jdir, case + ".json")
        judge = json.load(open(jp)) if os.path.exists(jp) else None
        for label in [k for k in m if len(k) == 1 and k.isupper()]:
            ver, cond = parse_label(m[label])
            if ver not in VERSIONS or cond not in CONDITIONS:
                raise SystemExit(f"cases.json: unknown version/condition {m[label]!r} for {case}/{label}")
            md = os.path.join(a.run_dir, "out", f"{case}-{label}.md")
            meta = os.path.join(a.run_dir, "out", f"{case}-{label}.meta.json")
            if not os.path.exists(md):
                print(f"WARNING: skipped {case}-{label} ({ver}/{cond}): no response file"); continue
            sel, loaded, extra = selections(md, meta, judge, label, a.run_dir, a.skill_dir)
            if loaded is None:
                print(f"WARNING: {case}-{label} ({ver}/{cond}) has no context count; excluded from the context gate")
            if cond == "routed" and extra:
                print(f"WARNING: {case}-{label} ({ver}/routed) loaded route files for unselected questions {extra}; routed integrity flag")
            P, R, fn, fp, unt = score(sel, g, ver, cond)
            row = dict(case=case, set=g["set"], ver=ver, cond=cond, label=label, sel=sorted(sel), fn=fn, fp=fp, unt=unt, route_extra=extra,
                       P=P, R=R, loaded=loaded, words=len(open(md).read().split()), boundary=g["boundary"],
                       chains=None, chains_done=0, chains_total=0, dq=None, miss=0, hit=0, must_not=0,
                       flags=0, prov=None, jfp=0, winner=None)
            if judge:
                r = judge["responses"].get(label, {})
                ch = r.get("complete_chains")
                if isinstance(ch, str) and "/" in ch:
                    x, _ = ch.split("/"); row["chains_total"] = 3 if g["material"] else 0
                    row["chains_done"] = min(int(x), row["chains_total"])
                dq = (r.get("decision") or {}).get("total")
                row.update(chains=ch, dq=(dq if g["material"] and isinstance(dq, (int, float)) else None),
                           miss=len((r.get("must_cover") or {}).get("miss", [])),
                           hit=len((r.get("must_cover") or {}).get("hit", [])),
                           must_not=len(r.get("must_not_violated", [])), flags=len(r.get("boundary_flags", [])),
                           prov=(r.get("provenance") if isinstance(r.get("provenance"), str)
                                 else ("error" if r.get("provenance_errors") else "unverified")),
                           jfp=len(r.get("justified_fp", [])))
                pref = judge.get("preference")
                row["winner"] = parse_label(m[pref])[0] if pref in m else "tie"
            rows.append(row)
    print(f"{'case':4} {'set':8} {'ver':4} {'cond':9} {'selected':18} {'FN':6} {'FP':8} {'unt':4} {'P':>4} {'R':>4} {'chains':>6} {'dq':>3} {'miss':>4} {'mnot':>4} {'flag':>4} {'jfp':>3} {'prov':>10} {'loaded':>6} {'words':>5} win")
    for r in sorted(rows, key=lambda r: (r["case"], r["cond"], r["ver"])):
        print(f"{r['case']:4} {str(r['set']):8} {r['ver']:4} {r['cond']:9} {','.join(r['sel']) or '-':18} {','.join(r['fn']) or '-':6} {','.join(r['fp']) or '-':8} {','.join(r['unt']) or '-':4} {str(r['P']):>4} {str(r['R']):>4} {str(r['chains'] or '-'):>6} {str(r['dq'] if r['dq'] is not None else '-'):>3} {r['miss']:>4} {r['must_not']:>4} {r['flags']:>4} {r['jfp']:>3} {str(r['prov'] or '-')[:10]:>10} {str(r['loaded']):>6} {r['words']:>5} {r['winner'] or '-'}")
    def mean(xs):
        xs = [x for x in xs if isinstance(x, (int, float))]; return round(st.mean(xs), 2) if xs else None
    def p90(xs):
        xs = sorted(x for x in xs if isinstance(x, (int, float)))
        return xs[math.ceil(0.9 * len(xs)) - 1] if xs else None
    print()
    keys = sorted(set((r["cond"], r["ver"]) for r in rows))
    sets = sorted(set(str(r["set"]) for r in rows))
    for cond, ver in keys:
        for st_ in [None] + sets:
            rs = [r for r in rows if r["cond"] == cond and r["ver"] == ver and (st_ is None or str(r["set"]) == st_)]
            if not rs:
                continue
            b = [r for r in rs if r["boundary"]]
            loaded = [r["loaded"] for r in rs if r["loaded"] is not None]
            cd, ct = sum(r["chains_done"] for r in rs), sum(r["chains_total"] for r in rs)
            prov_err = sum(1 for r in rs if (r["prov"] or "").startswith("error"))
            prov_unv = sum(1 for r in rs if r["prov"] == "unverified")
            print(f"{cond}/{ver}{'/' + st_ if st_ else ' (all sets)'}: n={len(rs)} P={mean([r['P'] for r in rs])} R={mean([r['R'] for r in rs])} "
                  f"boundaryP={mean([r['P'] for r in b])} boundaryR={mean([r['R'] for r in b])} "
                  f"chains={cd}/{ct}={round(cd/ct,2) if ct else None} dq={mean([r['dq'] for r in rs])} (n_dq={sum(1 for r in rs if r['dq'] is not None)}) "
                  f"must_cover_miss={sum(r['miss'] for r in rs)} must_not={sum(r['must_not'] for r in rs)} "
                  f"flags={sum(r['flags'] for r in rs)} justified_fp={sum(r['jfp'] for r in rs)} untallied={sum(len(r['unt']) for r in rs)} "
                  f"prov_errors={prov_err} prov_unverified={prov_unv} "
                  f"loaded_median={st.median(loaded) if loaded else None} loaded_p90={p90(loaded)} (n_context={len(loaded)}) "
                  f"words={mean([r['words'] for r in rs])} routed_integrity_flags={sum(1 for r in rs if r['route_extra'])} preference_wins={sum(1 for r in rs if r['winner']==ver)}")
    noskill = [r for r in rows if r["cond"] == "noskill"]
    if not noskill:
        print("decision gate: not evaluated (no noskill condition in this run)")
    else:
        for st_ in [None] + sets:
            for ver in sorted(set(r["ver"] for r in rows if r["cond"] == "routed")):
                nsr = {r["case"]: r for r in noskill if r["dq"] is not None and (st_ is None or str(r["set"]) == st_)}
                rdr = {r["case"]: r for r in rows if r["cond"] == "routed" and r["ver"] == ver and r["dq"] is not None and (st_ is None or str(r["set"]) == st_)}
                paired = sorted(set(nsr) & set(rdr))
                if not paired:
                    print(f"decision gate routed/{ver}{'/' + st_ if st_ else ' (all sets)'}: not evaluated (no case scored in both conditions)"); continue
                if set(nsr) != set(rdr):
                    print(f"decision gate routed/{ver}{'/' + st_ if st_ else ' (all sets)'}: refused, conditions cover different cases (paired {len(paired)}, noskill-only {sorted(set(nsr)-set(rdr))}, routed-only {sorted(set(rdr)-set(nsr))})"); continue
                ns = mean([nsr[c]["dq"] for c in paired]); rd = mean([rdr[c]["dq"] for c in paired])
                verdict = ("gate void: no-skill mean above 8.5, case set lacks headroom" if ns > 8.5
                           else ("pass" if rd >= 8.0 and rd - ns >= 1.0 else "fail"))
                print(f"decision gate routed/{ver}{'/' + st_ if st_ else ' (all sets)'}: routed={rd} noskill={ns} delta={round(rd - ns, 2)} -> {verdict}")

if __name__ == "__main__":
    main()
