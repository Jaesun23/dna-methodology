# 안전-임계 IoT 패밀리 (A-B-A) - 기술 매트릭스

**작성일**: 2025-11-12  
**패밀리**: 안전-임계 IoT (A-B-A)  
**검증 사례**: SCADA (5-250ms), IoT 긴급 경보 (450ms), 산업 안전 시스템

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 A-B-A 특성이 강제하는 것

#### A (치명적 실패) → 안전 시스템 필수

**특성**:
- 실패 시 인명 손실, 재산 피해
- 산업 재해, 화재, 폭발 위험
- 긴급 대응 필수 (경보, 셧다운)
- 규제 준수 (SIL 2+, UL, IEC)

**강제되는 기술적 요구**:
```
✅ Fail-Safe 설계 (기본값 안전)
✅ 중복성 (Redundancy)
✅ 워치독 (Watchdog) 타이머
✅ 감사 로그 (Audit Trail)
✅ 긴급 셧다운 (Emergency Shutdown)
```

**검증 사례**:
- 산업 제어 시스템 (SCADA): 센서 고장 시 자동 정지
- 긴급 경보 (EAS): 10분 내 전국 경보, FEMA/FCC

---

#### B (반구조화 데이터) → 센서 융합 필수

**특성**:
- JSON, XML 센서 데이터
- 가변 스키마 (센서별 다른 필드)
- 시계열 데이터 (온도, 압력, 진동)
- 다중 센서 융합 (Sensor Fusion)

**강제되는 기술적 요구**:
```
✅ 유연한 스키마 (Flexible Schema)
✅ 시계열 DB (Time-Series DB)
✅ 센서 융합 알고리즘
✅ JSON/XML 파싱
✅ 동적 필드 처리
```

**검증 사례**:
- IoT 센서: 온도 + 습도 + 진동 + 가스 농도
- SCADA: PLCraw 데이터 + 알람 메시지 + 상태 정보

---

#### A (밀리초 응답) → 실시간 처리 필수

**특성**:
- SCADA: 5-250ms 응답
- 긴급 경보: 450ms 미만
- 산업 제어: 수 밀리초 루프
- Edge Computing 필수

**강제되는 기술적 요구**:
```
✅ Edge Computing (로컬 처리)
✅ 경량 프로토콜 (MQTT, CoAP)
✅ 비동기 처리
✅ 우선순위 큐
✅ 저지연 네트워크 (5G, LoRaWAN)
```

**검증 사례**:
- Uber GPS: 2-5초 위치 업데이트
- 제조 안전: 밀리초급 센서-액추에이터 루프

---

### 1.2 이 패밀리에 필요한 DNA 시스템 및 메인 서비스

#### DNA 11개 시스템 중 필요한 것

A-B-A 패밀리는 다음 DNA 시스템이 필요합니다:

| DNA 시스템 | 중요도 | 이유 |
|-----------|-------|------|
| 1. Testing | ✅ 필수 | 안전 로직 검증, SIL 준수 |
| 2. Code Quality | ✅ 필수 | 결함 없는 코드 필수 |
| 3. Architecture | ✅ 필수 | Fail-safe 모듈 분리 |
| 4. **Type System** | **⭐⭐⭐ 매우 중요** | **컴파일 타임 안전성, SIL 인증** |
| 5. **Error Handling** | **⭐⭐⭐ 매우 중요** | **Fail-safe 전략, Watchdog** |
| 6. Configuration | ✅ 필수 | 센서 임계값, 타임아웃 설정 |
| 7. Identity & Access | ✅ 필수 | 센서 인증, 명령 권한 |
| 8. Observability | ✅ 필수 | 센서 상태, 알람 모니터링 |
| 9. API Gateway | ⚠️ 조건부 | SCADA 연동 시 필요 |
| 10. **Resilience** | **⭐⭐⭐ 매우 중요** | **N+1 중복, Failover, 생명 안전** |
| 11. Performance | ✅ 필수 | 밀리초 응답 보장 |

**특별히 중요한 DNA 시스템 (⭐⭐⭐)**:
- **Type System**: 런타임 에러 0을 목표, 컴파일 타임 검증 필수 (SIL 2+ 인증)
- **Error Handling**: 모든 에러는 안전 모드 전환, Watchdog 필수, 복구 불가 시 셧다운
- **Resilience**: 센서/액추에이터 N+1 중복, 5-250ms 페일오버, 크로스 체크

→ **Part 2.5에서 이 3가지 DNA 시스템의 기술 옵션을 다룹니다.**

#### 메인 서비스 필수 요소 (패밀리 강제)

A-B-A 패밀리는 다음 3가지 메인 서비스 기술을 **반드시** 포함해야 합니다:

#### 1. IoT 메시징 (MQTT/AMQP) (필수!)
**역할**: 센서 데이터 수집, 명령 전송
**이유**: 반구조화(B) + 밀리초(A)
**선택지**: EMQX, AWS IoT Core, RabbitMQ

