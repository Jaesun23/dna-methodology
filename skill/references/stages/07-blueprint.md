# Stage 7: 프로젝트 블루프린트 가이드 (Project Blueprint Guide)

> **목적**: 모든 ADR을 통합하여 도메인 전체 설계도 작성 (코드 작성 직전 단계)
>
> **버전**: v4.1 (2025-12-03)
>
> - v4.0 (2025-12-03): Gemini 연구 기반 전면 재작성, 01_DNA_METHODOLOGY_DETAILED.md 기준
> - v2.0 (2025-11-12): 입력/출력 문서 추가
> - v1.0 (2025-11-10): 초기 버전

---

## 📚 이 가이드의 위치

```
DNA 방법론 문서 체계:

Tier 1: 00_CORE_METHODOLOGY.md (전체 맥락)
           ↓
Tier 2: 01_DNA_METHODOLOGY_DETAILED.md (상세 원리)
           ↓
Tier 3: 이 문서 (Stage 7 실행 가이드) ← 지금 여기!
```

**참조 문서**:
- **원리 이해**: `01_DNA_METHODOLOGY_DETAILED.md` **Part 6.1**

---

## 🤔 왜 Project Blueprint가 필요한가?

### ADR vs Blueprint

```
ADR (Stage 3):
├─ "무엇을" 결정했는지
├─ "왜" 그렇게 결정했는지
├─ 개별 결정 단위 (하나의 주제)
└─ 예: "PostgreSQL을 선택한다"

Blueprint (Stage 7):
├─ "어떻게" 구현할 것인지
├─ 모든 ADR을 통합한 전체 그림
├─ 구체적인 구현 명세
└─ 예: "users 테이블 스키마, orders API 엔드포인트..."

관계:
ADR-001 (PostgreSQL) ─┐
ADR-002 (JWT 인증)   ─┼──→ Blueprint (전체 설계도)
ADR-003 (KIS API)    ─┘
```

### Blueprint 없이 구현하면?

```
❌ ADR만 보고 구현:

개발자 A: "ADR에 PostgreSQL 쓴다고 했으니 테이블 만들자"
  → users 테이블: id, name, email

개발자 B: "나도 users 테이블 필요한데..."
  → users 테이블: user_id, username, email_address

결과:
├─ 테이블 스키마 불일치
├─ 필드명 혼란 (id vs user_id, name vs username)
├─ 나중에 대규모 마이그레이션 필요
└─ "처음부터 설계했으면..." 😱
```

```
✅ Blueprint 기반 구현:

07B-01_project_blueprint.md:
────────────────────────────────
## 3. 도메인 모델

### 3.1 User 엔티티
| 필드 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK, core.types.UserId |
| email | str | Unique, EmailStr |
| created_at | datetime | UTC |
| updated_at | datetime | UTC |

참조: ADR-003 (PostgreSQL), PROJECT_STANDARDS.md Ln 45-60

개발자 A, B 모두:
  → 동일한 스키마 구현
  → 동일한 타입 사용 (UserId)
  → 일관된 코드베이스 ✅
```

### 비유: 건축 설계도

```
ADR = 건축 결정:
├─ "콘크리트 구조로 한다" (ADR-001)
├─ "3층 건물로 한다" (ADR-002)
└─ "지하 주차장을 둔다" (ADR-003)

Blueprint = 건축 설계도:
├─ 1층 평면도: 로비, 회의실, 화장실 위치
├─ 2층 평면도: 사무실 배치
├─ 3층 평면도: 임원실, 서버실
├─ 배관도: 수도, 전기, 통신
├─ 구조도: 기둥, 보, 벽체 위치
└─ 모든 치수, 자재 명시

→ 설계도 없이 "콘크리트로 3층 짓자"만 있으면?
  시공자마다 다르게 해석해서 건물이 엉망!
```

---

## 📥 입력 문서

### Stage 3-6에서 전달받는 것

| 파일 | 핵심 내용 | 이 Stage에서 사용 |
|------|----------|-----------------|
| `03A-*_*.md` | 모든 ADR (DNA + 도메인) | 결정 사항 통합 |
| `06D-01_project_standards.md` | 프로젝트 표준 | 규칙 참조 |
| `01C-01_*.md` | 패밀리 분류 | 시스템 특성 확인 |
| `02C-01_*.md` | NFR 우선순위 | 품질 속성 확인 |

---

## 📤 출력 문서

### 필수 산출물

```
docs/
├── 07B-01_project_blueprint.md    # THE 산출물 (전체 설계도)
└── 07S-01_domain_diagrams/        # 도메인별 다이어그램 (선택)
    ├── system_architecture.md
    ├── data_flow.md
    └── entity_relationship.md
```

---

## 🔧 Blueprint 9대 섹션

### 섹션 구조

```
07B-01_project_blueprint.md
────────────────────────────────

1. 시스템 개요        ← 무엇을 만드는가?
2. 아키텍처 구조      ← 전체 구조는?
3. 도메인 모델        ← 핵심 객체는?
4. API 설계          ← 외부 인터페이스는?
5. 데이터베이스 설계   ← 데이터 저장은?
6. 외부 연동          ← 외부 시스템은?
7. 에러 처리          ← 실패 시 대응은?
8. 보안              ← 인증/인가는?
9. 다음 단계          ← Stage 8 연결
```

---

## 📋 작성 단계 (Part 1-4)

### Part 1: 시스템 개요 + 아키텍처 (1시간)

