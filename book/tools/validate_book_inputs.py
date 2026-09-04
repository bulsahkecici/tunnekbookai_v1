#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys
root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'audits'/'question_bank_integrity.json').read_text(encoding='utf-8'))
manifest=json.loads((root/'audits'/'source_manifest.json').read_text(encoding='utf-8'))
errors=[]
for item in manifest['files']:
    p=root.parent/item['path'] if item['path'].startswith('book/') else root/item['path']
    if not p.exists(): errors.append(f"missing: {p}"); continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=item['sha256']: errors.append(f"sha mismatch: {p}")
qindex=json.loads((root/'question_bank'/'normalized'/'question_bank_index.json').read_text(encoding='utf-8'))
if qindex['total_sections']!=59: errors.append(f"section count {qindex['total_sections']} != 59")
if qindex['total_questions']!=2950: errors.append(f"question count {qindex['total_questions']} != 2950")
if audit['decision']!='PASS': errors.append('integrity audit is not PASS')
if errors:
    print('BOOK INPUT VALIDATION: FAIL')
    print('\n'.join('- '+e for e in errors))
    sys.exit(1)
print('BOOK INPUT VALIDATION: PASS')
print('59 question-bank sections / 2950 questions')