#### 2. 시계열 DB (필수!)
**역할**: 센서 데이터 저장, 이력 조회
**이유**: 반구조화(B) + 시계열
**선택지**: InfluxDB, TimescaleDB, DynamoDB

#### 3. Edge Computing (필수!)
**역할**: 로컬 실시간 처리, 긴급 대응
**이유**: 치명적(A) + 밀리초(A)
**선택지**: AWS IoT Greengrass, Azure IoT Edge, K3s

---

## Part 2: 메인 서비스 기술 선택 ⭐⭐⭐

### 2.1 IoT 메시징 선택

**패밀리 요구**:
- 경량 프로토콜 (배터리 제약)
- QoS 보장 (메시지 손실 방지)
- 대규모 연결 (수만~수백만 센서)
- 낮은 레이턴시 (밀리초~초)

---

#### 옵션 1: EMQX (Enterprise)

**핵심 스펙**:
- **연결 처리량**: 500만+ 동시 연결
- **메시지 처리량**: 초당 100만+ 메시지
- **레이턴시**: 밀리초 미만 (단일 홉)
- **프로토콜**: MQTT 3.1/3.1.1/5.0, MQTT-SN, CoAP, LwM2M

**비용**:
- **오픈소스**: 무료 (EMQX Broker)
- **Enterprise**: $5,000~$20,000/년 (노드당)
- **클라우드**: $0.15~$0.30/million messages

**장점**:
- ⚡ 초대규모 확장 (500만+ 연결)
- 🔧 완벽한 MQTT 지원
- 📡 다중 프로토콜 (MQTT, CoAP, LwM2M)
- 💪 고가용성 (클러스터링)
- 🔐 TLS/SSL, 인증/권한

**단점**:
- 💰 Enterprise 고가
- 🧑‍💻 복잡한 운영 (클러스터)
- 📚 학습 곡선
- 🔧 튜닝 필요

**적합한 경우**:
- 산업 IoT (수만~수백만 센서)
- SCADA, 스마트 팩토리
- 높은 신뢰성 필수
- 예산 $20K~$100K /year

**검증 사례**: 중국 제조업, 스마트 시티 프로젝트

---

#### 옵션 2: AWS IoT Core

**핵심 스펙**:
- **연결 처리량**: 무제한 (자동 확장)
- **메시지 처리량**: 사용량 기반
- **레이턴시**: 수십~수백 밀리초
- **프로토콜**: MQTT, MQTT over WebSocket, HTTPS

**비용**:
- **연결 비용**: $0.08/million connection-minutes
- **메시지 비용**: $1/million messages (first 1B/월)
- **예상**: 월 $1,000~$10,000 (중규모)

**장점**:
- 🤖 완전 관리형 (운영 부담 없음)
- 🚀 무제한 확장
- 🔗 AWS 통합 (Lambda, S3, DynamoDB)
- 🔐 강력한 보안 (X.509 인증)
- 📊 내장 규칙 엔진

**단점**:
- 🔒 AWS 종속
- 💰 대규모 시 비용 급증
- 📊 제한적 프로토콜 (MQTT 중심)
- 🌐 글로벌 배포 복잡

**적합한 경우**:
- AWS 중심 조직
- 소규모~중규모 (수만~수십만 센서)
- 빠른 프로토타이핑
- 운영 부담 최소화

**검증 사례**: 스마트 홈, 소규모 공장 자동화

---

#### 옵션 3: RabbitMQ (MQTT 플러그인)

**핵심 스펙**:
- **연결 처리량**: 수만~수십만 연결
- **메시지 처리량**: 초당 3만 메시지
- **레이턴시**: 밀리초~초
- **프로토콜**: MQTT, AMQP, STOMP, HTTP

**비용**:
- **오픈소스**: 무료
- **Self-hosted**: 월 $200~$2,000 (VM 비용)
- **CloudAMQP**: $19~$1,199/월

**장점**:
- 💰 저렴한 비용
- 📚 성숙한 기술
- 🔧 간단한 운영
- 🔌 다양한 프로토콜
- 💪 메시지 라우팅 유연성

**단점**:
- 📉 제한적 확장 (수만 연결)
- ⚡ EMQX 대비 낮은 성능
- 🔧 MQTT 기능 제한 (플러그인)
- 📊 대규모 IoT 부적합

**적합한 경우**:
- 소규모 IoT (수천~수만 센서)
- 레거시 통합 (AMQP)
- 예산 $5K~$30K /year
- 간단한 아키텍처

**검증 사례**: 스타트업 IoT, 빌딩 자동화

---

#### IoT 메시징 비교표

| 항목 | EMQX | AWS IoT Core | RabbitMQ |
|------|------|--------------|----------|
| **연결 수** | 500만+ | 무제한 | 수만 |
| **메시지/초** | 100만+ | 사용량 기반 | ~3만 |
| **레이턴시** | <10ms | 수십~수백ms | 밀리초~초 |
| **비용** | $5K~$20K/년 | $1K~$10K/월 | $200~$2K/월 |
| **운영** | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 | ⚙️⚙️ 중간 |

