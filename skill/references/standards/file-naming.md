# DNA 방법론 파일 및 코드 명명 규칙

> **목적**: 모든 파일(문서, 코드, 테스트, 설정)의 위치와 이름을 즉시 파악
> **버전**: v2.0 (2025-12-09)
> **적용 범위**: DNA 방법론의 모든 파일

---

## 📖 문서 구조

```
이 문서의 Part 구성:

Part 1: 방법론 산출물 (문서)     Line 23-248
Part 2: 소스 코드 구조           Line 249-443
Part 3: 테스트 파일              Line 444-578
Part 4: 스크립트/임시 파일       Line 579-709
Part 5: 설정 파일                Line 710-909
```

---

# Part 1: 방법론 산출물 (문서)

---

## 🎯 핵심 원칙

**"파일명만 봐도 어느 Stage의 무슨 역할인지 즉시 알 수 있어야 한다"**

### 왜 필요한가?

❌ **명명 규칙 없으면**:
```
core_functions.md
family.md
constraints_final_v2.md
ADR-fastapi.md
```
→ 어느 Stage인지? 순서는? 타입은? → **혼란!**

✅ **명명 규칙 있으면**:
```
01F-01_core_functions.md          # Stage 1, Function 문서
01C-01_family_classification.md   # Stage 1, Classification 문서
02D-01_tech_stack_decision.md     # Stage 2, Decision 문서
03A-103_fastapi_selection.md      # Stage 3, ADR (Domain)
```
→ **Stage, Type, 순서 즉시 파악!**

---

## 📋 문서 파일명 구조

### **패턴**: `{Stage}{Type}-{Seq}_{descriptive_name}.md`

```
01F-01_core_functions.md
│││ ││ └────────────────── 설명적 이름 (영문, snake_case)
│││ ││
│││ │└─────────────────── 순서 번호 (01~99)
│││ │
│││ └──────────────────── 구분자 (하이픈)
││└─────────────────────── 문서 타입 (알파벳 1글자)
│└──────────────────────── Stage 번호 (01~09)
└───────────────────────── 2자리 숫자 (앞에 0 붙임)
```

### **구성 요소**

| 요소 | 포맷 | 설명 | 예시 |
|------|------|------|------|
| **Stage** | 2자리 숫자 | 01~09 (9개 Stage) | `01`, `02`, `03` |
| **Type** | 알파벳 1글자 | 문서 유형 코드 | `F`, `C`, `D`, `A`, `G` |
| **Seq** | 2자리 숫자 | 01~99 (같은 Stage+Type 내 순서) | `01`, `02`, `03` |
| **Name** | snake_case | 설명적 이름 (영문) | `core_functions` |

---

## 🔤 Type 코드 정의

### **프로젝트 산출물**

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **F** | Function | 기능 정의 | `01F-01_core_functions.md` |
| **C** | Classification | 분류/분석 결과 | `01C-01_family_classification.md` |
| **D** | Decision | 결정 사항 | `02D-01_tech_stack_decision.md` |
| **S** | Schema | 스키마/설계 | `02S-02_data_schema.md` |
| **A** | ADR | Architecture Decision Record | `03A-001_logging.md` |
| **B** | Blueprint | 청사진 | `07B-01_project_blueprint.md` |
| **T** | Task | 작업 분해 | `08T-01_task_breakdown.md` |
| **L** | List/Checklist | 체크리스트 | `09L-01_task_001_checklist.md` |

### **방법론 문서**

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **G** | Guide | 간결한 가이드 | `01G-00_core_definition_guide.md` |
| **M** | Manual | 상세 해설서 | `01M-01_layer1_manual.md` |
| **E** | Example/Case | 사례집 | `02E-01_stock_trading_case.md` |

### **특수 문서**

| Code | 의미 | 용도 | 예시 |
|------|------|------|------|
| **00** | Meta | 방법론 자체 문서 | `00_FILE_NAMING_CONVENTION.md` |

---

## 📁 Stage별 산출물 요약

### Stage 1: 패밀리 구분과 핵심기능 파악
```
01F-01_core_functions.md          # 핵심 기능 정의
01C-01_family_classification.md   # 패밀리 분류 (A-C-A)
01C-02_nfr_profile.md             # NFR 프로파일 (A-B-B-A)
01D-01_tech_candidates.md         # 기술 후보군
```