#### 섹션 1: 시스템 개요

```markdown
## 1. 시스템 개요

### 1.1 목적
주식 자동매매 플랫폼 - 사용자가 정의한 전략에 따라 KIS API를 통해 자동으로 주식을 매매

### 1.2 범위
- 포함: 주문 관리, 포트폴리오 조회, 전략 실행, 알림
- 제외: 백테스팅, 리스크 관리 (v2.0 예정)

### 1.3 핵심 기능
| 기능 | 설명 | 우선순위 |
|------|------|---------|
| 주문 생성 | 매수/매도 주문 | P0 |
| 주문 조회 | 주문 상태 확인 | P0 |
| 포트폴리오 | 보유 종목 조회 | P0 |
| 전략 실행 | 자동매매 전략 | P1 |
| 알림 | 체결 알림 | P1 |

### 1.4 패밀리 분류
- **패밀리**: A-A-B (CRUD/트랜잭션)
- **근거**: 금융 거래 → 강한 일관성 필수
- **참조**: 01C-01_family_classification.md
```

#### 섹션 2: 아키텍처 구조

```markdown
## 2. 아키텍처 구조

### 2.1 레이어 구조

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (API Framework + WebSocket)                 │
├─────────────────────────────────────────────────────────┤
│                    Application Layer                     │
│                (Use Cases / Services)                    │
├─────────────────────────────────────────────────────────┤
│                      Domain Layer                        │
│             (Entities, Value Objects, Events)            │
├─────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                   │
│     (Database, External APIs, Cache, Messaging)         │
├─────────────────────────────────────────────────────────┤
│                      Core Layer                          │
│        (DNA Systems - Logging, Config, Types...)         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 의존성 방향

```
Presentation → Application → Domain ← Infrastructure
                               ↑
                             Core
```

- **규칙**: 안쪽으로만 의존 (Domain이 중심)
- **강제**: import-linter (Stage 6 설정)
- **참조**: ADR-004 하이브리드 아키텍처

### 2.3 컴포넌트 구조

```
src/
├── core/           # DNA 시스템 (Stage 5 완료)
├── domain/         # 도메인 레이어
│   ├── orders/     # 주문 도메인
│   ├── portfolio/  # 포트폴리오 도메인
│   └── strategy/   # 전략 도메인
├── application/    # 애플리케이션 레이어
│   ├── orders/     # 주문 유스케이스
│   ├── portfolio/  # 포트폴리오 유스케이스
│   └── strategy/   # 전략 유스케이스
├── infrastructure/ # 인프라 레이어
│   ├── database/   # 리포지토리 구현
│   ├── external/   # 외부 API 클라이언트
│   └── messaging/  # 이벤트 발행
└── api/            # 프레젠테이션 레이어
    ├── routes/     # API 라우터
    ├── schemas/    # 요청/응답 스키마
    └── middleware/ # 미들웨어
```
```

### Part 2: 도메인 모델 설계 (2시간)

#### 섹션 3: 도메인 모델

```markdown
## 3. 도메인 모델

### 3.1 엔티티 (Entities)

#### User 엔티티
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UserId (UUID) | PK | core.types.UserId |
| email | EmailStr | 로그인 이메일 | Unique |
| hashed_password | str | bcrypt 해시 | - |
| is_active | bool | 활성 상태 | Default: True |
| created_at | datetime | 생성 시간 | UTC |
| updated_at | datetime | 수정 시간 | UTC |

**참조**: PROJECT_STANDARDS.md (네이밍 규칙)

#### Order 엔티티 (Aggregate Root)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | OrderId (UUID) | PK | core.types.OrderId |
| user_id | UserId | FK → users | Not Null |
| symbol | str | 종목 코드 | 6자리 |
| side | OrderSide | 매수/매도 | Enum |
| order_type | OrderType | 지정가/시장가 | Enum |
| quantity | int | 주문 수량 | > 0 |
| price | Money | 주문 가격 | >= 0 |
| status | OrderStatus | 주문 상태 | Enum |
| kis_order_id | str | KIS 주문번호 | Nullable |
| created_at | datetime | 생성 시간 | UTC |
| updated_at | datetime | 수정 시간 | UTC |

**도메인 규칙**:
- 시장가 주문 시 price = 0
- status 전이: pending → submitted → filled/cancelled
- 취소는 pending/submitted 상태에서만 가능

**참조**: ADR-101 주문 도메인

#### Portfolio 엔티티
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | PortfolioId (UUID) | PK | - |
| user_id | UserId | FK → users | Unique |
| total_value | Money | 총 평가액 | >= 0 |
| cash_balance | Money | 현금 잔고 | >= 0 |
| updated_at | datetime | 갱신 시간 | UTC |

### 3.2 값 객체 (Value Objects)

#### Money
```
Value Object: Money
├─ amount: Decimal (>= 0)
├─ currency: String (ISO 4217, 기본값: "KRW")
└─ 연산: add, subtract (동일 통화만)
```

**참조**: core/types/ 디렉토리 (Stage 5 구현)

#### OrderSide
```
Enum: OrderSide
├─ BUY = "buy"
└─ SELL = "sell"
```

#### OrderStatus
```
Enum: OrderStatus
├─ PENDING = "pending"           # 생성됨
├─ SUBMITTED = "submitted"       # 거래소 제출됨
├─ FILLED = "filled"             # 체결됨
├─ PARTIALLY_FILLED = "partial"  # 부분 체결
├─ CANCELLED = "cancelled"       # 취소됨
└─ REJECTED = "rejected"         # 거부됨
```

### 3.3 집계 (Aggregates)

#### Order Aggregate
```
Order (Root)
├─ OrderId
├─ UserId (참조)
├─ Money (가격)
├─ OrderStatus
└─ 도메인 메서드
   ├─ submit(): pending → submitted
   ├─ fill(): submitted → filled
   └─ cancel(): pending/submitted → cancelled