**의사결정 가이드**:
```
센서 > 10만? → EMQX
  └─ NO
     ↓
AWS 중심? → AWS IoT Core
  └─ NO
     ↓
센서 < 5만? → RabbitMQ
  └─ NO → AWS IoT Core
```

---

### 2.2 시계열 DB 선택

**패밀리 요구**:
- 빠른 쓰기 (초당 수십만~수백만 포인트)
- 시간 기반 쿼리 최적화
- 압축 (저장 공간 절약)
- 다운샘플링 (Downsampling)

---

#### 옵션 1: InfluxDB (Enterprise)

**핵심 스펙**:
- **쓰기 처리량**: 초당 100만+ 포인트
- **압축**: 10:1 이상
- **레이턴시**: 밀리초 미만 (쓰기)
- **보존 정책**: 자동 다운샘플링

**비용**:
- **오픈소스**: 무료 (InfluxDB OSS)
- **Cloud**: $50~$500/월
- **Enterprise**: $10,000~$50,000/년

**장점**:
- ⚡ 초고속 쓰기
- 🔧 IoT 최적화 (Telegraf 통합)
- 📊 강력한 쿼리 (Flux, InfluxQL)
- 💾 효율적 압축
- 🕐 자동 다운샘플링

**단점**:
- 💰 Enterprise 고가
- 📊 제한적 분산 (클러스터링 Enterprise만)
- 🔧 메모리 사용량 높음
- 📈 대규모 확장 어려움

**적합한 경우**:
- IoT 센서 데이터 (초당 수십만 포인트)
- SCADA, 제조 라인
- 실시간 대시보드
- 예산 $10K~$100K /year

**검증 사례**: Cisco IoT, Salesforce 모니터링

---

#### 옵션 2: TimescaleDB (PostgreSQL 확장)

**핵심 스펙**:
- **쓰기 처리량**: 초당 10만 포인트
- **압축**: Native 압축 (7:1)
- **레이턴시**: <10ms (쓰기)
- **쿼리**: Full SQL 지원

**비용**:
- **오픈소스**: 무료
- **Timescale Cloud**: $50~$500/월
- **Enterprise**: $5,000~$20,000/년

**장점**:
- 🔍 Full SQL 지원
- 📊 복잡한 조인 가능
- 🛠️ PostgreSQL 생태계
- 💰 상대적 저렴
- 🔧 익숙한 운영

**단점**:
- ⚡ InfluxDB 대비 느림
- 📈 확장 제한 (vs 분산 DB)
- 💾 압축률 낮음
- 🔧 튜닝 필요

**적합한 경우**:
- SQL 필수 (복잡한 분석)
- PostgreSQL 팀 역량
- 중소규모 (초당 수만 포인트)
- 예산 $5K~$50K /year

**검증 사례**: 에너지 모니터링, 스마트 빌딩

---

#### 옵션 3: DynamoDB (AWS)

**핵심 스펙**:
- **쓰기 처리량**: 사용량 기반 (무제한)
- **레이턴시**: 단일 자릿수 밀리초
- **확장**: 자동 스케일링
- **TTL**: 자동 데이터 만료

**비용**:
- **On-Demand**: $1.25/million writes
- **Provisioned**: $0.00065/WCU/hour
- **예상**: 월 $500~$5,000

**장점**:
- 🤖 완전 관리형
- 🚀 무제한 확장
- 🔗 AWS 통합
- 💵 사용량 기반 과금
- 🕐 자동 TTL

**단점**:
- 🔒 AWS 종속
- 💰 대규모 시 비용 급증
- 📊 제한적 쿼리 (NoSQL)
- 🔧 시계열 최적화 부족

**적합한 경우**:
- AWS 중심
- 소규모~중규모
- 빠른 프로토타이핑
- 운영 부담 최소화

**검증 사례**: AWS IoT 사용자, 스타트업

---

#### 시계열 DB 비교표

| 항목 | InfluxDB | TimescaleDB | DynamoDB |
|------|----------|-------------|----------|
| **쓰기/초** | 100만+ | 10만 | 사용량 기반 |
| **SQL** | Flux/InfluxQL | ✅ Full SQL | ❌ NoSQL |
| **압축** | 10:1 | 7:1 | N/A |
| **비용** | $10K~$50K/년 | $5K~$20K/년 | $500~$5K/월 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️ 중간 | ⚙️ 낮음 |

**의사결정 가이드**:
```
쓰기 > 10만/초? → InfluxDB
  └─ NO
     ↓
SQL 필수? → TimescaleDB
  └─ NO
     ↓
AWS 중심? → DynamoDB
  └─ NO → InfluxDB
```

---

### 2.3 Edge Computing 선택