### Stage 2: 구조설계
```
02C-01_layer3_constraints.md      # Layer 3 제약 조사
02C-02_conflicts_analysis.md      # 충돌 패턴 분석
02D-01_tech_stack_decision.md     # 기술 스택 확정
02S-01_architecture_diagram.png   # 아키텍처 다이어그램
02S-02_data_schema.md             # 데이터 스키마
02S-03_api_design.md              # API 설계
02L-01_adr_list.md                # ADR 작성 대상 목록
```

### Stage 3: ADR 문서화
```
docs/adr/dna-system/
  03A-001_logging.md              # DNA 시스템 ADR (001~099)
  03A-002_error_handling.md
  ...

docs/adr/domain/
  03A-101_api_selection.md        # Domain ADR (100~999)
  03A-102_strategy_pattern.md
  ...
```

### Stage 4-5: DNA 시스템
```
04B-01_dna_system_blueprint.md    # DNA 시스템 청사진
04L-01_dna_system_checklist.md    # DNA 시스템 체크리스트
05D-01_module_usage_docs.md       # 모듈 사용법 문서
```

### Stage 6: Project Standards
```
06D-01_project_standards.md       # 프로젝트 표준 (THE 산출물)
```

### Stage 7: Project Blueprint
```
07B-01_project_blueprint.md       # 프로젝트 청사진
07S-01_domain_architecture.md     # 도메인 아키텍처
```

### Stage 8: Task Breakdown
```
08T-01_task_breakdown.md          # 작업 분해
```

### Stage 9: Checklist
```
09L-01_task_001_checklist.md      # 작업별 체크리스트
09L-02_task_002_checklist.md
...
```

---

## 📦 문서 저장 위치

### **방법론 문서** (dna-methodology 리포지토리)
```
docs/guides/
├── 00_CORE_METHODOLOGY.md
├── 01_DNA_METHODOLOGY_DETAILED.md
├── 01G-00_core_definition_guide.md
├── 02G-00_environment_constraints_guide.md
├── ...
├── standards/
│   ├── 00_FILE_NAMING_CONVENTION.md   # 이 문서!
│   └── 01_STAGE_STRUCTURE.md
│   ├── 02_PROJECT_STANDARDS_TEMPLATE.md
│   └── 03_DNA_SYSTEMS_GUIDE.md
└── manuals/
    └── (언어별 매뉴얼)
```

### **프로젝트 산출물** (실제 프로젝트)
```
docs/
├── architecture/              # Stage 1-2 산출물
│   ├── 01F-01_core_functions.md
│   └── 02D-01_tech_stack_decision.md
│
├── adr/                       # Stage 3 산출물
│   ├── dna-system/
│   │   └── 03A-001_logging.md
│   └── domain/
│       └── 03A-101_api_selection.md
│
├── dna-system/                # Stage 4-5 산출물
│   └── 04B-01_dna_system_blueprint.md
│
├── standards/                 # Stage 6 산출물
│   └── 06D-01_project_standards.md
│
├── blueprint/                 # Stage 7 산출물
│   └── 07B-01_project_blueprint.md
│
├── tasks/                     # Stage 8 산출물
│   └── 08T-01_task_breakdown.md
│
└── checklists/                # Stage 9 산출물
    ├── 09L-01_task_001_checklist.md
    └── ...
```

---

## 🎯 Type 치트시트

```
프로젝트 산출물:
F = Function       C = Classification   D = Decision
S = Schema         A = ADR              B = Blueprint
T = Task           L = List/Checklist

방법론 문서:
G = Guide          M = Manual           E = Example/Case
```

### 읽는 법
```
03A-101_fastapi_selection.md
│││ │││
││└─┴┴─ A-101 = ADR, 101번 (Domain ADR)
│└──── 03 = Stage 3
└───── "Stage 3의 101번 ADR (Domain)"
```

---

# Part 2: 소스 코드 구조

---

## 🏗️ 디렉토리 구조