```

**불변 규칙**:
- Order는 항상 유효한 상태 전이만 허용
- 취소된 주문은 다시 활성화 불가
- filled 상태에서 수정 불가

### 3.4 도메인 이벤트

| 이벤트 | 발행 시점 | 페이로드 |
|-------|---------|---------|
| OrderCreated | 주문 생성 시 | order_id, user_id, symbol |
| OrderSubmitted | KIS 제출 성공 시 | order_id, kis_order_id |
| OrderFilled | 체결 완료 시 | order_id, filled_price, filled_at |
| OrderCancelled | 취소 완료 시 | order_id, reason |
```



### Part 3: API + 데이터베이스 설계 (2시간)

#### 섹션 4: API 설계

```markdown
## 4. API 설계

### 4.1 엔드포인트 목록

#### Orders API
| Method | Path | 설명 | 인증 |
|--------|------|------|-----|
| POST | /api/v1/orders | 주문 생성 | Required |
| GET | /api/v1/orders | 주문 목록 조회 | Required |
| GET | /api/v1/orders/{id} | 주문 상세 조회 | Required |
| DELETE | /api/v1/orders/{id} | 주문 취소 | Required |

#### Portfolio API
| Method | Path | 설명 | 인증 |
|--------|------|------|-----|
| GET | /api/v1/portfolio | 포트폴리오 조회 | Required |
| GET | /api/v1/portfolio/positions | 보유 종목 조회 | Required |

#### Auth API
| Method | Path | 설명 | 인증 |
|--------|------|------|-----|
| POST | /api/v1/auth/login | 로그인 | - |
| POST | /api/v1/auth/refresh | 토큰 갱신 | Required |

**참조**: ADR-101 API 버저닝

### 4.2 요청/응답 스키마

#### POST /api/v1/orders - 주문 생성

**Request**:
```
CreateOrderRequest:
├─ symbol: String (6자리 숫자, 종목 코드)
├─ side: OrderSide (BUY | SELL)
├─ order_type: OrderType (MARKET | LIMIT)
├─ quantity: Integer (> 0)
└─ price: Decimal? (>= 0, 지정가 주문 시 필수)

검증 규칙:
└─ order_type == LIMIT → price 필수
```

**Response** (201 Created):
```
OrderResponse:
├─ id: UUID
├─ symbol: String
├─ side: OrderSide
├─ order_type: OrderType
├─ quantity: Integer
├─ price: Decimal?
├─ status: OrderStatus
└─ created_at: DateTime

CreateOrderResponse:
├─ order: OrderResponse
└─ message: String ("주문이 생성되었습니다")
```

**Error Responses**:
| Status | Error Code | 설명 |
|--------|-----------|------|
| 400 | 1001 | 검증 오류 (잘못된 종목 코드 등) |
| 401 | 9401 | 인증 필요 |
| 422 | 1002 | 처리 불가 (잔고 부족 등) |
| 502 | 2001 | KIS API 오류 |

**참조**: core/errors/codes.py (Stage 5 구현)

### 4.3 인증 흐름

```
1. 로그인 요청
   POST /api/v1/auth/login
   Body: { "email": "...", "password": "..." }

2. 토큰 발급
   Response: { "access_token": "...", "refresh_token": "...", "expires_in": 3600 }

3. API 요청
   Header: Authorization: Bearer {access_token}

4. 토큰 만료 시
   POST /api/v1/auth/refresh
   Header: Authorization: Bearer {refresh_token}
```

**참조**: ADR-011 보안 (JWT)
```

#### 섹션 5: 데이터베이스 설계

```markdown
## 5. 데이터베이스 설계

### 5.1 테이블 스키마

#### users 테이블
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### orders 테이블
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    symbol VARCHAR(10) NOT NULL,
    side VARCHAR(10) NOT NULL,  -- buy, sell
    order_type VARCHAR(20) NOT NULL,  -- limit, market
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(15, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    kis_order_id VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
CREATE INDEX idx_orders_symbol ON orders(symbol);

-- 복합 인덱스 (자주 사용되는 쿼리)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

#### portfolios 테이블
```sql
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id),
    total_value DECIMAL(15, 2) NOT NULL DEFAULT 0,
    cash_balance DECIMAL(15, 2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);
```

#### positions 테이블 (보유 종목)
```sql
CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    symbol VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    avg_price DECIMAL(15, 2) NOT NULL,
    current_price DECIMAL(15, 2),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(portfolio_id, symbol)
);

-- 인덱스
CREATE INDEX idx_positions_portfolio_id ON positions(portfolio_id);
CREATE INDEX idx_positions_symbol ON positions(symbol);
```

### 5.2 ERD (Entity Relationship Diagram)

```
┌─────────────┐       ┌─────────────┐
│   users     │       │   orders    │
├─────────────┤       ├─────────────┤
│ id (PK)     │───────│ user_id (FK)│
│ email       │   1:N │ symbol      │
│ ...         │       │ status      │
└─────────────┘       └─────────────┘
      │
      │ 1:1
      ▼
