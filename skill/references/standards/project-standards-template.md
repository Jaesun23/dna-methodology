# Project Standards 템플릿 (언어 중립)

> **버전**: v1.0
> **최종 수정**: 2025-12-09
> **출처**: 06G-00 Stage 6 가이드에서 분리
> **원칙**: 언어/프레임워크에 무관한 범용 템플릿

---

## 📋 개요

이 템플릿은 **Stage 6: Project Standards** 산출물의 기본 구조입니다.
프로젝트의 언어/프레임워크에 맞게 구체화하여 사용하세요.

**언어별 상세 예시**: `manual-cases/` 폴더 참조

---

## 📄 템플릿 시작

```markdown
# Project Standards

> **프로젝트**: [프로젝트명]
> **버전**: v1.0
> **작성일**: YYYY-MM-DD
> **기반 ADR**: 03A-401 ~ 03A-411 (DNA 시스템)
> **언어/프레임워크**: [언어 버전, 주요 프레임워크]

---

## 1. 코드 스타일

### 1.1 포맷팅
- **도구**: [Formatter Tool - 예: Ruff, Prettier, gofmt, rustfmt]
- **줄 길이**: [80/88/100/120자]
- **들여쓰기**: [Spaces/Tabs, 개수]
- **인용부호**: [큰따옴표/작은따옴표]

### 1.2 네이밍
| 대상 | 규칙 | 예시 |
|------|-----|------|
| 클래스/타입 | PascalCase | `OrderService`, `UserDto` |
| 함수/메서드 | [snake_case/camelCase] | `create_order` / `createOrder` |
| 변수 | [snake_case/camelCase] | `user_id` / `userId` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 비공개 | [_prefix/private 키워드] | `_internal` |

### 1.3 Import/Package 순서
```
# 1. 표준 라이브러리/내장 모듈

# 2. 서드파티/외부 패키지

# 3. 로컬 모듈 (core → domain → api 순)
```

---

## 2. DNA 시스템 사용 규칙

> 각 DNA 시스템별 DO/DON'T 패턴 정의

### 2.1 Logging

**DO ✅**
```
- 구조화된 로거 사용 (core/logging)
- 컨텍스트 정보 포함 (trace_id, user_id)
- 키워드 인자로 데이터 전달
```

**DON'T ❌**
```
- print/console.log 사용 금지
- 표준 로깅 라이브러리 직접 사용 금지
- 문자열 연결/포매팅으로 로그 메시지 생성 금지
```

### 2.2 Configuration

**DO ✅**
```
- 중앙 설정 관리자 사용 (core/config)
- 타입 안전한 설정 접근
- 환경별 설정 분리
```

**DON'T ❌**
```
- 환경변수 직접 접근 금지
- 하드코딩된 설정값 금지
- 설정 검증 없이 사용 금지
```

### 2.3 Types

**DO ✅**
```
- 도메인 타입 사용 (UserId, OrderId, Money 등)
- 모든 공개 API에 타입 명시
- 타입 검사 도구 통과 필수
```

**DON'T ❌**
```
- Any/unknown/dynamic 타입 금지
- 원시 타입만으로 도메인 표현 금지
- 타입 힌트/어노테이션 누락 금지
```

### 2.4 Error Handling

**DO ✅**
```
- 도메인 예외 클래스 사용 (ValidationError, NotFoundError 등)
- 예외에 컨텍스트 정보 포함
- 복구 가능 여부에 따른 예외 분류
```

**DON'T ❌**
```
- 일반 Exception/Error 사용 금지
- 빈 catch/except 블록 금지
- 예외 무시(swallow) 금지
```

### 2.5 Database

**DO ✅**
```
- 중앙 세션/커넥션 관리자 사용
- 파라미터화된 쿼리 사용
- 트랜잭션 경계 명확히 설정
```

**DON'T ❌**
```
- 문자열 연결로 쿼리 생성 금지 (SQL Injection!)
- 수동 커넥션 관리 금지
- 커밋/롤백 누락 금지
```

---

## 3. 품질 기준

### 3.1 Zero Tolerance

| 항목 | 기준 | 검증 방법 |
|------|-----|----------|
| [Lint Tool] | 0 violations | `[lint command]` |
| [Type Check Tool] | 0 errors | `[type check command]` |
| [Test Framework] | 0 failures | `[test command]` |
| Coverage | [95%+] | `[coverage command]` |

### 3.2 커밋 전 필수

```bash
# 모든 검증 통과 필수 (pre-commit hook)
[pre-commit run command]
```

위반 시 커밋 차단됨.

---

## 4. 아키텍처 규칙

### 4.1 레이어 구조

```
src/
├── core/      # DNA 시스템 (공통 인프라)
├── domain/    # 비즈니스 로직
└── api/       # 인터페이스 (HTTP, CLI, etc.)
```

### 4.2 의존성 방향

```
허용: api → domain → core
금지: core → domain, domain → api
```

### 4.3 아키텍처 검증

```bash
# 의존성 방향 검증 도구
[architecture lint command]