### 표준 프로젝트 구조
```
project-root/
├── src/                           # 소스 코드 루트
│   ├── core/                      # DNA 시스템 (Stage 5)
│   │   ├── logging/
│   │   ├── config/
│   │   ├── errors/
│   │   ├── types/
│   │   ├── database/
│   │   ├── cache/
│   │   ├── auth/
│   │   ├── validation/
│   │   ├── events/
│   │   ├── http/
│   │   └── testing/
│   │
│   ├── domain/                    # 도메인 로직 (Stage 9)
│   │   └── {domain_name}/
│   │       ├── entities/
│   │       ├── value_objects/
│   │       ├── services/
│   │       ├── repositories/
│   │       └── events/
│   │
│   ├── application/               # 유스케이스
│   │   └── {domain_name}/
│   │       ├── commands/
│   │       ├── queries/
│   │       └── handlers/
│   │
│   ├── infrastructure/            # 외부 연동
│   │   ├── persistence/
│   │   ├── external_apis/
│   │   └── messaging/
│   │
│   └── api/                       # API 레이어
│       ├── routes/
│       ├── schemas/
│       └── middleware/
│
├── tests/                         # Part 3 참조
├── scripts/                       # Part 4 참조
├── docs/                          # Part 1 참조
└── (설정 파일들)                   # Part 5 참조
```

---

## 📝 소스 파일 명명 규칙

### 기본 원칙
```
1. snake_case 사용 (모든 언어 공통 권장)
2. 역할이 명확한 접미사 사용
3. 복수형/단수형 일관성 유지
```

### 레이어별 파일명 패턴

#### core/ (DNA 시스템)
```
src/core/{system_name}/
├── index.*                       # 모듈 진입점 (언어별 상이)
├── {system_name}.*               # 주요 구현
├── config.*                      # 설정
├── types.*                       # 타입 정의
├── errors.*                      # 예외/에러 정의
└── constants.*                   # 상수

언어별 진입점:
├── Python:     __init__.py
├── TypeScript: index.ts
├── Rust:       mod.rs
├── Go:         (폴더명이 패키지)
└── Java:       (패키지 구조)

예시 (언어 무관):
src/core/logging/
├── index.*                       # 모듈 진입점
├── logger.*                      # get_logger(), bind_context()
├── config.*                      # LogConfig
├── formatters.*                  # JSON, Console formatter
└── handlers.*                    # File, Stream handler
```

#### domain/ (도메인)
```
src/domain/{domain_name}/
├── entities/
│   └── {entity_name}.*           # 단수형: user.*, order.*
├── value_objects/
│   └── {value_name}.*            # money.*, address.*
├── services/
│   └── {domain}_service.*        # order_service.*
├── repositories/
│   └── {entity}_repository.*     # user_repository.* (인터페이스)
└── events/
    └── {entity}_events.*         # order_events.*

예시:
src/domain/trading/
├── entities/
│   ├── order.*
│   └── position.*
├── value_objects/
│   ├── money.*
│   └── quantity.*
├── services/
│   └── trading_service.*
├── repositories/
│   └── order_repository.*
└── events/
    └── order_events.*
```

#### application/ (유스케이스)
```
src/application/{domain_name}/
├── commands/
│   └── {action}_{entity}_command.*    # create_order_command.*
├── queries/
│   └── get_{entity}_query.*           # get_order_query.*
└── handlers/
    └── {command/query}_handler.*      # create_order_handler.*

예시:
src/application/trading/
├── commands/
│   ├── create_order_command.*
│   └── cancel_order_command.*
├── queries/
│   └── get_order_history_query.*
└── handlers/
    ├── create_order_handler.*
    └── get_order_history_handler.*
```

#### infrastructure/ (인프라)
```
src/infrastructure/
├── persistence/
│   └── {db_type}_{entity}_repository.*   # postgres_user_repository.*
├── external_apis/
│   └── {service_name}_client.*           # kis_api_client.*
└── messaging/
    └── {broker}_{purpose}.*              # kafka_event_publisher.*
```

#### api/ (API)
```
src/api/
├── routes/
│   └── {domain}_routes.*          # trading_routes.*
├── schemas/
│   └── {domain}_schemas.*         # trading_schemas.*
└── middleware/
    └── {purpose}_middleware.*     # auth_middleware.*
```

---

## 🏷️ 클래스/함수 명명 규칙

### 클래스명 (PascalCase)
```
Entity:        User, Order, Product
Value Object:  Money, Address, Email
Service:       OrderService, TradingService
Repository:    UserRepository, OrderRepository
Handler:       CreateOrderHandler, GetUserHandler
Command:       CreateOrderCommand, UpdateUserCommand
Query:         GetOrderQuery, ListUsersQuery
Event:         OrderCreated, UserRegistered
Exception:     OrderNotFoundError, InvalidAmountError
```

### 함수명 (snake_case)
```
생성:    create_order(), register_user()
조회:    get_order(), find_by_id(), list_orders()
수정:    update_order(), change_status()
삭제:    delete_order(), remove_item()
검증:    validate_amount(), is_valid()
변환:    to_dict(), from_dto()
```