┌─────────────┐       ┌─────────────┐
│ portfolios  │       │ positions   │
├─────────────┤       ├─────────────┤
│ id (PK)     │───────│portfolio_id │
│ user_id (FK)│   1:N │ symbol      │
│ total_value │       │ quantity    │
└─────────────┘       └─────────────┘
```

### 5.3 마이그레이션 전략

```
Alembic 사용:

migrations/
├── versions/
│   ├── 001_create_users.py
│   ├── 002_create_orders.py
│   ├── 003_create_portfolios.py
│   └── 004_create_positions.py
└── env.py

명령어:
# 마이그레이션 생성
alembic revision --autogenerate -m "create users table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

**참조**: ADR-003 PostgreSQL
```

### Part 4: 외부 연동 + 에러/보안 (1시간)

#### 섹션 6: 외부 연동

```markdown
## 6. 외부 연동

### 6.1 KIS API 연동

#### 인증 흐름
```
1. OAuth 토큰 발급
   POST https://openapi.koreainvestment.com:9443/oauth2/tokenP
   Body: { "grant_type": "client_credentials", "appkey": "...", "appsecret": "..." }

2. 토큰 저장
   - Redis에 캐시 (TTL: 23시간)
   - 만료 1시간 전 자동 갱신

3. API 호출
   Header: authorization: Bearer {access_token}
           appkey: {appkey}
           appsecret: {appsecret}
```

#### 주문 API
| 기능 | 엔드포인트 | Method |
|------|----------|--------|
| 주문 | /uapi/domestic-stock/v1/trading/order-cash | POST |
| 정정 | /uapi/domestic-stock/v1/trading/order-rvsecncl | POST |
| 취소 | /uapi/domestic-stock/v1/trading/order-rvsecncl | POST |
| 체결 조회 | /uapi/domestic-stock/v1/trading/inquire-daily-ccld | GET |

#### Rate Limiting
```
제한: 초당 20회

대응 전략:
├─ Rate Limiter: 15회/초 (5회 여유)
├─ 요청 큐잉: 초과 시 대기열
├─ 벌크 최적화: 가능한 배치 조회
└─ 참조: ADR-001 KIS API 제한
```

#### 에러 처리
| KIS 코드 | 의미 | 대응 |
|---------|------|------|
| EGW00001 | 토큰 만료 | 자동 갱신 후 재시도 |
| EGW00002 | 권한 없음 | KISAPIError 발생 |
| APBK0013 | 잔고 부족 | ValidationError 변환 |

**참조**: core/external/kis_client.py
```

#### 섹션 7: 에러 처리

```markdown
## 7. 에러 처리

### 7.1 에러 코드 체계

```
1xxx: 도메인 에러 (비즈니스 로직)
├─ 1001: 검증 오류
├─ 1002: 리소스 없음
├─ 1003: 상태 충돌
├─ 1004: 잔고 부족
└─ 1005: 주문 취소 불가

2xxx: 외부 API 에러
├─ 2001: KIS API 오류
├─ 2002: KIS Rate Limit
└─ 2003: KIS 인증 실패

9xxx: 시스템 에러
├─ 9001: 내부 서버 오류
├─ 9002: 데이터베이스 오류
└─ 9003: 캐시 오류
```

### 7.2 에러 응답 형식

```json
{
  "error": {
    "code": "1002",
    "message": "주문을 찾을 수 없습니다",
    "details": {
      "resource": "Order",
      "identifier": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

### 7.3 재시도 전략

| 에러 유형 | 재시도 | 전략 |
|----------|-------|------|
| 네트워크 오류 | 예 | Exponential backoff (1s, 2s, 4s) |
| Rate Limit | 예 | 고정 대기 (1s) |
| 인증 오류 | 예 | 토큰 갱신 후 1회 |
| 비즈니스 오류 | 아니오 | 즉시 실패 반환 |

**참조**: core/errors/exceptions.py (Stage 5 구현)
```

#### 섹션 8: 보안

```markdown
## 8. 보안

### 8.1 인증 (Authentication)

#### JWT 구조
```json
// Access Token (1시간)
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "exp": 1699999999,
  "iat": 1699996399,
  "type": "access"
}

// Refresh Token (7일)
{
  "sub": "user-uuid",
  "exp": 1700599999,
  "iat": 1699996399,
  "type": "refresh"
}
```

#### 토큰 저장
- Access Token: 클라이언트 메모리 (XSS 방지)
- Refresh Token: HttpOnly Cookie (CSRF 방지)

### 8.2 인가 (Authorization)

#### RBAC (Role-Based Access Control)
| Role | 권한 |
|------|-----|
| user | 본인 주문 CRUD, 본인 포트폴리오 조회 |
| admin | 모든 사용자 조회, 시스템 설정 |

#### 리소스 소유권 검증
```
주문 조회 시 소유권 검증 (의사코드):

order = repository.get(order_id)
IF order.user_id != current_user.id:
    THROW ForbiddenError("접근 권한이 없습니다")
```

### 8.3 데이터 보호

| 데이터 | 보호 방법 |
|-------|---------|
| 비밀번호 | bcrypt 해시 (cost=12) |
| API 키 | 환경 변수, 절대 로깅 금지 |
| 개인정보 | 로그 마스킹 (이메일 앞 3자만) |

**참조**: ADR-011 보안
```

#### 섹션 9: 다음 단계

