"""Shared helpers for the 2026-11-25 fix pass (fix-pass-agent).

Loads JSONL record files, applies edits in place preserving line order and all untouched
fields, and records every change in `history` (questions, answer units) or `notes`
(controls, evidence requirements). Run scripts from the repository root.
"""
import glob
import json
import os

DATE = "2026-11-25"
BY = "fix-pass-agent"
EM = "—"


class Store:
    def __init__(self, directory):
        self.directory = directory
        self.files = {}  # path -> list of records
        self.index = {}  # id -> (path, position)
        for path in sorted(glob.glob(os.path.join(directory, "*.jsonl"))):
            recs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
            self.files[path] = recs
            for i, r in enumerate(recs):
                self.index[r["id"]] = (path, i)
        self.dirty = set()

    def __contains__(self, rid):
        return rid in self.index

    def get(self, rid):
        path, i = self.index[rid]
        self.dirty.add(path)
        return self.files[path][i]

    def peek(self, rid):
        path, i = self.index[rid]
        return self.files[path][i]

    def all(self):
        for path, recs in self.files.items():
            for r in recs:
                yield r

    def touch_all(self):
        self.dirty.update(self.files.keys())

    def next_id(self, prefix, cat, width):
        nums = [int(k.rsplit("-", 1)[1]) for k in self.index if k.startswith("%s-%s-" % (prefix, cat))]
        return "%s-%s-%0*d" % (prefix, cat, width, (max(nums) if nums else 0) + 1)

    def add(self, cat, record):
        path = os.path.join(self.directory, cat + ".jsonl")
        if record["id"] in self.index:
            raise SystemExit("duplicate id " + record["id"])
        self.files.setdefault(path, []).append(record)
        self.index[record["id"]] = (path, len(self.files[path]) - 1)
        self.dirty.add(path)
        return record

    def save(self):
        for path in sorted(self.dirty):
            text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.files[path])
            if EM in text:
                raise SystemExit("em dash in " + path)
            open(path, "w", encoding="utf-8").write(text)
        n = len(self.dirty)
        self.dirty = set()
        return n


def hist(rec, change):
    rec.setdefault("history", []).append({"date": DATE, "change": change, "by": BY})


def note(rec, text):
    prefix = "Fix pass %s (%s): " % (DATE, BY)
    rec["notes"] = (rec.get("notes", "").rstrip() + " " if rec.get("notes", "").strip() else "") + prefix + text


def replace(rec, field, old, new):
    if old not in rec[field]:
        raise SystemExit("%s.%s: text not found: %s" % (rec["id"], field, old[:80]))
    rec[field] = rec[field].replace(old, new)


def add_list(rec, field, items):
    cur = rec.get(field) or []
    if not isinstance(cur, list):
        cur = []
    for x in items:
        if x not in cur:
            cur.append(x)
    rec[field] = cur


def created(by=BY):
    return [{"date": DATE, "change": "created", "by": by}]