### 상수 (UPPER_SNAKE_CASE)
```
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT_MS = 5000
ORDER_STATUS_PENDING = "pending"
```

---

# Part 3: 테스트 파일

---

## 🧪 테스트 디렉토리 구조

```
tests/
├── unit/                          # 단위 테스트
│   ├── core/                      # DNA 시스템 테스트
│   │   ├── test_logging.*
│   │   ├── test_config.*
│   │   └── ...
│   │
│   ├── domain/                    # 도메인 테스트
│   │   └── {domain_name}/
│   │       ├── test_{entity}.*
│   │       └── test_{service}.*
│   │
│   └── application/               # 유스케이스 테스트
│       └── {domain_name}/
│           └── test_{handler}.*
│
├── integration/                   # 통합 테스트
│   ├── test_database.*
│   ├── test_external_api.*
│   └── test_{domain}_flow.*
│
├── e2e/                           # E2E 테스트
│   └── test_{scenario}.*
│
├── fixtures/                      # 공용 픽스처/헬퍼
│   ├── factories.*                # 테스트 데이터 팩토리
│   ├── mocks.*                    # 공용 Mock
│   └── data/                      # 테스트 데이터 파일
│       └── sample_orders.json
│
└── [테스트 설정 파일]              # 언어별 상이
    # Python: conftest.py
    # TypeScript: jest.config.ts, vitest.config.ts
    # Go: *_test.go (동일 폴더)
    # Java: src/test/resources/
```

---

## 📝 테스트 파일 명명 규칙

### 파일명 패턴
```
test_{대상모듈명}.*

예시:
test_user.*                        # User 엔티티 테스트
test_order_service.*               # OrderService 테스트
test_create_order_handler.*        # CreateOrderHandler 테스트
test_postgres_user_repository.*    # PostgresUserRepository 테스트
```

### 테스트 함수명 패턴
```
test_{기능}_{조건}_{예상결과}

예시 (언어별 스타일 다름):
# snake_case (Python, Rust)
test_create_order_with_valid_data_returns_order_id()
test_create_order_with_zero_amount_raises_error()

# camelCase (JavaScript, TypeScript, Java)
testCreateOrderWithValidDataReturnsOrderId()
shouldThrowErrorWhenAmountIsZero()

# BDD 스타일 (Jest, Vitest)
it('should create order with valid data')
describe('when amount is zero', () => { ... })
```

### 테스트 클래스명 패턴 (선택적)
```
class Test{대상클래스명}:
class Test{기능그룹}:

예시:
TestUser, TestOrderCreation, TestAuthenticationFlow
```

---

## 🎯 테스트 파일 위치 규칙

### 소스 ↔ 테스트 대응
```
소스 파일:
src/domain/trading/entities/order.*

테스트 파일:
tests/unit/domain/trading/test_order.*
```

### 미러링 원칙
```
src/                               tests/unit/
├── core/                          ├── core/
│   └── logging/                   │   └── test_logging.*
│       └── logger.*               │
│                                  │
├── domain/                        ├── domain/
│   └── trading/                   │   └── trading/
│       └── entities/              │       ├── test_order.*
│           └── order.*            │       └── test_position.*
│                                  │
└── application/                   └── application/
    └── trading/                       └── trading/
        └── handlers/                      └── test_create_order_handler.*
            └── create_order_handler.py
```

---

## 📦 픽스처 명명 규칙

### 팩토리 함수
```
def create_{entity}(**overrides) -> Entity:
def build_{entity}_dict(**overrides) -> dict:

예시:
def create_user(name="Test User", email="test@example.com") -> User:
def build_order_dict(amount=10000, status="pending") -> dict:
```

### Mock 객체
```
mock_{대상}_repository
mock_{서비스명}_client
stub_{외부시스템}

예시:
mock_user_repository
mock_kis_api_client
stub_payment_gateway
```

---

# Part 4: 스크립트/임시 파일

---

## 🔧 스크립트 디렉토리 구조

```
scripts/
├── setup/                         # 환경 설정 스크립트
│   ├── install_dependencies.sh
│   ├── setup_database.sh
│   └── init_project.sh
│
├── migration/                     # 마이그레이션 스크립트
│   ├── migrate_v1_to_v2.py
│   └── seed_data.py
│
├── deployment/                    # 배포 관련 스크립트
│   ├── deploy_staging.sh
│   └── deploy_production.sh
│
├── utils/                         # 유틸리티 스크립트
│   ├── generate_test_data.py
│   ├── cleanup_logs.sh
│   └── health_check.py
│
└── ci/                            # CI/CD 스크립트
    ├── run_tests.sh
    └── build_image.sh
```

