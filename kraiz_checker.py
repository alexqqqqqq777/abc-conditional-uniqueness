#!/usr/bin/env python3
"""
kraiz_checker.py — v4   (2025-06-05)

Поиск контрпримеров к Гипотезе Крайза:  A^x + B^y = C^z  (x,y,z>1)
• канонизация (A,x)↔(B,y) — перестановки не дают «фиктивных» дублей
• near-miss  |Δ| ≤ δ  (опция -d)
• диапазоны по A,B,C, x,y, z, лог-окно  log(B)/log(A)
• подробно пишет всё в файл-лог, на экран — краткую сводку
• код выхода 0 — гипотеза выдержала, 1 — найден контрпример
"""

from __future__ import annotations
import argparse, math, sys, time, datetime, pathlib
from collections import defaultdict
from typing import Dict, List, Tuple

# ───────────────── helpers ────────────────────────────────────────────────
def is_perfect_power(n: int) -> bool:
    if n <= 1:
        return False
    k_max = int(math.log2(n))
    for k in range(2, k_max + 1):
        r = round(n ** (1.0 / k))
        if r > 1 and r ** k == n:
            return True
    return False

def build_powtab(bases: List[int], z_lim: int):
    tab = defaultdict(list)                    # value → [(C,z), …]
    for c in bases:
        for z in range(2, z_lim + 1):
            tab[c ** z].append((c, z))
    return tab

def canon(rec: Tuple[int,int,int,int,int,int]):
    """Инвариантное представление решения (A,x)+(B,y)=C^z."""
    A,x,B,y,C,z = rec
    if (A,x) <= (B,y):
        return ((A,x), (B,y), C, z)
    return ((B,y), (A,x), C, z)

# ───────────────── scan ───────────────────────────────────────────────────
def scan(cfg, loud=False):
    bases = [n for n in range(cfg["min_b"], cfg["max_b"]+1)
             if not is_perfect_power(n)]
    powtab = build_powtab(bases, cfg["z_lim"])

    ordered, near = [], []
    total = len(bases)**2 * (cfg["max_e"]-1)**2
    t0, step, cnt = time.time(), max(total//200, 1), 0

    for A in bases:
        for x in range(2, cfg["max_e"]+1):
            Ax = A**x
            for B in bases:
                if B == A:            # симметрия сокращает половину
                    continue
                if cfg["win"]:
                    r = math.log(B)/math.log(A)
                    if not cfg["win"][0] <= r <= cfg["win"][1]:
                        continue
                for y in range(2, cfg["max_e"]+1):
                    S = Ax + B**y
                    # exact
                    if S in powtab:
                        for C,z in powtab[S]:
                            if C in (A,B): continue
                            if cfg["filt_z"] and z != cfg["filt_z"]: continue
                            ordered.append((A,x,B,y,C,z))
                    # near-miss
                    if cfg["delta"]:
                        for d in range(1, cfg["delta"]+1):
                            for s in (-1,1):
                                S2 = S + s*d
                                if S2 in powtab:
                                    for C,z in powtab[S2]:
                                        if C in (A,B): continue
                                        if cfg["filt_z"] and z != cfg["filt_z"]:
                                            continue
                                        near.append((A,x,B,y,C,z,s*d))
                    # progress
                    cnt += 1
                    if loud and cnt % step == 0:
                        pct  = 100*cnt/total
                        rate = cnt / (time.time()-t0+1e-9)
                        print(f"\r{pct:5.1f}%  {rate:,.0f} it/s", end="", flush=True)
    if loud: print("\r100.0%  done".ljust(40))
    return ordered, near, total

# ───────────────── analyse & log ──────────────────────────────────────────
def analyse(ordered):
    triples: Dict[frozenset,set] = defaultdict(set)   # {A,B,C}→{canon_sol}
    for rec in ordered:
        triples[frozenset((rec[0],rec[2],rec[4]))].add(canon(rec))
    multi = {k:v for k,v in triples.items() if len(v)>1}
    return triples, multi

def dump_log(path: pathlib.Path, cfg, triples, near):
    with path.open("w", encoding="utf-8") as f:
        f.write("# Kraiz checker full log\n")
        f.write(f"Generated: {datetime.datetime.now()}\n")
        f.write(json_header(cfg))
        f.write("\n== Exact solutions ==\n")
        for trio, sols in triples.items():
            f.write(f"{sorted(trio)}\n")
            for (A,x),(B,y),C,z in sols:
                f.write(f"  {A}^{x} + {B}^{y} = {C}^{z}\n")
        if near:
            f.write("\n== Near-miss (|Δ|≤δ) ==\n")
            for A,x,B,y,C,z,d in near:
                sign="+" if d>0 else "-"
                f.write(f"{A}^{x}+{B}^{y} = {C}^{z} {sign}{abs(d)}\n")

def json_header(cfg):
    import json, textwrap
    return textwrap.indent(json.dumps(cfg, indent=2, ensure_ascii=False), "  ") + "\n"

def summary(cfg, total, triples, multi, near, outfile):
    print("\n── SUMMARY ─────────────────────────────────────────")
    print(f"range A,B,C : {cfg['min_b']} … {cfg['max_b']}")
    print(f"range x,y   : 2 … {cfg['max_e']}")
    if cfg["filt_z"]:
        print(f"fixed z     : {cfg['filt_z']}")
    else:
        print(f"range z     : 2 … {cfg['z_lim']}")
    if cfg["win"]:
        lo,hi = cfg["win"]; print(f"log-window  : {lo} … {hi}")
    print(f"checked (ordered) combos : {total:,}")
    print(f"unique {{A,B,C}} triples : {len(triples):,}")
    print(f"triples with >1 solution : {len(multi):,}")
    print(f"log written to           : {outfile}")

    if multi:
        print("\n‼ counter-example(s) found!")
        for trio, sols in multi.items():
            print(" ", sorted(trio))
            for (A,x),(B,y),C,z in sols:
                print(f"   {A}^{x}+{B}^{y}={C}^{z}")
        sys.exit(1)
    else:
        print("\n✅ Kraiz conjecture holds in searched range.")
        if near:
            print("near-miss (first 10):")
            for A,x,B,y,C,z,d in near[:10]:
                sign="+" if d>0 else "-"
                print(f"  {A}^{x}+{B}^{y} = {C}^{z} {sign}{abs(d)}")
        sys.exit(0)

# ──────────────────────────── CLI ─────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Kraiz-conjecture checker")
    ap.add_argument("-m","--min-base", type=int, default=12)
    ap.add_argument("-B","--max-base", type=int, required=True)
    ap.add_argument("-E","--max-exp",  type=int, required=True)
    ap.add_argument("--z-max", type=int)
    ap.add_argument("--filter-z", type=int)
    ap.add_argument("-d","--delta", type=int, metavar="Δ")
    ap.add_argument("--ratio-window", nargs=2, type=float, metavar=("LOW","HIGH"))
    ap.add_argument("--output", type=str,
                    help="file for full log (default auto-name)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    cfg = dict(
        min_b=args.min_base,
        max_b=args.max_base,
        max_e=args.max_exp,
        z_lim=args.z_max if args.z_max else args.max_exp,
        filt_z=args.filter_z,
        delta=args.delta,
        win=tuple(args.ratio_window) if args.ratio_window else None,
    )
    out_path = pathlib.Path(
        args.output or f"kraiz_log_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    )

    ordered, near, total = scan(cfg, loud=args.verbose)
    triples, multi = analyse(ordered)
    dump_log(out_path, cfg, triples, near)
    summary(cfg, total, triples, multi, near, out_path)

if __name__ == "__main__":
    main()
