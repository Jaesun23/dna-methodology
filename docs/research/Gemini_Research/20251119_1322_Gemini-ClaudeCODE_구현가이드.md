

# **Claude CODE의 핵심 기능(Subagents, Slash Commands, Hooks)을 활용한 DNA 방법론 v4.0 구현: 심층 기술 아키텍처 및 구현 청사진**

## **요약 (Executive Summary)**

현대 소프트웨어 엔지니어링은 대규모 언어 모델(LLM)의 도입으로 급격한 변화를 겪고 있다. 그러나 LLM의 확률적(Probabilistic) 특성은 소프트웨어 아키텍처가 요구하는 결정론적(Deterministic) 엄격함과 자주 충돌한다. 이러한 문제를 해결하기 위해 제안된 **DNA Development Methodology v4.0**은 3계층 의사결정 트리(3-Layer Decision Tree)와 7가지 아키텍처 패밀리 분류를 통해 시스템의 본질을 정의하고, 이를 강제하는 '환경의 힘(Environment Force)'을 강조한다.1 한편, Anthropic의 **Claude CODE**는 이러한 방법론을 실행에 옮길 수 있는 강력한 CLI(Command Line Interface) 기반의 에이전트 런타임을 제공하며, 특히 서브에이전트(Subagents), 훅(Hooks), 슬래시 커맨드(Slash Commands)와 같은 기능은 방법론의 이론적 제약을 실제 코드 레벨에서 강제할 수 있는 수단을 제공한다.2

본 보고서는 DNA v4.0 방법론을 Claude CODE 환경에서 완벽하게 구현하기 위한 기술적 아키텍처를 상세히 기술한다. 단순한 프롬프트 엔지니어링을 넘어, YAML 구성을 통한 에이전트 페르소나 정의, Python 스크립트를 이용한 결정론적 훅 구현, 그리고 동적 컨텍스트 주입(Dynamic Context Injection)을 통한 'Context Rot(문맥 부패)' 방지 메커니즘을 포괄적으로 다룬다. 특히 DNA 방법론의 핵심인 '단계적 정의', '환경 강제', '레고블럭 전략'을 Claude CODE의 기술적 프리미티브(Primitive)와 매핑하여, 실제로 작동 가능한 엔지니어링 파이프라인을 제시하는 것을 목적으로 한다.

---

## **1\. 서론: 방법론과 실행 환경의 융합**

소프트웨어 개발에서 '무엇을 만들 것인가'에 대한 정의와 '어떻게 만들 것인가'에 대한 실행은 종종 괴리된다. Jason과 Claude(2호)가 제안한 DNA v4.0은 이 간극을 메우기 위해 고안되었으며, 특히 트랜스포머 모델의 컨텍스트 한계로 인해 발생하는 'Context Rot' 문제를 해결하는 데 중점을 둔다.1 이 방법론은 시스템을 18가지(실증적으로는 7가지 핵심) 패밀리로 분류하고, 각 패밀리에 맞는 NFR(Non-Functional Requirements)을 프로파일링하여 아키텍처를 결정한다.1

Claude CODE는 이러한 방법론적 엄격함을 수용할 수 있는 최적의 실행 환경이다. Claude CODE는 단순한 채팅 인터페이스가 아니라, 로컬 파일 시스템에 접근하고, 터미널 명령어를 실행하며, 사용자가 정의한 워크플로우를 따르는 '에이전트 툴킷'이다.5 본 보고서에서는 DNA v4.0의 이론적 구조를 Claude CODE의 기능적 구조로 변환하는 과정을 다층적으로 분석한다.

### **1.1 DNA v4.0의 핵심 요구사항 분석**

DNA v4.0의 성공적인 구현을 위해서는 다음 세 가지 핵심 요소가 기술적으로 보장되어야 한다.

1. **단계적 정의의 강제 (Step-by-Step Definition Enforcement):** 아이디어 정제(Phase 1)에서 아키텍처 스켈레톤(Phase 2), 환경 구축(Phase 3), 레고블럭 실행(Phase 4)으로 이어지는 프로세스가 순차적으로, 그리고 불가역적으로 진행되어야 한다. 이는 Claude CODE의 **Slash Command** 체이닝을 통해 구현된다.1  
2. **환경에 의한 통제 (Environment Force):** AI 에이전트가 아키텍처 원칙(예: "A-A-A 패밀리에서는 블로킹 I/O를 사용할 수 없다")을 위반하려 할 때, 이를 시스템 레벨에서 차단해야 한다. 이는 Claude CODE의 **Hooks** 시스템을 통해 결정론적으로 구현된다.3  
3. **전문가적 페르소나와 워크플로우 (Professional Persona & Workflow):** 각 단계마다 필요한 역량이 다르다(예: 창의적 발상 vs 엄격한 검증). 이는 **Subagents** 구성을 통해 각기 다른 'Traits(특성)'와 'Behavior Protocol(행동 수칙)'을 가진 에이전트를 호출함으로써 달성된다.1

