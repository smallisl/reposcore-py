#!/usr/bin/env python3
import subprocess
import jinja2
import os
import sys

# 1) --help 출력 시도
try:
    help_result = subprocess.run(
        ["python", "-m", "reposcore", "--help"],
        capture_output=True,
        text=True,
        check=True
    )
    help_text = help_result.stdout.strip()
except subprocess.CalledProcessError as e: 
    print(e.stderr or e.stdout)
    print("❌ Failed to get help text from 'reposcore':")
    print("❌ Failed to generate README.md from template_README.md")
    sys.exit(1)

# 2) 템플릿 로드
template_path = os.path.join(os.path.dirname(__file__), "..", "template_README.md")
with open(template_path, encoding="utf-8") as f:
    template = jinja2.Template(f.read())

# 3) 렌더링 & 저장
rendered = template.render(usage=help_text)
readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(rendered)

print("✅ README.md generated from template_README.md")