**패밀리 요구**:
- 로컬 실시간 처리 (밀리초)
- 오프라인 동작 (네트워크 단절 시)
- 경량 (저전력, 제한된 리소스)
- 클라우드 동기화

---

#### 옵션 1: AWS IoT Greengrass

**핵심 스펙**:
- **레이턴시**: 밀리초급 (로컬)
- **언어**: Python, Node.js, Java, C++
- **배포**: Over-the-Air (OTA)
- **오프라인**: 완전 지원

**비용**:
- **소프트웨어**: 무료
- **디바이스**: $10~$500 (하드웨어)
- **클라우드 연동**: AWS IoT Core 비용

**장점**:
- ⚡ 로컬 실시간 처리
- 🔗 AWS 완벽 통합
- 🤖 Lambda 로컬 실행
- 🔐 강력한 보안 (X.509)
- 📡 오프라인 동작

**단점**:
- 🔒 AWS 종속
- 💰 디바이스 비용 (ARM/x86)
- 🔧 복잡한 설정
- 📊 ML 추론 제한적

**적합한 경우**:
- AWS 중심 IoT
- 중간~고성능 Edge (Raspberry Pi 이상)
- 오프라인 필수
- 예산 $100~$500 per device

**검증 사례**: 석유/가스 리모트 모니터링, 스마트 빌딩

---

#### 옵션 2: Azure IoT Edge

**핵심 스펙**:
- **레이턴시**: 밀리초급 (로컬)
- **언어**: C#, Python, Node.js, Java, C
- **컨테이너**: Docker 기반
- **AI**: Azure ML 로컬 배포

**비용**:
- **소프트웨어**: 무료
- **디바이스**: $10~$500 (하드웨어)
- **클라우드 연동**: Azure IoT Hub 비용

**장점**:
- ⚡ 로컬 AI 추론 (ML 모델)
- 🐳 Docker 컨테이너 (표준)
- 🔗 Azure 통합
- 🔐 보안 모듈 (TPM)
- 📡 오프라인 동작

**단점**:
- 🔒 Azure 종속
- 💰 디바이스 비용
- 🧑‍💻 .NET 편향
- 📊 대규모 관리 복잡

**적합한 경우**:
- Azure 중심 조직
- AI/ML 추론 필요
- Docker 친숙
- 예산 $100~$500 per device

**검증 사례**: 제조업 품질 검사 (AI), 소매 매장 분석

---

#### 옵션 3: K3s (경량 Kubernetes)

**핵심 스펙**:
- **메모리**: 512MB RAM 이상
- **언어**: 모든 컨테이너화 앱
- **배포**: GitOps (Flux, ArgoCD)
- **클라우드**: 멀티 클라우드 지원

**비용**:
- **오픈소스**: 무료
- **디바이스**: $10~$200 (하드웨어)
- **관리**: Rancher (무료/Enterprise)

**장점**:
- 💰 완전 무료 (오픈소스)
- 🌐 멀티 클라우드 (AWS, Azure, GCP)
- 🔧 표준 Kubernetes API
- 🐳 모든 컨테이너 지원
- 📚 풍부한 생태계

**단점**:
- 🧑‍💻 Kubernetes 학습 곡선
- 🔧 직접 운영 필요
- 📊 클라우드 통합 별도 구현
- ⚠️ IoT 최적화 부족

**적합한 경우**:
- 멀티 클라우드 전략
- Kubernetes 팀 역량
- 예산 최소화
- 완전한 제어 필요

**검증 사례**: 엣지 AI 플랫폼, 스마트 시티 게이트웨이

---

#### Edge Computing 비교표

| 항목 | AWS Greengrass | Azure IoT Edge | K3s |
|------|----------------|----------------|-----|
| **레이턴시** | 밀리초 | 밀리초 | 밀리초 |
| **AI 추론** | 제한적 | ✅ Azure ML | ✅ 모든 프레임워크 |
| **오프라인** | ✅ | ✅ | ✅ |
| **비용** | AWS 연동 | Azure 연동 | 무료 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️ 중간 | ⚙️⚙️⚙️ 높음 |

**의사결정 가이드**:
```
AWS 중심? → AWS IoT Greengrass
  └─ NO
     ↓
AI 추론 필요? → Azure IoT Edge
  └─ NO
     ↓
멀티 클라우드? → K3s
  └─ NO → AWS IoT Greengrass
```

---

## Part 2.5: 핵심 DNA 시스템 기술 선택 ⭐⭐⭐

이 패밀리에서 특별히 중요한 DNA 시스템(⭐⭐⭐)에 대한 기술 선택입니다.

### 2.5.1 Type System (DNA #4) - 안전 인증 타입 시스템 ⭐⭐⭐

**패밀리 요구**:
- 런타임 에러 0 목표 (컴파일 타임 검증)
- SIL 2+ 인증 지원
- 메모리 안전성 보장
- 정적 분석 통합
- Null pointer, buffer overflow 완전 방지