---

## **2\. 에이전트 레이어 (The Agent Layer): 특성과 행동의 코드화**

DNA 방법론에서 에이전트는 단순한 LLM 인스턴스가 아니라, 특정 역할(Role), 특성(Traits), 그리고 행동 프로토콜(Behavior Protocol)의 집합체로 정의된다. Claude CODE의 서브에이전트(Subagent) 기능은 이러한 정의를 .claude/agents/ 디렉토리 내의 마크다운 파일과 YAML 프론트매터(Frontmatter)를 통해 기술적으로 구현할 수 있게 해준다.4

### **2.1 서브에이전트 구성 아키텍처**

Claude CODE의 서브에이전트는 \~/.claude/agents/(사용자 전역) 또는 .claude/agents/(프로젝트 전용)에 저장되며, 파일명은 에이전트의 호출 ID가 된다. DNA 방법론의 각 단계별 에이전트를 구현하기 위해 다음과 같은 필드들이 YAML 프론트매터에 필수적으로 포함되어야 한다.4

* **name:** 에이전트의 고유 식별자 (예: system-classifier-spark). 소문자와 하이픈만 사용 가능하다.  
* **description:** 에이전트의 목적에 대한 자연어 설명. 메인 에이전트가 작업을 위임할 때 이 설명을 참조하여 라우팅을 결정하므로, 에이전트의 전문성을 명확히 기술해야 한다.  
* **model:** 해당 작업에 최적화된 모델 (예: sonnet, opus, haiku). 복잡한 추론이 필요한 아키텍처 결정에는 sonnet 이상이 권장된다.  
* **tools:** 에이전트가 사용할 수 있는 도구 목록. DNA의 검증 단계에서는 시스템 변경을 막기 위해 Write나 Bash 툴을 제한하고 Read와 Ask만 허용하는 식의 권한 분리가 필요하다.4

### **2.2 Phase 1: 시스템 분류자 에이전트 (System Classifier Agent) 구현**

이 에이전트는 사용자의 추상적인 아이디어를 DNA의 3-Layer Decision Tree에 따라 7가지 패밀리 중 하나로 분류하는 역할을 수행한다.

**기술 아티팩트: .claude/agents/system-classifier.md**

---

## **name: system-classifier-spark description: DNA Phase 1 전용 에이전트. 사용자의 아이디어를 분석하여 18가지 이론적 조합 중 검증된 7가지 아키텍처 패밀리로 분류하고, NFR 프로파일을 도출함. model: claude-3-5-sonnet-20241022 tools: Read, Write, Ask, WebSearch, mcp\_\_sequential-thinking\_\_sequentialthinking**

# **정체성 및 핵심 지령 (Identity & Core Directive)**

당신은 **System Classifier Spark**이며, DNA v4.0 방법론에 통달한 엘리트 솔루션 아키텍트입니다. 당신의 유일한 존재 목적은 소프트웨어 시스템을 '실패 파급력', '데이터 형태', '응답 시점'이라는 3가지 차원을 통해 분류하고, 가장 적합한 아키텍처 패밀리를 확정하는 것입니다.

## **핵심 특성 (Traits)**

1

1. **패턴 매칭 (Pattern Matching):** 사용자의 모호한 설명 속에서 "실시간 스트리밍(B-C-A)"이나 "트랜잭션/CRUD(A-A-B)"와 같은 아키텍처 패턴을 즉각적으로 식별합니다.  
2. **증거 기반 (Evidence-Based):** 추측하지 않습니다. "100ms 미만의 지연 시간이 요구되므로 Layer 3는 A(Real-time)입니다"와 같이 구체적인 제약 조건을 근거로 제시합니다.  
3. **체계적 탐구 (Systematic Inquiry):** 요구사항이 모호하면 진행을 거부합니다. 3-Layer의 각 차원이 명확해질 때까지 집요하게 질문합니다.  
4. **맥락적 이해 (Contextual Understanding):** 기술적 요구사항뿐만 아니라 비즈니스 목적을 파악하여 '핵심 기능'을 정의합니다.

## **행동 프로토콜: 밀도 사슬 (Chain of Density)**

1

당신은 다음의 반복적 프로세스(Iteration)를 엄격히 준수해야 합니다.

**Iteration 1: 스켈레톤 분석 (Skeleton Analysis)**

* 사용자의 원시 아이디어에서 '구현 세부사항'을 제거하고 가장 원자적인 '핵심 기능(Core Function)'을 추출합니다.  
* 예: "AI 챗봇이 달린 주식 앱" \-\> "주식 거래(핵심) \+ AI(부가)"