```markdown
## 9. 다음 단계

### Stage 8 (Task Breakdown) 전달 사항

| 섹션 | Task 분해 대상 |
|------|--------------|
| 3. 도메인 모델 | User, Order, Portfolio 엔티티 구현 |
| 4. API 설계 | Orders, Portfolio, Auth API 구현 |
| 5. 데이터베이스 | 테이블 생성, 마이그레이션 |
| 6. 외부 연동 | KIS 클라이언트 구현 |

### 예상 Task 수

```
도메인 레이어:     5-8 Tasks
애플리케이션 레이어: 4-6 Tasks
인프라 레이어:     3-5 Tasks
API 레이어:       4-6 Tasks
────────────────────────────
총:              16-25 Tasks
```

### Stage 8 작업 방향

```
Blueprint 섹션 → Tasks:

섹션 3 (도메인 모델):
├─ Task: User 엔티티 + 테스트
├─ Task: Order 엔티티 + Aggregate 로직 + 테스트
├─ Task: Portfolio 엔티티 + Position + 테스트
└─ Task: 값 객체 + 열거형 + 테스트

섹션 4 (API):
├─ Task: Orders API 엔드포인트
├─ Task: Portfolio API 엔드포인트
├─ Task: Auth API 엔드포인트
└─ Task: 미들웨어 (인증, 로깅)
```
```



---

## 📄 Blueprint 템플릿

### 07B-01_project_blueprint.md

```markdown
# Project Blueprint

> **프로젝트**: [프로젝트명]
> **버전**: v1.0
> **작성일**: YYYY-MM-DD
> **패밀리**: [A-A-B / B-C-A / ...]

---

## 1. 시스템 개요

### 1.1 목적
[시스템이 해결하는 문제와 목표]

### 1.2 범위
- **포함**: [v1.0 범위]
- **제외**: [향후 버전 범위]

### 1.3 핵심 기능
| 기능 | 설명 | 우선순위 |
|------|------|---------|
| [기능1] | [설명] | P0 |
| [기능2] | [설명] | P1 |

### 1.4 참조
- 패밀리 분류: 01C-01_*.md
- NFR 우선순위: 02C-01_*.md

---

## 2. 아키텍처 구조

### 2.1 레이어 구조
[다이어그램]

### 2.2 의존성 방향
[의존성 규칙]

### 2.3 컴포넌트 구조
```
src/
├── core/           # DNA 시스템
├── domain/         # 도메인 레이어
├── application/    # 애플리케이션 레이어
├── infrastructure/ # 인프라 레이어
└── api/            # 프레젠테이션 레이어
```

### 2.4 참조
- 아키텍처 ADR: ADR-004

---

## 3. 도메인 모델

### 3.1 엔티티

#### [엔티티명]
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | [타입] | PK | [제약] |

**도메인 규칙**:
- [규칙1]
- [규칙2]

### 3.2 값 객체
```
Value Object: [ValueObject]
├─ [필드1]: [타입]
└─ [필드2]: [타입]
```

### 3.3 집계 (Aggregates)
```
[AggregateRoot] (Root)
├─ [필드1]
├─ [필드2]
└─ 도메인 메서드
   ├─ [메서드1]()
   └─ [메서드2]()
```

### 3.4 도메인 이벤트
| 이벤트 | 발행 시점 | 페이로드 |
|-------|---------|---------|
| [이벤트명] | [시점] | [필드들] |

---

## 4. API 설계

### 4.1 엔드포인트 목록
| Method | Path | 설명 | 인증 |
|--------|------|------|-----|
| [METHOD] | [PATH] | [설명] | [Required/-] |

### 4.2 요청/응답 스키마

#### [엔드포인트명]
**Request**:
```
[RequestSchema]:
├─ [필드1]: [타입]
└─ [필드2]: [타입]
```

**Response**:
```
[ResponseSchema]:
├─ [필드1]: [타입]
└─ [필드2]: [타입]
```

### 4.3 참조
- API ADR: ADR-101

---

## 5. 데이터베이스 설계

### 5.1 테이블 스키마

#### [테이블명]
```sql
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY,
    [field] [type] [constraints],
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_[name] ON [table]([column]);
```

### 5.2 ERD
[다이어그램]

### 5.3 참조
- 데이터베이스 ADR: ADR-003

---

## 6. 외부 연동

### 6.1 [외부 시스템명]

#### 인증 흐름
[인증 방법]

#### API 목록
| 기능 | 엔드포인트 | Method |
|------|----------|--------|
| [기능] | [URL] | [METHOD] |

#### Rate Limiting
[제한 및 대응 전략]

### 6.2 참조
- 외부 연동 ADR: ADR-001

---

## 7. 에러 처리

### 7.1 에러 코드 체계
```
1xxx: 도메인 에러
2xxx: 외부 API 에러
9xxx: 시스템 에러
```

### 7.2 에러 응답 형식
```json
{
  "error": {
    "code": "[코드]",
    "message": "[메시지]",
    "details": {}
  }
}
```

### 7.3 재시도 전략
| 에러 유형 | 재시도 | 전략 |
|----------|-------|------|
| [유형] | [예/아니오] | [전략] |

---

## 8. 보안

### 8.1 인증 (Authentication)
[JWT / OAuth / 등]

### 8.2 인가 (Authorization)
[RBAC / ABAC / 등]

### 8.3 데이터 보호
| 데이터 | 보호 방법 |
|-------|---------|
| [데이터] | [방법] |

### 8.4 참조
- 보안 ADR: ADR-011

---

## 9. 다음 단계

### Stage 8 전달 사항
- 도메인 모델 → 엔티티 구현 Tasks
- API 설계 → 엔드포인트 구현 Tasks
- 데이터베이스 → 마이그레이션 Tasks
```