# 위반 시
FAILED: Core는 Domain/API에 의존하지 않음
```

---

## 5. Git 규칙

### 5.1 커밋 메시지

```
<type>(<scope>): <subject>

타입:
- feat: 새 기능
- fix: 버그 수정
- refactor: 리팩토링
- test: 테스트 추가/수정
- docs: 문서 수정
- chore: 빌드/설정 변경
```

### 5.2 브랜치 전략

```
main         ← 운영 (보호됨)
develop      ← 개발 통합
feature/*    ← 기능 개발
fix/*        ← 버그 수정
```

### 5.3 PR 규칙

- [ ] 모든 CI 통과
- [ ] 리뷰어 [N]명 이상 승인
- [ ] 커버리지 유지 또는 증가

---

## 6. 참조

- ADR: `docs/adr/03A-401~411_*.md`
- DNA 구현: `src/core/`
- 자동화 설정: `[빌드 설정 파일]`, `[pre-commit 설정]`
```

## 템플릿 끝

---

## 🔧 사용 방법

### 1. 복사 후 구체화
```bash
cp 02_PROJECT_STANDARDS_TEMPLATE.md docs/06D-01_project_standards.md
```

### 2. 플레이스홀더 교체

| 플레이스홀더 | 언어별 예시 |
|------------|-----------|
| `[Lint Tool]` | Ruff (Python), ESLint (TS), golangci-lint (Go) |
| `[Type Check Tool]` | MyPy (Python), tsc (TS), go vet (Go) |
| `[Test Framework]` | pytest (Python), Jest (TS), go test (Go) |
| `[Formatter Tool]` | Ruff (Python), Prettier (TS), gofmt (Go) |
| `[lint command]` | `ruff check .`, `eslint .`, `golangci-lint run` |

### 3. DNA 규칙 상세화
각 DNA 시스템별로 프로젝트에 맞는 구체적인 DO/DON'T 코드 예시 추가

### 4. 팀 합의 반영
- 줄 길이, 들여쓰기 등 스타일 결정
- 커버리지 기준 결정
- 리뷰어 수 결정

---

## 📚 언어별 상세 예시

- **Python**: `manual-cases/06M-01_python_standards_manual.md` (예정)
- **TypeScript**: `manual-cases/06M-02_typescript_standards_manual.md` (예정)
- **Go**: `manual-cases/06M-03_go_standards_manual.md` (예정)

---

## ✅ 체크리스트: 템플릿 사용 전 확인

- [ ] 프로젝트 언어/프레임워크 결정됨
- [ ] DNA 시스템 ADR 작성 완료 (Stage 4)
- [ ] DNA 시스템 구현 완료 (Stage 5)
- [ ] 품질 도구 선택 완료
- [ ] 팀 스타일 합의 완료