Iteration 2: 3-Layer 심문 (The 3-Layer Interrogation) 1

* **Layer 1 (실패 파급력):** "이 시스템이 5분간 멈추면 금전/생명 손실(A)입니까, 아니면 단순 불편(B)입니까?"  
* **Layer 2 (데이터 형태):** "스키마가 사전에 완벽히 정의됩니까(A), 일부만 정의됩니까(B), 아니면 비정형입니까(C)?"  
* **Layer 3 (응답 시점):** "결과가 밀리초 단위(A), 초 단위(B), 혹은 배치(C)로 필요합니까?"

**Iteration 3: 패밀리 수렴 (Family Convergence)**

* 답변을 조합하여 18가지 이론적 조합 중 하나를 도출합니다.  
* 도출된 코드를 **7가지 실증 패밀리**와 매핑합니다 (예: A-A-A는 초고속 거래, B-C-A는 실시간 스트리밍).  
* **중요:** 만약 A-C-A (치명적/비구조화/실시간) 패턴이 도출되면, 이는 "이론적으로 극도로 어려운" 조합임을 경고하고 구조적 변환(비구조화 데이터의 구조화 처리 등)을 제안해야 합니다.1

**Iteration 4: NFR 프로파일링**

* 결정된 패밀리에 따라 NFR(정확성, 속도, 보안, 비용)의 우선순위를 결정합니다 (예: A-A-B 패밀리 \-\> 정확성 \> 속도 \> 보안 \> 비용).

## **출력 형식 (Output Format)**

최종적으로 01C-01\_family\_classification.md 파일을 생성해야 하며, 다음 내용을 포함해야 합니다:

1. **패밀리 코드:** (예: A-A-B)  
2. **결정 근거:** Layer 1, 2, 3에 대한 답변과 증거.  
3. **핵심 기능:** 비즈니스 목적에 따른 원자적 기능 정의.  
4. **검증 체크리스트:** 다른 패밀리가 아닌 이유.

아키텍처 분석:  
이 서브에이전트는 mcp\_\_sequential-thinking\_\_sequentialthinking 도구를 사용하여 논리적 비약을 방지하고 단계별 추론을 강화하도록 구성되었다.1 프롬프트 내에 DNA 방법론의 이론적 배경(예: A-C-A 패턴의 난이도)을 직접 주입함으로써, 모델이 일반적인 상식이 아닌 방법론 특화 지식을 기반으로 판단하도록 강제했다. 이는 "Hallucination(환각)"을 줄이고 "전문가적 조언"의 품질을 높이는 핵심 기법이다.

### **2.3 Phase 2: 아키텍처 의사결정자 에이전트 (Architecture Decision Maker) 구현**

이 에이전트는 Phase 1의 결과를 바탕으로 구체적인 기술 스택(데이터베이스, 언어, 프레임워크 등)을 결정하는 ADR(Architecture Decision Records)을 작성한다.

**기술 아티팩트: .claude/agents/arch-decision-maker.md**

---

## **name: arch-decision-maker-spark description: DNA Phase 2 전용 에이전트. 확정된 패밀리 분류를 기반으로 Bootstrap ADR(기술 결정 문서)을 작성하며, Tree of Thoughts 기법을 사용하여 대안을 비교함. model: claude-3-5-sonnet-20241022 tools: Read, Write, WebSearch, Bash**

# **정체성 및 핵심 지령**

당신은 **Architecture Decision Maker**이며, DNA 프로세스의 Phase 2를 담당합니다. 당신의 임무는 추상적인 패밀리 분류를 구체적인 기술 결정(Bootstrap ADRs)으로 변환하는 것입니다.

## **핵심 특성 (Traits)**

1

1. **트레이드오프 추론 (Trade-off Reasoning):** "최고의 기술"은 없다고 믿습니다. 오직 현재 제약조건에 맞는 "최적의 트레이드오프"만 있을 뿐입니다. 장단점을 명시적으로 저울질합니다.  
2. **충돌 감지 (Conflict Detection):** NFR(비기능 요구사항)과 선택된 기술 간의 모순을 찾아냅니다 (예: "비용 최소화" NFR vs "Oracle DB" 선택).  
3. **증거 기반 비교 (Systematic Comparison):** 감이 아닌 스펙과 벤치마크 데이터를 통해 기술을 비교합니다.

## **행동 프로토콜: 생각의 나무 (Tree of Thoughts \- ToT)**

모든 기술 결정(DB, 언어, 메시징 큐 등)에 대해 다음 3단계 시뮬레이션을 수행해야 합니다.

**Step 1: 가지치기 (Branching \- 옵션 생성)**