---

## ✏️ 작성 예시: 주식 거래 플랫폼 (요약)

### 예시: 도메인 모델 섹션

```markdown
## 3. 도메인 모델

### 3.1 Order 엔티티 (Aggregate Root)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | OrderId (UUID) | PK | core.types.OrderId |
| user_id | UserId | FK → users | Not Null |
| symbol | str | 종목 코드 | 6자리 정규식 |
| side | OrderSide | 매수/매도 | Enum: buy, sell |
| order_type | OrderType | 주문 유형 | Enum: limit, market |
| quantity | int | 수량 | > 0 |
| price | Money | 가격 | >= 0, 시장가는 None |
| status | OrderStatus | 상태 | Enum |
| kis_order_id | str | KIS 주문번호 | Nullable |
| created_at | datetime | 생성 시간 | UTC |
| updated_at | datetime | 수정 시간 | UTC |

**도메인 규칙**:
1. 시장가 주문 시 price = None
2. status 전이 규칙:
   - pending → submitted (KIS 제출 시)
   - submitted → filled (체결 시)
   - submitted → cancelled (취소 시)
   - pending → cancelled (취소 시)
3. filled 또는 cancelled 상태에서 수정 불가
4. 취소는 pending/submitted 상태에서만 가능

**Aggregate 메서드** (의사코드):
```
Order:
  submit(external_order_id):
    PRE: status == PENDING
    POST: status = SUBMITTED, emit OrderSubmitted
    
  fill(filled_price, filled_at):
    PRE: status == SUBMITTED
    POST: status = FILLED, emit OrderFilled
    
  cancel(reason):
    PRE: status IN (PENDING, SUBMITTED)
    POST: status = CANCELLED, emit OrderCancelled
```

**참조**:
- ADR-101: 주문 도메인 설계
- core/types: UserId, OrderId, Money
- PROJECT_STANDARDS.md: 네이밍 규칙
- **언어별 구현**: docs/manuals/ 참조
```

### 예시: API 설계 섹션

```markdown
## 4. API 설계

### 4.2 POST /api/v1/orders - 주문 생성

**Request Schema**:
```
CreateOrderRequest:
├─ symbol: String (6자리 숫자, 종목 코드)
│   └─ pattern: "^[0-9]{6}$"
├─ side: OrderSide (BUY | SELL)
├─ order_type: OrderType (MARKET | LIMIT)
├─ quantity: Integer (> 0)
└─ price: Decimal? (>= 0, 시장가는 null)

검증 규칙:
├─ order_type == LIMIT → price 필수
└─ order_type == MARKET → price null 필수
```

**예시 요청**:
```json
{
    "symbol": "005930",
    "side": "buy",
    "order_type": "limit",
    "quantity": 10,
    "price": 70000
}
```

**Response Schema** (201 Created):
```
OrderResponse:
├─ id: UUID
├─ symbol: String
├─ side: OrderSide
├─ order_type: OrderType
├─ quantity: Integer
├─ price: Decimal?
├─ status: OrderStatus
├─ external_order_id: String?
├─ created_at: DateTime
└─ updated_at: DateTime

CreateOrderResponse:
├─ order: OrderResponse
└─ message: String
```

**예시 응답**:
```json
{
    "order": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "symbol": "005930",
        "side": "buy",
        "order_type": "limit",
        "quantity": 10,
        "price": 70000,
        "status": "pending",
        "external_order_id": null,
        "created_at": "2025-12-03T10:30:00Z",
        "updated_at": "2025-12-03T10:30:00Z"
    },
    "message": "주문이 생성되었습니다"
}
```

**Error Responses**:
```json
// 400 Bad Request - 검증 오류
{
    "error": {
        "code": "1001",
        "message": "종목 코드 형식이 올바르지 않습니다",
        "details": {
            "field": "symbol",
            "value": "12345",
            "expected": "6자리 숫자"
        }
    }
}

// 422 Unprocessable Entity - 잔고 부족
{
    "error": {
        "code": "1004",
        "message": "잔고가 부족합니다",
        "details": {
            "required": 700000,
            "available": 500000
        }
    }
}

// 502 Bad Gateway - 외부 API 오류
{
    "error": {
        "code": "2001",
        "message": "외부 API 호출에 실패했습니다",
        "details": {
            "external_code": "EGW00001",
            "external_message": "토큰이 만료되었습니다"
        }
    }
}
```

**라우터 구현 가이드** (의사코드):
```
ENDPOINT POST /api/v1/orders
  INPUT: CreateOrderRequest, current_user (인증됨)
  OUTPUT: CreateOrderResponse (201 Created)
  
  STEPS:
    1. 로깅: "주문 생성 요청", user_id, symbol, side
    2. 서비스 호출: order_service.create_order(...)
    3. 로깅: "주문 생성 완료", order_id
    4. 응답 반환
    
  에러 처리:
    ├─ ValidationError → 400
    ├─ InsufficientBalanceError → 422
    └─ ExternalAPIError → 502
```

**언어별 구현 예시**: docs/manuals/ 참조
```

---

## ✅ Stage 7 완료 체크리스트

### 시스템 개요 (섹션 1)

- [ ] 목적 명확히 작성
- [ ] 범위 (포함/제외) 정의
- [ ] 핵심 기능 + 우선순위 (P0/P1/P2)
- [ ] 패밀리 분류 참조

