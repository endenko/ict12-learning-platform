#!/usr/bin/env python3
"""Native XLSX integrity checks. Prints only verdicts/counts, never student data."""
import json,datetime
from pathlib import Path
from openpyxl import load_workbook
checks=[]
for target in ['local','production']:
 w=load_workbook(f'tests/readiness-{target}-export.xlsx',data_only=False)
 assert w.sheetnames==['Bảng điểm','Chi tiết câu trả lời']
 scores,details=w.worksheets
 assert scores.max_row==2 and details.max_row==82
 assert isinstance(scores.cell(2,5).value,(int,float))
 name=scores.cell(2,2)
 assert name.data_type=='s' and str(name.value).lstrip().startswith(('=','+','-','@'))
 assert all(c.data_type!='f' for s in w for row in s for c in row)
 default=load_workbook(f'tests/readiness-{target}-default-export.xlsx',data_only=False)
 assert not any(str(row[0].value or '').lower().startswith('test') or str(row[2].value or '').upper().startswith('TEST') for row in list(default.worksheets[0])[1:])
 checks.append(dict(target=target,filteredScoreRows=scores.max_row-1,perQuestionRows=details.max_row-1,formulaLikeName='literal string',numericScore=True,formulaCells=0,defaultExcludesTests=True))
r=dict(success=True,checkedAt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),checks=checks)
Path('tests/readiness-excel-results.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