* 해당 컴포넌트에 대해 최소 3가지의 실행 가능한 후보를 도출합니다 (예: DB \-\> PostgreSQL vs MySQL vs Aurora).  
* **필터링:** DNA 패밀리 특성에 맞지 않는 후보는 즉시 제거합니다 (예: A-A-A 패밀리에서 지연 시간이 긴 NoSQL 제거).

**Step 2: 확장 (Expansion \- 심층 분석)**

* 각 후보에 대해 다음을 분석합니다:  
  * **적합성:** NFR 프로파일을 만족하는가?  
  * **제약:** Layer 3 제약(비용, 인프라)을 위반하지 않는가?  
  * **생태계:** 팀의 기술 스택과 호환되는가?

**Step 3: 가지치기 및 선택 (Pruning & Selection)**

* "치명적(Critical)" NFR을 만족하지 못하는 옵션을 탈락시킵니다.  
* 가장 균형 잡힌 트레이드오프를 가진 기술을 선택합니다.

## **출력 형식**

docs/adr/ 디렉토리에 03A-{번호}\_{제목}.md 형식으로 파일을 생성합니다. 각 ADR은 다음 섹션을 반드시 포함해야 합니다 8:

* **\#\# Context:** 문제 상황과 제약 조건.  
* **\#\# Decision:** 선택된 기술.  
* **\#\# Alternatives:** 고려했으나 기각된 대안들과 그 이유 (ToT의 증거).  
* **\#\# Consequences:** 이 결정으로 인해 얻는 이득과 감수해야 할 부채.

구현 전략:  
이 에이전트 설정은 Claude CODE의 파일 시스템 접근 권한을 활용하여 docs/adr/ 경로에 직접 결과물을 저장하도록 유도한다. description 필드에 "Tree of Thoughts"를 명시함으로써, 메인 에이전트가 복잡한 비교 분석이 필요할 때 이 서브에이전트를 호출하도록 유도한다.6

---

## **3\. 거버넌스 레이어 (The Governance Layer): 결정론적 훅(Hooks)**

에이전트가 '생성'을 담당한다면, 거버넌스 레이어는 '제약'을 담당한다. DNA v4.0의 "환경 강제(Environment Force)" 개념은 에이전트나 개발자가 정해진 아키텍처 원칙을 위반하는 코드를 작성하거나 문서를 생성하려 할 때, 이를 사전에 차단하거나 경고하는 시스템이다. Claude CODE의 Hooks 시스템은 PreToolUse, PostToolUse 등의 이벤트를 통해 쉘 명령어를 실행하고, 그 결과(Exit Code, JSON 출력)에 따라 에이전트의 행동을 제어할 수 있다.3

### **3.1 컨텍스트 부패 방지 및 모순 탐지 훅 (Context Rot Prevention Hook)**

가장 치명적인 문제는 프로젝트 후반부에 초기의 결정(예: "우리는 초저지연 시스템을 만든다")이 망각되는 'Context Rot'이다.1 이를 방지하기 위해, 파일 쓰기(Write) 도구가 호출되기 직전에 실행되는 PreToolUse 훅을 구현하여, 작성하려는 내용이 프로젝트의 핵심 제약조건(Global Context)과 충돌하지 않는지 검사한다.

**기술 아티팩트 1: .claude/settings.json 설정**

JSON

{  
  "hooks": {  
    "PreToolUse":  
      }  
    \],  
    "PostToolUse":  
      }  
    \]  
  }  
}

**기술 아티팩트 2: .claude/hooks/validate\_consistency.py (검증 스크립트)**

이 Python 스크립트는 stdin으로 들어오는 에이전트의 도구 사용 요청(JSON)을 파싱하여, 작성하려는 파일의 내용(content)이 프로젝트의 context\_summary.json에 정의된 제약조건을 위반하는지 검사한다.11

Python

import sys  
import json  
import os  
import re

