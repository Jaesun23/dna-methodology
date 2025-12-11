#!/usr/bin/env python3
"""
Gemini Gem용 파일에서 Claude/1호/2호 관련 내용을 일반화
"""
import re
from pathlib import Path

GEM_DIR = Path("/Users/jason/Projects/dna-methodology/gemini-gem")

# 치환 규칙 (순서 중요!)
REPLACEMENTS = [
    # 1호/2호 관련
    (r'1호/2호 확인 완료', 'AI 검증 완료'),
    (r'1호 확인 완료', 'AI 검증 완료'),
    (r'2호 확인 완료', 'AI 검증 완료'),
    (r'\(1호\)', '(AI 어시스턴트)'),
    (r'\(2호\)', '(AI 어시스턴트)'),
    (r'\(Jason \+ 2호\)', '(Jason + AI)'),
    (r'에이전트 vs 2호', 'AI 모델별 차이'),
    (r'├─ 2호: Compact 있음 → 긴 작업 가능', '├─ 일부 AI: Compact 기능으로 긴 작업 가능'),
    (r'├─ 에이전트: Compact 없음 → 200K가 hard limit', '├─ 일부 AI: Compact 없음 → 컨텍스트가 hard limit'),
    
    # Claude 200K → 일반화 (컨텍스트 예시로 유지하되 AI로 일반화)
    (r'Claude 200K 토큰 윈도우:', 'AI 컨텍스트 윈도우 (예: 200K 토큰):'),
    (r'Claude 컨텍스트 윈도우: 200K 토큰', 'AI 컨텍스트 윈도우 (예: 200K 토큰)'),
    (r'컨텍스트 = 80-90K 토큰 \(Claude\)', '컨텍스트 = 모델별 안전 범위'),
]

def process_file(filepath: Path):
    """파일 내용 치환"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for pattern, replacement in REPLACEMENTS:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            # 변경된 횟수 카운트
            count = len(re.findall(pattern, content))
            changes.append(f"  '{pattern}' → '{replacement}' ({count}회)")
            content = new_content
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath.name} 수정됨:")
        for change in changes:
            print(change)
    else:
        print(f"⏭️  {filepath.name} 변경 없음")
    
    return content != original


def main():
    print("🔧 Gemini Gem 파일 수정 시작\n")
    
    files_to_process = [
        "02_STANDARDS.txt",
        "03_STAGE_GUIDES.txt",
        "04_DNA_METHODOLOGY_DETAILED.txt",
    ]
    
    modified_count = 0
    for filename in files_to_process:
        filepath = GEM_DIR / filename
        if filepath.exists():
            if process_file(filepath):
                modified_count += 1
        else:
            print(f"⚠️  {filename} 파일 없음")
        print()
    
    print(f"\n🎉 완료! {modified_count}개 파일 수정됨")
    
    # 수정 후 확인
    print("\n📋 수정 후 확인:")
    import subprocess
    result = subprocess.run(
        ['grep', '-n', '-i', '1호\\|2호\\|claude', *[str(GEM_DIR / f) for f in files_to_process]],
        capture_output=True, text=True
    )
    if result.stdout:
        print("⚠️  아직 남은 항목:")
        print(result.stdout)
    else:
        print("✅ 모든 Claude/1호/2호 관련 내용 제거됨!")


if __name__ == "__main__":
    main()