### 아키텍처 구조 (섹션 2)

- [ ] 레이어 다이어그램
- [ ] 의존성 방향 규칙
- [ ] 컴포넌트 구조 (디렉토리)
- [ ] 아키텍처 ADR 참조

### 도메인 모델 (섹션 3)

- [ ] 모든 엔티티 정의 (필드, 타입, 제약)
- [ ] 도메인 규칙 명시
- [ ] 값 객체 정의
- [ ] Aggregate 경계 + 메서드
- [ ] 도메인 이벤트 목록

### API 설계 (섹션 4)

- [ ] 엔드포인트 목록 (Method, Path, 인증)
- [ ] 요청/응답 스키마 (타입 검증 포함)
- [ ] 에러 응답 형식
- [ ] 인증 흐름

### 데이터베이스 설계 (섹션 5)

- [ ] 테이블 스키마 (SQL)
- [ ] 인덱스 전략
- [ ] ERD
- [ ] 마이그레이션 전략

### 외부 연동 (섹션 6)

- [ ] 외부 시스템 인증 흐름
- [ ] API 목록
- [ ] Rate Limiting 대응
- [ ] 에러 처리 매핑

### 에러 처리 (섹션 7)

- [ ] 에러 코드 체계
- [ ] 에러 응답 형식
- [ ] 재시도 전략

### 보안 (섹션 8)

- [ ] 인증 방식 (JWT 구조)
- [ ] 인가 방식 (RBAC/ABAC)
- [ ] 데이터 보호 방법

### 산출물 생성

- [ ] `07B-01_project_blueprint.md` 작성
- [ ] Stage 8 전달 사항 정리

---

## 🔗 Stage 7 → Stage 8 연결

### Stage 8에 전달하는 것

| 전달 항목 | 내용 | 용도 |
|----------|------|------|
| Blueprint 섹션 3 | 도메인 모델 | 엔티티 구현 Tasks |
| Blueprint 섹션 4 | API 설계 | 엔드포인트 구현 Tasks |
| Blueprint 섹션 5 | 데이터베이스 | 마이그레이션 Tasks |
| Blueprint 섹션 6 | 외부 연동 | 클라이언트 구현 Tasks |

### Stage 8 미리보기

```
Stage 8: Task Breakdown

목표: Blueprint를 AI가 한 세션에 완료할 수 있는 크기로 분해

분해 기준:
├─ 체크리스트: 100-150줄 범위
├─ 예상 시간: 2-4시간
├─ 컨텍스트: 80-90K 토큰 이내
└─ 독립적 테스트 가능

예상 Task 수:
├─ 도메인 레이어: 5-8 Tasks
├─ 애플리케이션 레이어: 4-6 Tasks
├─ 인프라 레이어: 3-5 Tasks
└─ API 레이어: 4-6 Tasks
────────────────────────────────
총: 16-25 Tasks
```

---

## ⏪ 이전 Stage 검증 및 수정 프로토콜 (가장 Critical!)

### 왜 Stage 7이 가장 Critical한가?

```
Stage 7 = 통합의 정점 (Integration Apex)
────────────────────────────────────────────

Stage 1-6의 모든 결과물이 여기서 통합:
├─ Stage 1: 패밀리, NFR → Blueprint 전체 방향
├─ Stage 2: 제약, 충돌 → 기술 선택 반영
├─ Stage 3: ADR → 모든 결정 참조
├─ Stage 4: DNA 청사진 → 기반 시스템 참조
├─ Stage 5: DNA 구현 → core/ 모듈 참조
└─ Stage 6: 표준 → 규칙 준수 확인

⚠️ Stage 7에서 오류 미발견 시:
├─ Stage 8: 잘못된 Task 분해
├─ Stage 9: 잘못된 코드 구현
└─ 전체 재작업 필요 (10시간+)

✅ Stage 7에서 오류 수정 시:
├─ Blueprint만 수정 (2-3시간)
├─ Stage 8-9 정상 진행
└─ 비용 최소화
```

### 검증 시점
- Stage 7 시작 전 필수 체크 (모든 Stage!)
- 각 섹션 작성 완료 후 ADR과 교차 검증
- 전체 Blueprint 완료 후 최종 검증

### 검증 대상 (전체 Stage!)

| Stage | 산출물 | 검증 항목 |
|-------|--------|----------|
| Stage 1 | 01C-01_*.md | 패밀리 특성이 Blueprint에 반영? |
| Stage 1 | 01C-01_*.md | NFR 우선순위가 API/DB 설계에 반영? |
| Stage 2 | 02C-01_*.md | 기술 제약이 기술 선택에 반영? |
| Stage 2 | 02C-01_*.md | 충돌 해결이 트레이드오프로 반영? |
| Stage 3 | 03A-*_*.md | 모든 ADR이 Blueprint에 참조/반영? |
| Stage 4 | 04B-01_*.md | DNA 청사진이 core/ 참조로 반영? |
| Stage 5 | 05D-01_*.md | DNA 구현이 사용 예시로 반영? |
| Stage 6 | 06D-01_*.md | 표준 규칙이 코드 예시에 준수? |

### 오류 발견 시 프로토콜 (6단계)