def main():  
    \# 1\. Claude Code로부터 입력 JSON 파싱 (stdin)  
    try:  
        input\_data \= json.load(sys.stdin)  
    except json.JSONDecodeError:  
        sys.exit(0) \# 입력이 없으면 통과

    tool\_input \= input\_data.get('tool\_input', {})  
    file\_path \= tool\_input.get('file\_path', '')  
    content \= tool\_input.get('content', '')

    \# 2\. 프로젝트 컨텍스트 로드 (The "Truth")  
    \# DNA 방법론에서는 핵심 결정사항이 이 JSON에 요약되어 저장된다.  
    context\_file \= '.claude/context\_summary.json'  
    if not os.path.exists(context\_file):  
        sys.exit(0) \# 컨텍스트가 아직 없으면 검증 패스

    with open(context\_file, 'r') as f:  
        context \= json.load(f)

    family \= context.get('core\_decisions', {}).get('family', '')  
    constraints \= context.get('core\_decisions', {}).get('critical\_constraints',)

    \# 3\. 로직: 아키텍처 위반 감지 (Family 기반)  
    \# 예: A-A-A (초고속 거래) 패밀리에서는 블로킹 HTTP 호출을 금지한다.  
    if family \== 'A-A-A':  
        if 'requests.get' in content or 'http.client' in content:  
            if 'src/core/engine' in file\_path: \# 핵심 엔진 코드인 경우  
                \# Claude에게 차단 결정과 이유를 JSON으로 반환  
                print(json.dumps({  
                    "decision": "block",  
                    "reason": (  
                        f"CRITICAL ARCHITECTURE VIOLATION: 시스템 패밀리가 {family} (Ultra-Low Latency)입니다. "  
                        "코어 엔진에서의 블로킹 HTTP 호출은 엄격히 금지됩니다. "  
                        "ADR-003에 정의된 비동기 네트워킹 또는 메시지 큐를 사용하십시오."  
                    )  
                }))  
                sys.exit(0) \# 스크립트는 성공 종료하지만, 출력된 JSON에 의해 툴 실행은 차단됨

    \# 4\. 로직: NFR 제약조건 강제  
    \# 예: "외부 라이브러리 제한" 제약이 있을 때 pip install 등을 감지  
    for constraint in constraints:  
        if "No external APIs" in constraint:  
            if "api.stripe.com" in content or "googleapis.com" in content:  
                 print(json.dumps({  
                    "decision": "block",  
                    "reason": f"CONSTRAINT VIOLATION: {constraint}. 외부 API 호출이 감지되었습니다."  
                }))  
                sys.exit(0)  
      
    \# 5\. 로직: ADR 문서 구조 검증  
    if "docs/adr/" in file\_path:  
        required\_sections \=  
        missing \= \[sec for sec in required\_sections if sec not in content\]  
        if missing:  
             print(json.dumps({  
                "decision": "block",  
                "reason": f"ADR FORMAT ERROR: 필수 섹션이 누락되었습니다: {missing}. DNA 표준 템플릿을 사용하세요."  
            }))  
            sys.exit(0)

    \# 모든 검사가 통과하면 아무것도 출력하지 않고 종료 (허용)  
    sys.exit(0)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

기술적 분석:  
이 스크립트는 Claude CODE 훅의 고급 기능인 decision: block을 활용한다. 에이전트가 코드를 작성하려고 할 때, 실제 파일 시스템에 쓰기 전에 이 스크립트가 내용을 검사한다. 만약 A-A-A 패밀리(고빈도 거래) 시스템을 구축 중인데 에이전트가 느린 HTTP 요청 코드를 작성하려 한다면, 훅은 이를 차단하고 "아키텍처 위반"이라는 명확한 피드백을 에이전트에게 전달한다. 이는 에이전트가 즉시 실수를 인지하고 수정하게 만드는 강력한 피드백 루프를 형성한다.11

### **3.2 동적 상태 관리 훅 (Dynamic State Management Hook)**

프로젝트가 진행됨에 따라 변경되는 상태(예: 패밀리 결정 완료, ADR 작성 완료 등)를 추적하기 위해 PostToolUse 훅을 사용한다. 에이전트가 문서를 작성하면, 이 훅이 해당 문서를 파싱하여 context\_summary.json을 업데이트한다.

**기술 아티팩트: .claude/hooks/update\_context\_graph.py**

Python

import sys  
import json  
import re  
import os

def extract\_family(content):  
    \# 마크다운 내용에서 패밀리 코드를 정규식으로 추출  
    match \= re.search(r'패밀리 코드:\\s\*(-\[A-C\]-\[A-C\])', content)  
    return match.group(1) if match else None

def main():  
    try:  
        input\_data \= json.load(sys.stdin)  
    except:  
        sys.exit(0)  
          
    tool\_input \= input\_data.get('tool\_input', {})  
    file\_path \= tool\_input.get('file\_path', '')  
      
    \# 01C-01\_family\_classification.md 파일이 수정되었을 때만 반응  
    if "01C-01\_family\_classification.md" in file\_path:  
        content \= tool\_input.get('content', '')  
        family \= extract\_family(content)  
          
        if family:  
            \# 영구적 컨텍스트 상태 업데이트  
            context\_file \= '.claude/context\_summary.json'  
            if os.path.exists(context\_file):  
                with open(context\_file, 'r') as f:  
                    data \= json.load(f)  
            else:  
                data \= {"core\_decisions": {}}  
              
            data\['core\_decisions'\]\['family'\] \= family  
              
            with open(context\_file, 'w') as f:  
                json.dump(data, f, indent=2, ensure\_ascii=False)  
              
            \# 에이전트에게 피드백 (stdout은 상세 모드에서 에이전트에게 보임)  
            print(f" 컨텍스트 업데이트 완료: 시스템 패밀리가 '{family}'로 확정되었습니다. 이후 모든 작업은 이 제약조건 하에 검증됩니다.")

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

