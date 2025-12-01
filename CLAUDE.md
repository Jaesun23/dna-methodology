# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DNA Methodology v4.0 is a 9-Stage software design framework that overcomes AI context limitations during collaboration. It provides a systematic approach from abstract ideas to production-ready systems.

**DNA**: Like DNA is the foundation of life, the 11 DNA Systems are the foundation of software - the most fundamental systems every project needs.

**Core Problem**: AI context decay (Context Rot) - as conversations grow, initial decisions fade, leading to inconsistency and incomplete implementations.

**Solution Strategy**:
1. **Staged Definition**: Build environment (Stage 1-6) → Execute (Stage 7-9)
2. **Environment Enforcement**: Standards + DNA Systems + Automation ensure consistency
3. **LEGO Block Strategy**: Break work into independent, self-contained units

## 9-Stage Process

```
Stage 1: Core Definition (Family Classification)
Stage 2: Environment Constraints (Layer 3 Investigation)
Stage 3: ADR (Architecture Decision Records)
Stage 4: DNA System Planning (11 Common Modules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage 5: DNA System Implementation
Stage 6: Project Standards
Stage 7: Blueprint Creation
Stage 8: Task Breakdown
Stage 9: Governance & Automation
```

## Agent Architecture

DNA Methodology uses 9 specialized agents (all with `-dna` suffix):

### Stage 1-4: New Agents (Not Yet Implemented)
- `classifier-dna` - Family classification using CoD (Chain of Density)
- `investigator-dna` - Environment constraints investigation
- `decision-maker-dna` - ADR authoring with Context7
- `planner-dna` - DNA system planning

### Stage 5-9: Copied from SPARK (Completed)
- `implementer-dna` - DNA system implementation
- `documenter-dna` - Standards documentation
- `designer-dna` - Blueprint creation
- `analyzer-dna` - Task breakdown
- `qc-dna` - Governance & automation

**Note**: Stage 5-9 agents are copied from SPARK Agent System with only the `name` field changed in YAML frontmatter. All Traits, Workflow, and Behavior Protocol remain identical.

## Key Concepts

### 18 Architecture Families

Systems classified by 3-layer decision tree:
- **Layer 1**: Failure Impact (A: Critical, B: Serious, C: Minor)
- **Layer 2**: Data Attributes (A: Structured, B: Semi-structured, C: Unstructured)
- **Layer 3**: Response Time (A: Milliseconds, B: Seconds, C: Minutes/Hours)

Examples:
- **A-A-A**: Financial trading system
- **C-B-B**: Blog platform
- **A-C-A**: Real-time transactions (newly discovered pattern!)

### 11 DNA Systems

Reusable common modules for all projects:
1. Logging (structlog)
2. Configuration (Pydantic)
3. Database (SQLAlchemy)
4. Cache (Redis)
5. Messaging (RabbitMQ)
6. Types (Strong type system)
7. Testing (pytest)
8. Monitoring (Prometheus)
9. Security (Auth/Authorization)
10. Error Handling
11. API Gateway

### Context Rot Prevention (3-Layer Defense)

1. **JSON State**: Store each Stage result in structured files
2. **Context Re-ranking**: Load only relevant context for next Stage
3. **Validation**: Automatic verification at each Stage completion

## Development Workflow

### Plugin Installation

```bash
# 1. Install SPARK plugin (required dependency)
/plugin install https://github.com/Jaesun23/spark-claude

# 2. Install DNA plugin
cd dna-methodology
/plugin install .
```

### Usage Commands

```bash
# Initialize DNA project
/dna:init "Stock Trading Platform"

# Execute stages sequentially
/dna:stage1  # Family classification
/dna:stage2  # Environment constraints
/dna:stage3  # ADR creation
/dna:stage4  # DNA system planning
/dna:stage5  # DNA system implementation
/dna:stage6  # Project standards
/dna:stage7  # Blueprint creation
/dna:stage8  # Task breakdown
/dna:stage9  # Governance & automation
```

**Current Status**: Commands not yet implemented. Only agents for Stage 5-9 are complete.

## File Structure

```
dna-methodology/
├── dna-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   │   ├── implementer-dna.md       ✅ Stage 5
│   │   ├── documenter-dna.md        ✅ Stage 6
│   │   ├── designer-dna.md          ✅ Stage 7
│   │   ├── analyzer-dna.md          ✅ Stage 8
│   │   └── qc-dna.md                ✅ Stage 9
│   │   # Missing: classifier-dna, investigator-dna, decision-maker-dna, planner-dna
│   ├── skills/
│   │   ├── assets/templates/
│   │   └── references/
│   └── commands/                    ❌ Not yet created
├── docs/
│   ├── guides/                      📚 Stage 1-9 methodology guides
│   ├── plugin-guide/                📚 Plugin development guides
│   └── integration/                 📚 SPARK integration docs
└── .claude/
    └── dependencies.json
```

## DNA File Naming Convention

Pattern: `{Stage}{Type}-{Seq}_{descriptive_name}.md`

### Type Codes
- **F** = Function (기능 정의)
- **C** = Classification (분류/분석)
- **D** = Decision (결정 사항)
- **A** = ADR (Architecture Decision Record)
- **B** = Blueprint (청사진)
- **T** = Task (작업 분해)
- **L** = List/Checklist (체크리스트)
- **G** = Guide (간결한 가이드)
- **M** = Manual (상세 해설서)
- **E** = Example/Case (사례집)

