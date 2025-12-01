# DNA Methodology v4.0

> **D**esign **N**avigation **A**rchitecture - AI 컨텍스트 한계를 극복하는 소프트웨어 설계 방법론

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/Jaesun23/dna-methodology)

---

## 📖 개요

DNA Methodology는 **AI와 협업할 때 발생하는 컨텍스트 한계를 극복**하기 위해 설계된 9-Stage 소프트웨어 설계 시스템입니다.

### 🎯 핵심 문제

AI 협업의 가장 큰 문제:
- **컨텍스트 부패 (Context Rot)**: 대화가 길어질수록 초기 결정사항 희석
- **정보 과부하**: 많은 정보 ≠ 좋은 결과
- **일관성 부재**: 단계마다 즉흥적 해결, 표준 없음

### 💡 DNA의 해결책

**3단계 전략**:

1. **단계적 정의**: Stage 1-6으로 환경 구축 → Stage 7-9로 실행
2. **환경 강제**: Standards + DNA Systems + 자동화로 일관성 보장
3. **레고블럭 전략**: 독립 실행 가능한 작업 단위로 분할

---

## 🏗️ 9-Stage 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│                     DNA Methodology v4.0                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: 핵심 정의 (패밀리 분류)                             │
│  Stage 2: 환경 제약 (Layer 3 조사)                           │
│  Stage 3: ADR (아키텍처 결정 기록)                            │
│  Stage 4: DNA 시스템 계획 (11개 공용 모듈)                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Stage 5: DNA 시스템 구현                                    │
│  Stage 6: 프로젝트 표준                                      │
│  Stage 7: 청사진 작성                                        │
│  Stage 8: 작업 분해                                          │
│  Stage 9: 거버넌스 & 자동화                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 단계별 설명

| Stage | 목표 | 산출물 |
|-------|------|--------|
| **1. 핵심 정의** | 18개 패밀리 중 선택 + NFR 우선순위 | 패밀리 코드 (A-C-A 등) |
| **2. 환경 제약** | 기술/팀/인프라 제약 조사 | 제약 목록, 충돌 패턴 |
| **3. ADR** | 아키텍처 결정 문서화 | Bootstrap ADR 10-20개 |
| **4. DNA 계획** | 11개 공용 모듈 설계 | DNA 시스템 스펙 |
| **5. DNA 구현** | 공용 모듈 구현 | 실제 코드 |
| **6. 표준** | ADR → DO/DON'T 변환 | PROJECT_STANDARDS.md |
| **7. 청사진** | 완전한 설계서 | BLUEPRINT.md |
| **8. 작업 분해** | 독립 작업 단위 | TASK_BREAKDOWN.md |
| **9. 거버넌스** | 체크리스트 + 자동화 | Pre-commit hooks, CI/CD |

---

## 🚀 빠른 시작

### 전제조건

DNA Methodology는 **SPARK Agent System**에 의존합니다.

```bash
# 1. SPARK 플러그인 설치 (필수!)
/plugin install https://github.com/Jaesun23/spark-claude

# 2. DNA 플러그인 설치
cd dna-methodology
/plugin install .
```

### 사용법

```bash
# 프로젝트 초기화
/dna:init "주식 거래 플랫폼"

# Stage 1: 패밀리 분류
/dna:stage1

# Stage 2: 환경 제약 조사
/dna:stage2

# Stage 3: ADR 작성
/dna:stage3

# ... Stage 4-9 계속 진행
```

---

## 📚 핵심 개념

### 18개 아키텍처 패밀리

시스템을 **3-Layer 결정 트리**로 분류:
- **Layer 1**: 실패 영향 (A: 치명적, B: 심각, C: 경미)
- **Layer 2**: 데이터 속성 (A: 구조화, B: 반구조화, C: 비구조화)
- **Layer 3**: 응답 시간 (A: 밀리초, B: 초, C: 분/시간)

예시:
- **A-A-A**: 금융 거래 시스템 (치명적 + 구조화 + 밀리초)
- **C-B-B**: 블로그 플랫폼 (경미 + 반구조화 + 초)
- **A-C-A**: 실시간 트랜잭션 (치명적 + 비구조화 + 밀리초) - **새 발견!**

### DNA 11 시스템