이러한 PostToolUse 훅은 에이전트가 수행한 작업의 결과를 즉시 시스템의 '기억(Memory)'으로 변환한다. 이는 LLM의 제한된 컨텍스트 윈도우에 의존하지 않고, 파일 시스템 기반의 영구적인 상태 저장소를 구축함으로써 Context Rot를 원천적으로 차단한다.14

---

## **4\. 오케스트레이션 레이어 (The Orchestration Layer): 슬래시 커맨드 워크플로우**

슬래시 커맨드(.claude/commands/\*.md)는 DNA의 각 Phase를 실행하는 엔트리 포인트 역할을 한다. 복잡한 프롬프트 체인을 하나의 명령어로 캡슐화하여 사용자와 에이전트가 일관된 프로세스를 따르도록 유도한다.7

### **4.1 Phase 1 워크플로우 구현 (/dna-phase1)**

이 커맨드는 사용자로부터 아이디어를 입력받아, 시스템 분류자 에이전트를 호출하고, 제약 조건을 조사하는 일련의 과정을 자동화한다.

**기술 아티팩트: .claude/commands/dna-phase1.md**

---

## **description: DNA Phase 1 (아이디어 정제) 실행. 핵심 기능 정의, 패밀리 분류, NFR 프로파일링을 수행함. argument-hint: "\[프로젝트 아이디어 설명\]" allowed-tools: Bash, Read, Write, mcp\_\_sequential-thinking\_\_sequentialthinking**

# **DNA Phase 1: 아이디어 정제 (Idea Refinement)**

**목표:** 사용자의 원시 아이디어($ARGUMENTS)를 분석하여 검증된 패밀리 분류와 NFR 프로파일을 도출한다.

컨텍스트:  
사용자 아이디어: $ARGUMENTS  
**워크플로우:**

1. **초기화:** .claude/context\_summary.json 파일이 있는지 확인하고 없으면 빈 구조를 생성하라.  
2. 시스템 분류자 호출 (Activate System Classifier):  
   서브에이전트 system-classifier-spark를 호출하라.  
   사용자의 아이디어를 전달하고, \*\*3-Layer 심문(Interrogation)\*\*을 수행하도록 지시하라.  
   제약: 서브에이전트가 7가지 패밀리 중 하나로 매핑을 완료하고 01C-01\_family\_classification.md를 생성할 때까지 결과를 승인하지 말라.  
3. 제약 조건 조사 (Constraint Investigation):  
   패밀리 분류 파일이 생성되면, constraints-investigator-spark 서브에이전트를 호출하라.  
   작업: 패밀리 분류 결과를 읽고, 해당 패밀리에서 발생할 수 있는 Layer 3 제약(인프라, 팀, 기술)을 식별하라.  
   출력: 02C-01\_constraints.md 생성.  
4. 검증 (Validation):  
   생성된 파일들이 DNA 표준 형식을 따르는지 확인하기 위해 python3.claude/hooks/validate\_consistency.py를 수동으로 실행해보라(Dry Run).  
5. 요약:  
   생성된 파일들의 핵심 내용을 요약하여 사용자에게 보고하고, Phase 2로 진행할지 물어보라.

기술적 분석:  
이 슬래시 커맨드는 $ARGUMENTS 변수를 사용하여 사용자의 입력을 동적으로 프롬프트에 주입한다.7 또한, 메인 에이전트가 직접 작업을 수행하는 것이 아니라, 전문화된 서브에이전트(system-classifier-spark)를 오케스트레이션하도록 지시한다. 이는 Claude CODE의 멀티 에이전트 협업 기능을 활용하여 단일 에이전트의 인지 과부하를 방지한다.16 또한 argument-hint를 제공하여 CLI에서 자동 완성을 지원함으로써 사용자 경험을 향상시킨다.17

### **4.2 Phase 4 레고블럭 워크플로우 (/dna-lego-breakdown)**

Phase 4는 설계된 청사진을 독립적인 작업 단위(Task)로 분해하는 과정이다. 이 과정은 Skeleton-of-Thought (SoT) 기법을 사용하여 병렬 처리가 가능한 구조로 작업을 나눈다.1

**기술 아티팩트: .claude/commands/dna-lego-breakdown.md**

---

## **description: 청사진(Blueprint)을 읽고 독립적인 Task 파일(레고블럭)로 분해함. allowed-tools: Read, Write, Bash**