---

#### 옵션 1: Rust + RTIC

**핵심 스펙**:
- **메모리 안전성**: 컴파일 타임 보장 (borrow checker)
- **실시간 지원**: RTIC 프레임워크 (Zero-cost abstractions)
- **타겟**: Cortex-M, RISC-V 임베디드
- **인증**: ISO 26262 (자동차), IEC 61508 진행 중

**비용**: 오픈소스 (무료), 도구체인 무료

**장점**:
- 🔧 메모리 안전성 컴파일 타임 보장
- 🔧 Zero-cost abstractions (C 수준 성능)
- 🔧 우선순위 기반 리소스 공유 (RTIC)
- 🔧 활발한 임베디드 생태계 (Embassy, probe-rs)

**단점**:
- ⚠️ SIL 인증 아직 진행 중 (완료 아님)
- ⚠️ 학습 곡선 (borrow checker)
- ⚠️ 레거시 C 코드와 통합 복잡
- ⚠️ 일부 MCU 지원 제한

**적합한 경우**:
- 신규 프로젝트 (레거시 없음)
- SIL 2 미만 또는 인증 불필요
- 팀이 Rust 경험 있음
- 메모리 안전성 최우선

**검증 사례**: Volvo (자동차), Oxide Computer, Arm Pelion

---

#### 옵션 2: Ada/SPARK

**핵심 스펙**:
- **정적 검증**: SPARK 프로버 (수학적 증명)
- **인증**: DO-178C (항공), EN 50128 (철도), IEC 61508 인증 완료
- **타겟**: 모든 주요 MCU, x86, ARM
- **역사**: 40년+ 안전-임계 시스템 검증

**비용**: GNAT Community (무료), GNAT Pro ($10K~$50K/년)

**장점**:
- 🔧 SIL 4까지 인증 완료
- 🔧 DO-178C Level A 인증 (항공)
- 🔧 수학적 증명 가능 (SPARK)
- 🔧 40년 검증된 안전 기록

**단점**:
- ⚠️ 개발자 풀 제한적
- ⚠️ GNAT Pro 고비용 ($10K+/년)
- ⚠️ 현대 라이브러리 생태계 부족
- ⚠️ 학습 자료 제한적

**적합한 경우**:
- SIL 3/4 필수 (항공, 철도, 원자력)
- DO-178C 인증 필수
- 장기 유지보수 (20년+)
- 예산 충분

**검증 사례**: Boeing 787, Airbus A380, 프랑스 TGV

---

#### 옵션 3: C + MISRA + 정적 분석

**핵심 스펙**:
- **표준**: MISRA C:2012 (자동차/산업 표준)
- **인증**: IEC 61508, ISO 26262 광범위 인증
- **도구**: Polyspace, PC-lint, Coverity, PVS-Studio
- **타겟**: 모든 MCU 지원

**비용**: 도구 $5K~$50K/년 (PC-lint $400, Polyspace $20K+)

**장점**:
- 🔧 가장 넓은 MCU 지원
- 🔧 개발자 풀 풍부
- 🔧 레거시 코드 활용 가능
- 🔧 기존 인증 사례 풍부

**단점**:
- ⚠️ 언어 자체 안전성 없음 (도구 의존)
- ⚠️ 정적 분석으로 모든 버그 못 잡음
- ⚠️ MISRA 준수 수동 검토 필요
- ⚠️ 메모리 오류 런타임에 발생 가능

**적합한 경우**:
- 레거시 C 코드 유지보수
- 기존 팀 C 전문성
- 검증된 도구체인 필수
- MCU 지원 범위 우선

**검증 사례**: 자동차 ECU 대부분, 산업 PLC, 의료기기

---

**Type System 의사결정 플로우차트**:
```
SIL 3/4 또는 DO-178C 필수? → Ada/SPARK
  └─ NO
     ↓
신규 프로젝트 + 메모리 안전성 우선? → Rust + RTIC
  └─ NO
     ↓
레거시 C + 넓은 MCU 지원? → C + MISRA
```

---

### 2.5.2 Error Handling (DNA #5) - Fail-Safe 전략 ⭐⭐⭐

**패밀리 요구**:
- 모든 에러 → 안전 모드 전환
- Watchdog 타이머 필수
- 센서 융합 에러 처리
- 복구 불가 시 안전한 셧다운
- 에러 전파 차단

---

#### 옵션 1: Rust Result + Custom Error Types

**핵심 스펙**:
- **에러 모델**: Result<T, E> (강제 처리)
- **전파**: `?` 연산자 (명시적)
- **패닉 처리**: `#[panic_handler]` 커스텀
- **Watchdog**: HAL 통합 (cortex-m, stm32)

**비용**: 오픈소스 (무료)

**장점**:
- 🔧 컴파일 타임 에러 처리 강제
- 🔧 에러 무시 불가능
- 🔧 Zero-cost (런타임 오버헤드 없음)
- 🔧 패닉 → 안전 모드 자동 전환 가능