Examples:
```
01F-01_core_functions.md          # Stage 1 function definition
02C-01_layer3_constraints.md      # Stage 2 constraints classification
03A-001_logging.md                # Stage 3 ADR (Bootstrap #1)
07B-01_blueprint.md               # Stage 7 blueprint
09L-001_task1_checklist.md        # Stage 9 checklist for task 1
```

## Critical Principles

### 1. Environment First, Then Execution

**Wrong Approach**:
```
Idea → Blueprint → Implementation
(Blueprint incomplete due to missing environment context)
```

**Correct Approach**:
```
Stage 1-6: Build Environment (Family, Constraints, ADR, DNA Systems, Standards)
    ↓
Stage 7: Blueprint (Now complete with full environment context)
    ↓
Stage 8-9: Task Breakdown → Execution
```

### 2. Environment Enforcement (Not Just Documentation)

**The Problem**: Telling AI rules verbally → repeated failures
- Type errors
- Using `print()` instead of logger
- Unmocked dependencies
- TODO/pass left in code

**The Solution**: "Environment" = Standards + DNA Systems + Automation
```
Standards (documented rules):
  "DO NOT use print()"
    ↓
DNA Systems (common modules):
  src/core/logging/ (structlog)
    ↓
Automation (enforcement):
  Pre-commit hook detects print() → blocks commit
```

**Result**: AI cannot make mistakes even if it wants to!

### 3. LEGO Block Strategy

Break work into blocks that fit together perfectly:

```
Blueprint (complete design after environment ready)
    ↓
Task Breakdown (independent LEGO blocks)
    - Each task: 2-4 hours
    - No TODO, no pass
    - Complete and verified
    ↓
Checklist (execution manual for each block)
    - Read only this checklist
    - Execute only this task
    - Independent execution
    ↓
Implementation
    - Each checklist done = one block complete
    - All checklists done = project complete
```

### 4. Jason's Blueprint 3-Phase Process

**Phase 1: Blueprint** - Capture everything while context is fresh
- Purpose: Complete design document when context is intact
- Principle: Detailed enough for anyone to implement independently

**Phase 2: Task Breakdown** - Create LEGO blocks
- Purpose: Split long blueprint (can't implement at once) into blocks
- Principle: Atomic units, each task 2-4 hours

**Phase 3: Checklist** - Execution manual per block
- Purpose: Detailed checklist per task in separate files
- Principle: Read only this checklist, execute only this task (independent)
- Result: All checklists done = entire project complete

> **"If you can do it all at once, just use the blueprint. But when you can't, make it 'complete' in smaller chunks. Create a plan where executing each piece completes the whole. Context limitation breakthrough!!! The method is to create the 'environment'!"** - Jason

## Relationship with SPARK Agent System

**SPARK** (spark-claude):
- Identity: General-purpose AI agent orchestration system
- Purpose: Traits + Role-based agent research
- Naming: `{role}-spark`

**DNA** (dna-methodology):
- Identity: AI collaboration development framework (software design methodology)
- Purpose: 9-Stage process + Skills refinement
- Naming: `{role}-dna`

**Dependency**: DNA reuses SPARK agents for Stage 5-9 by copying and renaming. No runtime dependency—agents are independent copies.

## Important Documentation

### User Guides
- `docs/guides/00_CORE_METHODOLOGY.md` - DNA v4.0 overview
- `docs/guides/01G-00_*.md` - Stage 1 guides
- `docs/guides/02G-00_*.md` - Stage 2 guides
- `docs/guides/03G-00_*.md` - Stage 3 guides

### Developer Guides
- `docs/plugin-guide/plugin-structure-guide.md` - Claude Code plugin development
- `docs/plugin-guide/agent-definition-structure.md` - 7-Section agent structure
- `docs/plugin-guide/stage-execution-guide.md` - Stage goals, techniques, references

### Integration Guides
- `docs/integration/spark-agent-mapping.md` - DNA ↔ SPARK mapping
- `docs/integration/agent-naming-convention.md` - Agent naming strategy

## Current Project Status

**Completed**:
- ✅ Stage 5-9 agents (copied from SPARK, renamed to `-dna`)
- ✅ Documentation structure (guides, plugin-guide, integration)
- ✅ Basic plugin structure

**Not Yet Implemented**:
- ❌ Stage 1-4 agents (classifier, investigator, decision-maker, planner)
- ❌ All commands (`/dna:init`, `/dna:stage1` ~ `/dna:stage9`)
- ❌ Validator scripts
- ❌ Skills implementation

**Next Steps**:
1. Implement Stage 1-4 agents following agent-definition-structure.md
2. Create command definitions in `dna-plugin/commands/`
3. Implement validator scripts
4. Test end-to-end workflow

## Key References

- **SPARK Repository**: https://github.com/Jaesun23/spark-claude
- **SEI Architecture Decision**: Software Engineering Institute
- **Gemini 4-Phase Process**: CoD, ToT, SoT techniques
- **Research Base**: Jason's 2 years of AI collaboration experience, 7 project failure analysis

## Contact

- **Author**: Jason (Jaesun23)
- **Email**: jaesun23@gmail.com
- **GitHub**: https://github.com/Jaesun23
- **Issues**: https://github.com/Jaesun23/dna-methodology/issues

---

**"Context limitation breakthrough!!! The method is to create the 'environment'!"** - Jason