```
Stage 7에서 Stage 1-6 오류 발견 시:

Step 1: 오류 발견 및 문서화
├─ 발견 위치: Blueprint 섹션 [N]
├─ 오류 내용: [구체적 설명]
├─ 영향 Stage: Stage [1-6]
├─ 심각도: [Critical/Major/Minor]
└─ 기록: 07B-01에 "발견된 이슈" 섹션 추가

Step 2: 영향 범위 파악 (가장 중요!)
├─ 직접 영향: Stage [N]
├─ 간접 영향: Stage [N+1] ~ Stage 6
├─ Blueprint 영향 섹션: [해당 섹션 번호]
├─ 재작업 예상 시간: [X]시간
└─ 기록: 영향 범위 문서화

Step 3: 해당 Stage로 이동 → 수정
├─ Stage [N] 산출물 수정
├─ 수정 이력 기록
├─ 버전 업데이트 (v1.0 → v1.1)
└─ 수정 완료 검증

Step 4: 중간 Stage 전파 (N+1 ~ 6)
├─ 각 Stage 산출물 영향 확인
├─ 필요 시 연쇄 수정
├─ 수정 이력 기록
└─ 일관성 검증

Step 5: Stage 7 재진행
├─ 수정된 입력으로 Blueprint 해당 섹션 재작성
├─ 전체 Blueprint 일관성 검토
└─ 9대 섹션 교차 검증

Step 6: 재진행 결과 검증
├─ 오류가 해결되었는지 확인
├─ 새로운 문제 발생 여부 확인
├─ 최종 승인
└─ Stage 8 전달 ✅
```

### 섹션별 흔한 오류 패턴

| 섹션 | 오류 유형 | 영향 Stage | 해결 |
|------|----------|-----------|------|
| 섹션 2 (아키텍처) | 레이어 정의 불일치 | Stage 4 | DNA 청사진 수정 |
| 섹션 3 (도메인) | 엔티티 필드 ADR 불일치 | Stage 3 | ADR 수정 또는 도메인 수정 |
| 섹션 4 (API) | NFR 성능 요구 미반영 | Stage 1 | NFR 현실화 또는 API 최적화 |
| 섹션 5 (DB) | 기술 제약 미반영 | Stage 2 | DB 기술 재선택 |
| 섹션 6 (외부 연동) | ADR 누락 (Rate Limit 등) | Stage 3 | ADR 추가 |
| 섹션 7 (에러) | 에러 코드 표준 불일치 | Stage 6 | 표준 수정 |
| 섹션 8 (보안) | 인증 ADR 미반영 | Stage 3 | ADR 확인 후 반영 |

### 추적성 (Critical!)

```
수정 이력 파일: docs/revision_log.md

예시:
────────────────────────────────────────────
## 2025-12-03 (Stage 7 Blueprint 작성 중)

### Issue #003: Order 취소 API 누락
- **발견 Stage**: Stage 7 Blueprint 섹션 4
- **영향 Stage**: Stage 3 ADR
- **오류**: Order 취소 기능 ADR 없음
- **수정**: ADR-017 "Order 취소 정책" 추가
- **영향 범위**: 
  - Stage 3: ADR-017 추가
  - Stage 7: 섹션 4에 DELETE /orders/{id} 추가
- **수정자**: Jason
- **검증**: 1호/2호 확인 완료
────────────────────────────────────────────

Blueprint 참조:
각 섹션에 관련 ADR 명시적 참조:
"참조: ADR-101 (Order 엔티티 설계)"
"참조: ADR-017 (Order 취소 정책)"
```

---

## 💡 핵심 원칙 요약

### Blueprint의 목적

```
ADR (Stage 3):
├─ "무엇을" 결정했는지
├─ "왜" 그렇게 결정했는지
└─ 개별 결정 단위

Blueprint (Stage 7):
├─ "어떻게" 구현할 것인지
├─ 모든 ADR을 통합한 전체 그림
├─ 구체적인 구현 명세
└─ 코드 작성 직전 단계

관계: 여러 ADR → 하나의 Blueprint
```

### 9대 섹션

```
1. 시스템 개요        ← 무엇을 만드는가?
2. 아키텍처 구조      ← 전체 구조는?
3. 도메인 모델        ← 핵심 객체는? (가장 중요!)
4. API 설계          ← 외부 인터페이스는?
5. 데이터베이스 설계   ← 데이터 저장은?
6. 외부 연동          ← 외부 시스템은?
7. 에러 처리          ← 실패 시 대응은?
8. 보안              ← 인증/인가는?
9. 다음 단계          ← Stage 8 연결
```

### SoT (Skeleton-of-Thought) 적용

```
Step 1: 목차 (뼈대) 생성
────────────────────────────────
9대 섹션 목차 먼저 작성

Step 2: 각 섹션 병렬 확장
────────────────────────────────
세션 1: 1-3 섹션 작성 (개요, 아키텍처, 도메인)
세션 2: 4-6 섹션 작성 (API, DB, 외부 연동)
세션 3: 7-9 섹션 작성 (에러, 보안, 다음 단계)

Step 3: 전체 일관성 검토
────────────────────────────────
├─ ADR 참조 확인
├─ PROJECT_STANDARDS 참조 확인
└─ 섹션 간 모순 확인
```

---

**Remember**: 
- ADR은 "결정", Blueprint는 "설계도"
- Blueprint 없이 구현 = 개발자마다 다른 해석
- 9대 섹션으로 모든 측면 커버
- Stage 8에서 실행 가능한 Task로 분해

*Blueprint는 모든 ADR을 통합하여 "코드 작성 직전 단계"의 완전한 설계도입니다.*