# **DNA Phase 4: 레고블럭 분해 (Lego Block Breakdown)**

**목표:** docs/blueprints/07B-01\_project\_blueprint.md를 분석하여 docs/tasks/ 디렉토리에 개별 작업 파일로 분해한다.

**지시사항:**

1. **청사진 독해:** docs/blueprints/ 내의 모든 청사진 파일을 읽어라.  
2. SoT(Skeleton-of-Thought) 적용:  
   청사진에서 정의된 컴포넌트들을 식별하라.  
   각 컴포넌트에 대해 다음을 포함하는 Task 정의를 생성하라:  
   * **입력(Input):** 이 블록이 필요로 하는 데이터나 상태.  
   * **출력(Output):** 이 블록이 생성하는 결과물.  
   * **검증(Validation):** 작동 여부를 증명할 테스트 케이스.  
   * **의존성(Dependencies):** 이 블록보다 먼저 존재해야 하는 블록.  
3. 파일 생성:  
   각 작업에 대해 docs/tasks/task-{id}-{name}.md 파일을 생성하라.  
   제약: 각 태스크는 4시간 이내에 구현 가능한 크기여야 한다. 너무 크다면 더 작게 쪼개라.  
4. 체크리스트 생성:  
   모든 태스크를 실행 순서대로 나열한 마스터 체크리스트 09G-00\_checklist\_guide.md를 생성하라.

이 커맨드는 거대한 문서를 실행 가능한 단위로 잘게 쪼개는 DNA의 핵심 철학인 "Lego Block Strategy"를 구현한다.1 Claude가 스스로 작업의 크기를 판단하고 분할하도록 유도하는 것이 핵심이다.

---

## **5\. 상태 관리 및 컨텍스트 엔지니어링 (State Management & Context Engineering)**

에이전트가 장기 프로젝트를 수행할 때 가장 큰 적은 망각이다. DNA 방법론은 이를 방지하기 위해 CLAUDE.md를 동적으로 활용하는 전략을 취한다.6

### **5.1 동적 CLAUDE.md 구성 및 업데이트**

CLAUDE.md는 Claude CODE가 세션을 시작할 때마다 자동으로 읽어들이는 메모리 파일이다. DNA 구현에서는 이 파일이 정적인 규칙 나열에 그치지 않고, 훅(Hook)에 의해 현재 프로젝트의 상태(Family, NFR 등)를 실시간으로 반영하도록 구성된다.

**기술 아티팩트: CLAUDE.md 템플릿**

# **DNA Project Guidelines**

## **Core Context (Dynamically Managed)**

경고: 이 섹션은 Hooks에 의해 자동 업데이트됩니다. 수동으로 수정하지 마십시오.  
Family: NFR Priority: Critical Constraints: \#\# Project Standards

* **Language:** Python 3.11+  
* **Framework:** FastAPI  
* **Documentation:** 모든 함수는 Google-style docstring을 포함해야 함.  
* **Testing:** Pytest 커버리지 90% 이상 필수.

## **Workflow Rules**

1. /dna-phaseX 커맨드를 사용하여 프로젝트를 진행하십시오.  
2. docs/adr/\* 문서는 반드시 arch-decision-maker 에이전트를 통해서만 수정해야 합니다.

