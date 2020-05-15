#!/usr/bin/env python3

import os
import shutil
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--out-dir", type=Path)
parser.add_argument("--input", type=Path)
parser.add_argument("--output", type=Path)
parser.add_argument("--tmp-dir", type=Path)
parser.add_argument("--no-nacp", type=bool, default=False)
parser.add_argument("--name", default=None)
parser.add_argument("--author", default=None)
parser.add_argument("--version", default=None)
parser.add_argument("--icon", type=Path, default=None)
parser.add_argument("--romfs", type=Path, default=None)
parser.add_argument("--npdm-json", type=Path, default=None)
args = parser.parse_args()

for arg in ("input", "output", "icon", "romfs", "npdm_json"):
    p = getattr(args, arg)
    if p is not None:
        setattr(args, arg, p.absolute())

args.tmp_dir.mkdir(parents=True, exist_ok=True)
os.chdir(args.tmp_dir)

stem = args.input.stem

if args.npdm_json is not None:
    os.system(f"npdmtool {args.npdm_json} {stem}.npdm")
    os.system(f"elf2nso {args.input} {stem}.nso")

    exefs_dir = Path("exefs")
    exefs_dir.mkdir(exist_ok=True)
    shutil.copyfile(f"{stem}.nso", exefs_dir / "main")
    shutil.copyfile(f"{stem}.npdm", exefs_dir / "main.npdm")

    os.system(f"build_pfs0 {exefs_dir} {args.output}")

    shutil.rmtree(exefs_dir)
else:
    cmd= f"elf2nro {args.input} {args.output} --icon={args.icon}"

    if not args.no_nacp:
        os.system(f"nacptool --create '{args.name}' '{args.author}' '{args.version}' {stem}.nacp")
        cmd += f" --nacp={stem}.nacp"

    if args.romfs is not None:
        cmd += f" --romfsdir={args.romfs}"

    os.system(cmd)