---

## 📝 스크립트 명명 규칙

### 파일명 패턴
```
{동작}_{대상}.{확장자}

예시:
setup_database.sh                  # 데이터베이스 설정
run_tests.sh                       # 테스트 실행
generate_test_data.py              # 테스트 데이터 생성
migrate_v1_to_v2.py                # v1에서 v2로 마이그레이션
cleanup_old_logs.sh                # 오래된 로그 정리
```

### 스크립트 종류별 접두사
```
setup_     환경/초기 설정
run_       실행 스크립트
build_     빌드 관련
deploy_    배포 관련
migrate_   마이그레이션
generate_  생성 스크립트
cleanup_   정리 스크립트
check_     검증/확인
```

---

## 📁 임시 파일 관리

### 임시 작업 디렉토리
```
.work/                             # 임시 작업 (gitignore 필수!)
├── notes/                         # 작업 메모
│   └── 2024-01-15_api_research.md
├── scratch/                       # 실험 코드
│   └── test_concept.py
├── debug/                         # 디버깅용
│   └── error_trace_20240115.log
└── exports/                       # 임시 내보내기
    └── report_draft.csv
```

### 임시 파일 명명 규칙
```
날짜 포함 권장:
{YYYY-MM-DD}_{설명}.{확장자}

예시:
2024-01-15_api_response_analysis.md
2024-01-15_performance_test_results.json
```

### .gitignore 필수 항목
```
# 임시 작업 폴더
.work/
temp/
tmp/

# 개인 메모
*.local.md
*.draft.md

# IDE/편집기
.idea/
.vscode/
*.swp
```

---

## 🗂️ 작업 관련 문서

### 작업 중 생성되는 문서 위치
```
docs/work/                         # 작업 관련 문서 (선택적 버전 관리)
├── research/                      # 리서치 문서
│   └── {date}_{topic}_research.md
├── decisions/                     # 미확정 결정 메모
│   └── {date}_{topic}_draft.md
└── reviews/                       # 리뷰/피드백
    └── {date}_{target}_review.md
```

### vs 공식 산출물 구분
```
공식 산출물 (Part 1 규칙):
docs/architecture/01F-01_core_functions.md    # 버전 관리 O
docs/adr/03A-001_logging.md                   # 버전 관리 O

작업 중 문서 (이 섹션):
docs/work/research/2024-01-15_db_comparison.md  # 버전 관리 △
.work/notes/quick_memo.md                       # 버전 관리 X
```

---

# Part 5: 설정 파일

---

## ⚙️ 프로젝트 루트 설정 파일

### 표준 레이아웃
```
project-root/
├── pyproject.toml                 # 빌드/린터/타입체커 (Python)
├── package.json                   # 빌드/린터 (TypeScript)
├── Cargo.toml                     # 빌드 설정 (Rust)
├── go.mod                         # 모듈 설정 (Go)
│
├── .pre-commit-config.yaml        # pre-commit hooks
├── .importlinter                  # 아키텍처 의존성 (Python)
│
├── .env.example                   # 환경변수 예시 (버전 관리 O)
├── .env                           # 실제 환경변수 (버전 관리 X)
├── .env.local                     # 로컬 오버라이드 (버전 관리 X)
│
├── .gitignore                     # Git 제외 파일
├── .dockerignore                  # Docker 제외 파일
│
├── Dockerfile                     # Docker 빌드
├── docker-compose.yml             # 로컬 개발 환경
├── docker-compose.test.yml        # 테스트 환경
│
├── Makefile                       # 공용 명령어 (선택)
└── README.md                      # 프로젝트 소개
```

---

## 📝 설정 파일 명명 규칙

### 환경별 설정 파일
```
.env.example                       # 예시 (버전 관리 O, 실제 값 X)
.env                               # 기본 환경
.env.local                         # 로컬 오버라이드
.env.development                   # 개발 환경
.env.staging                       # 스테이징 환경
.env.production                    # 운영 환경 (버전 관리 X!)
.env.test                          # 테스트 환경
```

### Docker 관련
```
Dockerfile                         # 기본 (운영용)
Dockerfile.dev                     # 개발용
Dockerfile.test                    # 테스트용

docker-compose.yml                 # 기본 (개발용)
docker-compose.test.yml            # 테스트용
docker-compose.prod.yml            # 운영용
```