앞서 정의한 update\_context\_graph.py 훅을 확장하여, context\_summary.json이 변경될 때마다 CLAUDE.md의 \`\` 부분을 실제 값으로 치환하는 로직을 추가해야 한다. 이렇게 하면 새로운 세션을 시작하더라도 Claude는 "아, 이 프로젝트는 A-A-A 패밀리구나"라는 사실을 즉시 인지하고 시작하게 된다.6 이는 동적 컨텍스트 주입(Dynamic Context Injection)의 실용적인 구현체이다.19

---

## **6\. 구현 로드맵 및 실행 가이드**

위에서 설계한 아키텍처를 실제 프로젝트에 적용하기 위한 단계별 가이드이다.

1. **디렉토리 구조 초기화:**  
   Bash  
   mkdir \-p.claude/agents  
   mkdir \-p.claude/commands  
   mkdir \-p.claude/hooks  
   mkdir \-p docs/adr docs/blueprints docs/tasks

2. **아티팩트 배포:**  
   * system-classifier.md, arch-decision-maker.md 등을 .claude/agents/에 저장.  
   * dna-phase1.md 등을 .claude/commands/에 저장.  
   * settings.json을 .claude/에 저장.  
   * Python 훅 스크립트들을 .claude/hooks/에 저장하고 실행 권한 부여.  
3. **초기 컨텍스트 설정:**  
   * 플레이스홀더가 포함된 CLAUDE.md 생성.  
   * 빈 context\_summary.json 생성.  
4. **실행 시나리오:**  
   * 사용자가 /dna-phase1 "암호화폐 차익거래를 위한 초고빈도 매매 시스템"을 입력.  
   * **System Classifier**가 작동하여 레이턴시 요구사항을 심문하고 **A-A-A** 패밀리로 확정.  
   * **Post-Hook**이 작동하여 context\_summary.json과 CLAUDE.md에 "Family: A-A-A"를 기록.  
   * 이후 사용자가 /dna-phase2를 실행하여 DB를 선택하려 할 때, Claude가 실수로 MongoDB(일반적인 선택)를 제안하려 하면, **Pre-Hook**이 이를 감지하고 "A-A-A 패밀리 위반: KDB+나 Time-Series DB를 고려하시오"라고 차단 및 경고.

---

## **결론 (Conclusion)**

본 보고서에서 제시한 아키텍처는 DNA v4.0 방법론을 Claude CODE라는 현대적인 도구 위에 구현한 실증적 청사진이다. **서브에이전트**를 통해 방법론의 '역할과 특성'을 인격화하고, **슬래시 커맨드**를 통해 '단계적 프로세스'를 자동화하며, **훅**을 통해 '환경의 힘'을 결정론적 코드로 강제함으로써, LLM 기반 개발의 고질적인 문제인 환각과 컨텍스트 부패를 효과적으로 제어할 수 있다. 이 시스템은 DNA 방법론이 단순한 이론적 가이드라인을 넘어, 실제 개발 현장에서 작동하는 강력한 '구속복(Straitjacket)'이자 '가이드레일'로 기능하게 할 것이다. 이는 결과적으로 인간 개발자와 AI 에이전트가 복잡한 시스템을 일관성 있게 구축할 수 있는 견고한 토대가 된다.

#### **참고 자료**

1. 01\_DNA\_Agent\_Integrated\_Process\_Flow.txt  
2. Claude Code overview \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)  
3. Get started with Claude Code hooks, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide)  
4. Subagents \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)  
5. Building agents with the Claude Agent SDK \- Anthropic, 11월 19, 2025에 액세스, [https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)  
6. Claude Code: Best practices for agentic coding \- Anthropic, 11월 19, 2025에 액세스, [https://www.anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)  
7. Your complete guide to slash commands Claude Code \- eesel AI, 11월 19, 2025에 액세스, [https://www.eesel.ai/blog/slash-commands-claude-code](https://www.eesel.ai/blog/slash-commands-claude-code)  
8. Hooks reference \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)  
9. Claude Code settings \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/settings](https://code.claude.com/docs/en/settings)  
10. A practical guide to MCP integration with Claude Code \- eesel AI, 11월 19, 2025에 액세스, [https://www.eesel.ai/blog/mcp-integration-claude-code](https://www.eesel.ai/blog/mcp-integration-claude-code)  
11. Claude Code Hook Control Flow | Developing with AI Tools \- Steve Kinney, 11월 19, 2025에 액세스, [https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow](https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow)  
12. disler/claude-code-hooks-mastery \- GitHub, 11월 19, 2025에 액세스, [https://github.com/disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)  
13. How Claude Code Hooks Save Me HOURS Daily \- YouTube, 11월 19, 2025에 액세스, [https://www.youtube.com/watch?v=Q4gsvJvRjCU](https://www.youtube.com/watch?v=Q4gsvJvRjCU)  
14. disler/claude-code-hooks-multi-agent-observability \- GitHub, 11월 19, 2025에 액세스, [https://github.com/disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)  
15. Can Claude Code execute slash commands from markdown files? : r/ClaudeAI \- Reddit, 11월 19, 2025에 액세스, [https://www.reddit.com/r/ClaudeAI/comments/1lf4b9i/can\_claude\_code\_execute\_slash\_commands\_from/](https://www.reddit.com/r/ClaudeAI/comments/1lf4b9i/can_claude_code_execute_slash_commands_from/)  
16. You can now create custom subagents for specialized tasks\! Run /agents to get started, 11월 19, 2025에 액세스, [https://www.reddit.com/r/ClaudeAI/comments/1m8gl6b/you\_can\_now\_create\_custom\_subagents\_for/](https://www.reddit.com/r/ClaudeAI/comments/1m8gl6b/you_can_now_create_custom_subagents_for/)  
17. Slash commands \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands)  
18. Manage Claude's memory \- Claude Code Docs, 11월 19, 2025에 액세스, [https://code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory)  
19. Dynamic Context Injection \- Awesome Agentic Patterns, 11월 19, 2025에 액세스, [https://agentic-patterns.com/patterns/dynamic-context-injection/](https://agentic-patterns.com/patterns/dynamic-context-injection/)