**단점**:
- ⚠️ 학습 곡선 (Result, Option)
- ⚠️ 기존 C 라이브러리 래핑 필요
- ⚠️ 에러 타입 설계 복잡
- ⚠️ 일부 HAL 미성숙

**적합한 경우**:
- Rust 기반 신규 프로젝트
- 컴파일 타임 안전성 우선
- 팀이 함수형 프로그래밍 경험
- 에러 처리 누락 방지 필수

---

#### 옵션 2: C + Defensive Programming + Watchdog

**핵심 스펙**:
- **패턴**: MISRA C 에러 처리 규칙
- **Watchdog**: 하드웨어 WDT + 소프트웨어 타이머
- **방어**: 어설션, 범위 체크, 센서 크로스 체크
- **복구**: 상태 머신 기반 복구 로직

**비용**: 도구 $1K~$20K/년 (정적 분석 포함)

**장점**:
- 🔧 검증된 패턴 풍부
- 🔧 하드웨어 Watchdog 직접 제어
- 🔧 레거시 코드와 호환
- 🔧 MISRA 준수 도구 지원

**단점**:
- ⚠️ 에러 처리 누락 가능 (컴파일러 미강제)
- ⚠️ 수동 방어 코딩 필요
- ⚠️ 정적 분석 의존
- ⚠️ 런타임 에러 가능

**적합한 경우**:
- 레거시 C 코드베이스
- 검증된 Watchdog 패턴 필요
- MISRA 준수 필수
- 팀 C 전문성

---

#### 옵션 3: Ada Exception + SPARK 계약

**핵심 스펙**:
- **에러 모델**: Ada Exception (구조화된 예외)
- **계약**: SPARK Pre/Post conditions (정적 증명)
- **검증**: 런타임 체크 + 정적 증명 조합
- **복구**: Exception handler 체계

**비용**: GNAT Community (무료), GNAT Pro ($10K+/년)

**장점**:
- 🔧 수학적 에러 부재 증명 (SPARK)
- 🔧 구조화된 예외 처리
- 🔧 Pre/Post condition 강제
- 🔧 런타임 + 정적 검증 조합

**단점**:
- ⚠️ SPARK 증명 복잡
- ⚠️ 예외 오버헤드 (SPARK 미사용 시)
- ⚠️ 개발자 풀 제한적
- ⚠️ 도구 비용

**적합한 경우**:
- SIL 3/4 프로젝트
- 수학적 증명 필수
- Ada 팀 구성 가능
- 장기 유지보수

---

**Error Handling 의사결정 플로우차트**:
```
수학적 에러 부재 증명 필수? → Ada Exception + SPARK
  └─ NO
     ↓
컴파일 타임 에러 처리 강제? → Rust Result
  └─ NO
     ↓
레거시 C + Watchdog? → C Defensive Programming
```

---

### 2.5.3 Resilience (DNA #10) - 생명 안전 중복성 ⭐⭐⭐

**패밀리 요구**:
- N+1 센서/액추에이터 중복
- 5-250ms 페일오버
- 센서 크로스 체크 (Voting)
- 자동 복구 (Self-healing)
- Health Check + 격리

---

#### 옵션 1: 하드웨어 중복 + Voting

**핵심 스펙**:
- **패턴**: Triple Modular Redundancy (TMR)
- **Voting**: 2-out-of-3, 다수결
- **페일오버**: 하드웨어 스위칭 (<1ms)
- **격리**: 물리적 분리 (별도 전원, 별도 회로)

**비용**: 하드웨어 3배 + 설계 $50K~$500K

**장점**:
- 🔧 하드웨어 레벨 안전성
- 🔧 1ms 미만 페일오버
- 🔧 Byzantine Fault Tolerance
- 🔧 SIL 4 달성 가능

**단점**:
- ⚠️ 하드웨어 비용 3배+
- ⚠️ 설계 복잡도 높음
- ⚠️ 전력 소비 증가
- ⚠️ 물리적 공간 필요

**적합한 경우**:
- SIL 3/4 필수
- 예산 충분
- 물리적 공간 여유
- 하드웨어 팀 존재

**검증 사례**: 항공기 비행 제어, 원자력 발전소

---

#### 옵션 2: 소프트웨어 Failover + Circuit Breaker

**핵심 스펙**:
- **패턴**: Primary-Standby, Active-Active
- **Circuit Breaker**: failsafe-rs, 지수 백오프
- **Health Check**: 주기적 Heartbeat
- **페일오버**: 5-50ms (소프트웨어)

**비용**: 추가 하드웨어 $500~$5K + 개발

**장점**:
- 🔧 비용 효율적
- 🔧 유연한 복구 전략
- 🔧 소프트웨어 업데이트 가능
- 🔧 Circuit Breaker로 장애 전파 차단