모든 프로젝트에서 재사용 가능한 공용 모듈:
1. Logging (structlog)
2. Configuration (Pydantic)
3. Database (SQLAlchemy)
4. Cache (Redis)
5. Messaging (RabbitMQ)
6. Types (강타입 시스템)
7. Testing (pytest)
8. Monitoring (Prometheus)
9. Security (인증/인가)
10. Error Handling
11. API Gateway

### Context Rot 방지 3중 방어

1. **JSON State**: 각 Stage 결과를 구조화된 파일로 저장
2. **Context Re-ranking**: 다음 Stage에서 관련 컨텍스트만 로드
3. **Validation**: 각 Stage 완료 시 자동 검증

---

## 🛠️ 기술 스택

### DNA Plugin 구성

- **Agents**: Stage 1-4 전용 에이전트 (신규 작성)
- **Commands**: `/dna:stage1` ~ `/dna:stage9` (13개)
- **Skills**: 방법론 지식, 템플릿, Validator

### DNA Agents (9개 전체)

**Stage 1-4** (신규 에이전트):
- `classifier-dna` - 패밀리 분류
- `investigator-dna` - 환경 제약 조사
- `decision-maker-dna` - ADR 작성
- `planner-dna` - DNA 시스템 계획

**Stage 5-9** (복사 후 이름 변경):
- `implementer-dna` (from `implementer-spark`)
- `documenter-dna` (from `documenter-spark`)
- `designer-dna` (from `designer-spark`)
- `analyzer-dna` (from `analyzer-spark`)
- `qc-dna` (from `qc-spark`)

자세한 매핑: [SPARK Agent 매핑 가이드](docs/integration/spark-agent-mapping.md)

---

## 📖 문서

### 사용자 가이드

- [00. 핵심 방법론](docs/guides/00_CORE_METHODOLOGY.md) - DNA v4.0 개요
- [Stage 1-9 가이드](docs/guides/) - 각 Stage별 상세 가이드

### 개발자 가이드

- [Plugin 구조](docs/plugin-guide/plugin-structure-guide.md) - Claude Code Plugin 제작
- [에이전트 정의](docs/plugin-guide/agent-definition-structure.md) - 7-Section 구조
- [Stage 실행 가이드](docs/plugin-guide/stage-execution-guide.md) - Stage별 목표/기술/참고문서

### 통합 가이드

- [SPARK Agent 매핑](docs/integration/spark-agent-mapping.md) - DNA ↔ SPARK 연동

---

## 🎯 사용 사례

### Case 1: 주식 거래 플랫폼 (A-C-A)

**발견**: 새로운 아키텍처 패밀리 A-C-A 패턴!
- Layer 1: 치명적 (금전 손실)
- Layer 2: 비구조화 (실시간 스트림)
- Layer 3: 밀리초 (거래 타이밍)

**결과**: 하이브리드 아키텍처 (Lambda + Kappa)

자세히: [02E-01 Stock Trading Case](docs/guides/02E-01_stock_trading_case.md)

### Case 2: Kent Beck의 BPlusTree3 (리팩토링)

**상황**: 기존 코드 개선 프로젝트
**접근**: Stage 1-3만 사용, Stage 4-9 생략

자세히: [03E-02 Kent Beck Case](docs/guides/03E-02_kent_beck_bplustree_case.md)

---

## 🤝 기여

### 개발 로드맵

- [ ] Stage 1-4 에이전트 구현
- [ ] Stage 1-9 Commands 작성
- [ ] Validator 스크립트 구현
- [ ] 통합 테스트
- [ ] 예시 프로젝트 추가

### 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 🙏 감사의 말

### 영감을 준 프로젝트

- **SPARK Agent System**: https://github.com/Jaesun23/spark-claude
- **SEI Architecture Decision**: Software Engineering Institute
- **Gemini AI Research**: 4-Phase 프로세스 (CoD, ToT, SoT)

### 연구 기반

- Jason의 2년간 AI 협업 경험
- 7개 프로젝트 실패 분석
- Context Rot 극복 방법론

---

## 📞 연락처

- **Author**: Jason (Jaesun23)
- **GitHub**: https://github.com/Jaesun23
- **Issues**: https://github.com/Jaesun23/dna-methodology/issues

---

**"한계극복!!! 그 방법은 '환경'을 만드는 것!"** - Jason