### CI/CD 설정
```
.github/
├── workflows/
│   ├── ci.yml                     # CI 파이프라인
│   ├── cd.yml                     # CD 파이프라인
│   └── codeql.yml                 # 보안 분석
├── CODEOWNERS                     # 코드 소유자
└── pull_request_template.md       # PR 템플릿

.gitlab-ci.yml                     # GitLab CI
```

---

## 🔒 버전 관리 주의 파일

### 버전 관리 O (반드시 포함)
```
✅ .env.example                    # 환경변수 구조 공유
✅ pyproject.toml / package.json   # 의존성 정의
✅ .pre-commit-config.yaml         # 품질 도구 설정
✅ Dockerfile                      # 빌드 정의
✅ docker-compose.yml              # 개발 환경
✅ .gitignore                      # 제외 파일 정의
```

### 버전 관리 X (반드시 제외)
```
❌ .env                            # 실제 환경변수
❌ .env.local                      # 개인 설정
❌ .env.production                 # 운영 비밀키
❌ *.pem, *.key                    # 인증서/키 파일
❌ node_modules/, __pycache__/     # 의존성/캐시
❌ .work/, temp/                   # 임시 파일
❌ *.log                           # 로그 파일
❌ .DS_Store                       # 시스템 파일
```

---

## 🗂️ 설정 파일 배치 원칙

### 1. 루트 vs 하위 폴더
```
프로젝트 전체 설정 → 루트
├── pyproject.toml
├── .pre-commit-config.yaml
└── docker-compose.yml

특정 영역 설정 → 해당 폴더
├── src/core/logging/config.py
├── tests/conftest.py
└── .github/workflows/ci.yml
```

### 2. 환경별 분리 원칙
```
공통 설정:     기본 파일 (docker-compose.yml)
환경별 설정:   접미사로 구분 (.env.{environment})
오버라이드:    .local 접미사 (.env.local)
```

---

# 부록: 체크리스트

---

## ✅ 새 파일 생성 시 확인

### 문서 파일 (Part 1)
```
[ ] Stage 번호가 정확한가? (01~09)
[ ] Type 코드가 올바른가? (F/C/D/S/A/B/T/L/G/M/E)
[ ] Seq 번호가 중복되지 않는가?
[ ] 설명적 이름이 snake_case인가?
[ ] 저장 위치가 올바른가? (docs/{category}/)
```

### 소스 코드 (Part 2)
```
[ ] 올바른 레이어에 위치하는가? (core/domain/application/infrastructure/api)
[ ] 파일명이 역할을 명확히 표현하는가?
[ ] 클래스/함수명이 명명 규칙을 따르는가?
[ ] 도메인 폴더 구조가 일관적인가?
```

### 테스트 파일 (Part 3)
```
[ ] tests/ 하위 올바른 위치에 있는가?
[ ] test_ 접두사가 있는가?
[ ] 소스 파일과 경로가 미러링되는가?
[ ] 테스트 함수명이 기능_조건_결과 패턴인가?
```

### 스크립트/임시 (Part 4)
```
[ ] scripts/ 하위 적절한 폴더에 있는가?
[ ] 동작_대상 패턴을 따르는가?
[ ] 임시 파일은 .work/ 또는 gitignore된 위치인가?
```

### 설정 파일 (Part 5)
```
[ ] 비밀 정보가 포함된 파일은 gitignore되었는가?
[ ] .env.example이 존재하는가?
[ ] 환경별 파일명이 일관적인가?
```

---

## 🔍 빠른 검색 명령어

```bash
# Stage 2 문서 찾기
find docs/ -name "02*"

# 모든 ADR 찾기
find docs/adr/ -name "03A-*"

# 특정 도메인 테스트 찾기
find tests/ -path "*trading*" -name "test_*.py"

# DNA 시스템 코드 찾기
find src/core/ -name "*.py" | head -20
```

---

## 📚 참고 문서

- **01_STAGE_STRUCTURE.md**: 9개 Stage 전체 구조
- **00_CORE_METHODOLOGY.md**: DNA 방법론 개요
- **06G-00_project_standards_guide.md**: 프로젝트 표준 가이드

---

**버전 이력**:
- v2.0 (2025-12-09): 소스코드/테스트/스크립트/설정 규칙 추가 (1호)
- v1.0 (2025-11-12): 초기 작성 - 문서 명명 규칙 (Jason + 2호)