**단점**:
- ⚠️ 하드웨어 TMR보다 느림 (5-50ms)
- ⚠️ 소프트웨어 버그 가능
- ⚠️ SIL 4 달성 어려움
- ⚠️ 복잡한 상태 관리

**적합한 경우**:
- SIL 2 이하
- 예산 제한
- 소프트웨어 팀 강점
- 유연한 복구 필요

**검증 사례**: 산업 자동화, 스마트 팩토리

---

#### 옵션 3: 클라우드 기반 Redundancy

**핵심 스펙**:
- **패턴**: Edge + Cloud 이중화
- **동기화**: 상태 복제 (MQTT, Kafka)
- **페일오버**: 100-500ms (네트워크 의존)
- **관리**: AWS IoT Greengrass, Azure IoT Edge

**비용**: 클라우드 $100~$1K/월 + Edge 하드웨어

**장점**:
- 🔧 원격 모니터링/관리
- 🔧 자동 스케일링
- 🔧 글로벌 분산
- 🔧 OTA 업데이트

**단점**:
- ⚠️ 네트워크 의존 (오프라인 시 제한)
- ⚠️ 페일오버 느림 (100-500ms)
- ⚠️ 데이터 주권 이슈
- ⚠️ SIL 인증 어려움

**적합한 경우**:
- 비-임계 모니터링
- 원격 관리 필수
- 네트워크 안정적
- SIL 인증 불필요

**검증 사례**: 스마트 빌딩, 원격 자산 모니터링

---

**Resilience 의사결정 플로우차트**:
```
SIL 3/4 + 1ms 미만 페일오버? → 하드웨어 TMR
  └─ NO
     ↓
Edge 로컬 처리 + 유연한 복구? → 소프트웨어 Failover
  └─ NO
     ↓
원격 관리 + 비-임계? → 클라우드 Redundancy
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 센서 하드웨어

**선택지**:
- **Raspberry Pi 4**: 범용, Linux, Python/C++
- **Arduino**: 저전력, 실시간, C/C++
- **ESP32**: WiFi/BLE, 초저전력, MicroPython
- **산업용 PLC**: Siemens, Allen-Bradley (규제 인증)

**선택 기준**:
- 처리 능력: 복잡한 센서 융합 → Raspberry Pi
- 저전력: 배터리 → Arduino, ESP32
- 산업 표준: 규제 준수 → PLC

**A-B-A 영향**: **큼** - 실시간 처리(A) + 센서 융합(B) 요구  
(Edge Computing 성능 결정)

---

### 3.2 통신 프로토콜

**선택지**:
- **WiFi**: 고대역폭, 짧은 거리, 실내
- **4G/5G**: 이동성, 넓은 범위, 고비용
- **LoRaWAN**: 초저전력, 장거리 (수 km), 저속 (50kbps)
- **Zigbee**: 저전력, 메쉬 네트워크, 짧은 거리

**선택 기준**:
- 레이턴시: 밀리초(A) → WiFi, 4G/5G
- 저전력: 배터리 수명 → LoRaWAN, Zigbee
- 이동성: 차량, 드론 → 4G/5G
- 범위: 공장/건물 → WiFi, Zigbee

**A-B-A 영향**: **매우 큼** - 밀리초(A) 달성 가능 여부  
(WiFi: 5-50ms, 4G: 50-100ms, LoRaWAN: 1-5초)

---

### 3.3 대시보드/시각화

**선택지**:
- **Grafana**: 오픈소스, 시계열, Prometheus 통합
- **Kibana**: Elasticsearch, 로그 중심
- **Power BI**: 엔터프라이즈, Microsoft 생태계
- **Custom Web**: React, D3.js (맞춤형)

**선택 기준**:
- 실시간 모니터링: Grafana (초 단위 갱신)
- 로그 분석: Kibana (ELK Stack)
- 비즈니스 리포트: Power BI (주간/월간)
- 특수 요구사항: Custom Web

**A-B-A 영향**: 최소 (패밀리 무관, 사용자 선호도)

---

### 3.4 클라우드 vs 온프레미스

**선택지**:
- **클라우드**: AWS IoT, Azure IoT (확장성, 관리 편의)
- **하이브리드**: Edge + 클라우드 (로컬 처리 + 중앙 집계)
- **온프레미스**: 완전 자체 호스팅 (데이터 주권, 규제)

**선택 기준**:
- 밀리초 응답(A): 하이브리드 또는 온프레미스 (네트워크 지연 회피)
- 규제: 데이터 주권, SIL 인증 → 온프레미스
- 확장성: 수십만 센서 → 클라우드

**A-B-A 영향**: **큼** - 치명적 실패(A) + 밀리초(A) 요구  
(클라우드 왕복 100-500ms → 로컬 처리 필수)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 제조 공장 안전 시스템

**Layer 3 제약 발견**:
- 규제: SIL 2 인증 필수 (IEC 61508)
- 네트워크: 공장 WiFi 불안정 (패킷 손실 5%)
- 예산: $100K/년 (전체)
- 기존 시스템: Siemens PLC (Profinet)

**기술 선택 영향**:
```
IoT 메시징:
- EMQX (선호) → RabbitMQ
- 이유: 예산 제약, Profinet 연동

