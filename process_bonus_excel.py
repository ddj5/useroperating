#!/usr/bin/env python3
"""Process recall bonus Excel files and generate bonus/coupon output workbooks.

This script uses only Python's standard library, so it can run in locked-down
machines where openpyxl/pandas are not installed.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN_SHEET_NAMES = {"A", "B", "C", "A组", "B组", "C组", "Group A", "Group B", "Group C"}
GROUP_MAP = {"A": "Group A", "B": "Group B", "C": "Group C", "A组": "Group A", "B组": "Group B", "C组": "Group C"}
COUPON_IDS = {"ng": "89199", "tz": "89198", "ug": "89197", "gh": "89196", "ke": "89195"}
SPORTS_COUPON_COL = "No-Deposit Sports Coupon(odd>2.5)"
CASH_BONUS_COL = "casinobonus"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _col_to_num(cell_ref: str) -> int:
    letters = re.sub(r"[^A-Z]", "", cell_ref.upper())
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _num_to_col(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


@dataclass
class WorkbookData:
    sheets: dict[str, list[dict[str, str]]]

    @property
    def rows(self) -> list[dict[str, str]]:
        out: list[dict[str, str]] = []
        for name, rows in self.sheets.items():
            if _is_input_group_sheet(name, rows):
                for row in rows:
                    row = dict(row)
                    row.setdefault("label", GROUP_MAP.get(name, name))
                    out.append(row)
        return out


def _is_input_group_sheet(name: str, rows: list[dict[str, str]]) -> bool:
    return bool(rows) and name in MAIN_SHEET_NAMES and {"userid", "username", "country"}.issubset(rows[0])


def read_xlsx(path: Path) -> WorkbookData:
    with zipfile.ZipFile(path) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))

        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rel_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {r.attrib["Id"]: r.attrib["Target"] for r in rel_root}
        sheets: dict[str, list[dict[str, str]]] = {}

        for sh in wb.findall("m:sheets/m:sheet", NS):
            name = sh.attrib["name"]
            rid = sh.attrib[f"{{{REL_NS}}}id"]
            ws_path = posixpath.normpath("xl/" + rels[rid].lstrip("/"))
            rows: list[list[str]] = []
            root = ET.fromstring(zf.read(ws_path))
            for row in root.findall("m:sheetData/m:row", NS):
                vals: list[str] = []
                for c in row.findall("m:c", NS):
                    idx = _col_to_num(c.attrib.get("r", "A1")) - 1
                    while len(vals) <= idx:
                        vals.append("")
                    v = c.find("m:v", NS)
                    val = "" if v is None or v.text is None else v.text
                    if c.attrib.get("t") == "s" and val:
                        val = shared[int(val)]
                    elif c.attrib.get("t") == "inlineStr":
                        val = "".join(t.text or "" for t in c.findall(".//m:t", NS))
                    vals[idx] = val
                rows.append(vals)
            if not rows:
                sheets[name] = []
                continue
            headers = [str(x).strip() for x in rows[0]]
            sheets[name] = [dict(zip(headers, r + [""] * (len(headers) - len(r)))) for r in rows[1:]]
        return WorkbookData(sheets)


def write_xlsx(path: Path, sheets: dict[str, list[list[object]]]) -> None:
    def esc(s: object) -> str:
        return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))

    def sheet_xml(rows: list[list[object]]) -> str:
        body = []
        for r_idx, row in enumerate(rows, 1):
            cells = []
            for c_idx, value in enumerate(row, 1):
                if value in (None, ""):
                    continue
                ref = f"{_num_to_col(c_idx)}{r_idx}"
                cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{esc(value)}</t></is></c>')
            body.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + "".join(body) + "</sheetData></worksheet>"

    names = list(sheets)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(names)+1)) + "</Types>")
        zf.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        zf.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(f'<sheet name="{esc(n)}" sheetId="{i}" r:id="rId{i}"/>' for i, n in enumerate(names, 1)) + "</sheets></workbook>")
        zf.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(names)+1)) + "</Relationships>")
        for i, name in enumerate(names, 1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(sheets[name]))


def _has_positive_amount(value: str) -> bool:
    try:
        return float(value or 0) > 0
    except ValueError:
        return bool(value)


def _is_deposit_category_1_to_5(value: str) -> bool:
    value = (value or "").strip().replace(" ", "")
    if value == "[1,5)":
        return True
    try:
        amount = float(value)
    except ValueError:
        return False
    return 1 <= amount < 5


def build_outputs(wb: WorkbookData) -> dict[str, dict[str, list[list[object]]]]:
    rows = wb.rows
    bonus1 = [["用户id", "用户金额"]]
    bonus2 = [["用户id", "用户金额"]]
    coupon = [["用户名", "优惠券ID", "发放后几天生效", "优惠券金额", "优惠券数量"]]
    for r in rows:
        casino_amount = r.get(CASH_BONUS_COL, "")
        user_preference = (r.get("User Preference") or "").strip().lower()
        if _has_positive_amount(casino_amount) and user_preference != "sport-user":
            bonus_row = [r.get("userid", ""), casino_amount]
            if _is_deposit_category_1_to_5(r.get("deposit_category", "")):
                bonus2.append(bonus_row)
            else:
                bonus1.append(bonus_row)

        sports_amount = r.get(SPORTS_COUPON_COL, "")
        country = (r.get("country") or "").lower()
        coupon_id = COUPON_IDS.get(country, "")
        if _has_positive_amount(sports_amount):
            coupon.append([r.get("username", ""), coupon_id, 0, sports_amount, 1])

    return {"bonus1": {"bonus1": bonus1}, "bonus2": {"bonus2": bonus2}, "coupon": {"优惠券模板": coupon}}


def main() -> None:
    parser = argparse.ArgumentParser(description="处理召回 bonus Excel，并输出 bonus 与优惠券模板 Excel。")
    parser.add_argument("input", type=Path, help="上传/源 Excel，例如 gh召回0612_bonus.xlsx")
    parser.add_argument("--output-dir", type=Path, default=Path("output"), help="输出目录，默认 output")
    parser.add_argument("--prefix", default=None, help="输出文件名前缀；默认使用输入文件名")
    args = parser.parse_args()

    wb = read_xlsx(args.input)
    outputs = build_outputs(wb)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or args.input.stem
    bonus1_path = args.output_dir / f"{prefix}_bonus1.xlsx"
    bonus2_path = args.output_dir / f"{prefix}_bonus2.xlsx"
    coupon_path = args.output_dir / f"{prefix}_优惠券模板.xlsx"
    write_xlsx(bonus1_path, outputs["bonus1"])
    write_xlsx(bonus2_path, outputs["bonus2"])
    write_xlsx(coupon_path, outputs["coupon"])
    print(f"已输出: {bonus1_path}")
    print(f"已输出: {bonus2_path}")
    print(f"已输出: {coupon_path}")


if __name__ == "__main__":
    main()