시계열 DB:
- InfluxDB (선호) → TimescaleDB
- 이유: SQL 필수 (규제 보고), 예산

Edge Computing:
- AWS Greengrass (불가능) → K3s
- 이유: 공장 내 온프레미스, 오프라인
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 밀리초 응답 A + WiFi 불안정
- **NFR**: 450ms 미만 경보 응답
- **제약**: 공장 WiFi 불안정 (패킷 손실 5%)
- **해결**: Edge Computing 필수 (로컬 처리) + 유선 백업
- **트레이드오프**:
  - ✅ 로컬 처리로 50ms 응답 달성 (WiFi 독립)
  - ✅ 네트워크 장애 시에도 작동
  - ⚠️ Edge 디바이스 비용 증가 ($200~$500/센서)
  - ⚠️ 유선 백업 설치 비용 ($50~$100/센서)
  - ⚠️ 유지보수 복잡도 증가 (센서별 업데이트)

---

**충돌 2**: 치명적 실패 A + 예산 제약
- **NFR**: SIL 2 인증 필수 (안전 규제)
- **제약**: 예산 $100K/년 (EMQX Enterprise, InfluxDB Enterprise 불가)
- **해결**: 오픈소스 스택 (RabbitMQ + TimescaleDB + K3s) + 외부 인증 비용
- **트레이드오프**:
  - ⚠️ 확장성 제한 (수만 센서까지, 수백만 불가)
  - ⚠️ 고가용성 구성 복잡 (직접 클러스터링)
  - ✅ 소프트웨어 비용 $50K/년 → $10K/년 (80% 절감)
  - ✅ SIL 2 인증 $30K (외부 인증 기관)
  - ✅ 총 예산 $40K/년 (목표 $100K 내)

---

**충돌 3**: 센서 융합 B + 레거시 PLC
- **NFR**: JSON 센서 데이터 (온도, 습도, 진동 융합)
- **제약**: Siemens PLC (Profinet 바이너리 프로토콜)
- **해결**: Edge Gateway 변환 (Profinet → MQTT/JSON)
- **트레이드오프**:
  - ⚠️ 레이턴시 추가 10-50ms (변환 오버헤드)
  - ⚠️ Gateway 단일 장애 지점 (SPOF)
  - ⚠️ Gateway 비용 $2,000~$5,000
  - ✅ 레거시 PLC 활용 (교체 불필요)
  - ✅ 표준 MQTT 인프라 구축
  - ✅ 향후 센서 추가 용이

**추가 해결**: Gateway 이중화 (Active-Standby)  
**추가 비용**: $3,000~$6,000 (Gateway 2대)

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ IoT 메시징: RabbitMQ (MQTT 플러그인)
✅ 시계열 DB: TimescaleDB
✅ Edge Computing: K3s (온프레미스)

도메인 선택:
✅ 센서: Raspberry Pi 4 + DHT22 + MCP3008
✅ 통신: WiFi (주) + 유선 Ethernet (백업)
✅ 대시보드: Grafana + Prometheus
```

**ADR 작성 대상**:
1. IoT 메시징 선택 (EMQX vs RabbitMQ)
2. 시계열 DB 선택 (InfluxDB vs TimescaleDB)
3. Edge Computing 전략 (Greengrass vs K3s)
4. 네트워크 이중화 방안 (WiFi + 유선)
5. SIL 2 인증 경로

---

## 📚 참고 자료

### IoT 메시징 벤치마크
- [EMQX Performance](https://www.emqx.com/en/products/emqx/performance)
- [AWS IoT Core Limits](https://docs.aws.amazon.com/general/latest/gr/iot-core.html)

### 시계열 DB 벤치마크
- [InfluxDB Performance](https://www.influxdata.com/influxdb-performance/)
- [TimescaleDB Benchmark](https://docs.timescale.com/timescaledb/latest/overview/how-it-works/)

### Edge Computing
- [AWS IoT Greengrass](https://aws.amazon.com/greengrass/)
- [Azure IoT Edge](https://azure.microsoft.com/en-us/products/iot-edge/)
- [K3s](https://k3s.io/)

### 산업 표준
- [IEC 61508: SIL](https://en.wikipedia.org/wiki/IEC_61508)
- [ISA-95: 제조 표준](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95)

### 검증 사례
- [IoT 긴급 경보 시스템](https://www.fcc.gov/emergency-alert-system-eas)
- [SCADA 시스템](https://en.wikipedia.org/wiki/SCADA)

---

**마지막 업데이트**: 2025-11-12  
**다음 검토**: 2026-02-12 (기술 스택 업데이트 반영)
