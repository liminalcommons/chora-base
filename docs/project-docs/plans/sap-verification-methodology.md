# SAP Verification Methodology

**Repository**: https://github.com/liminalcommons/chora-base-SAP-Verification
**Purpose**: Verify SAP efficacy by emulating exact adopter experience
**Framework**: Aligned with SAP-027 Dogfooding Patterns
**Version**: 1.0.0
**Created**: 2025-11-07

---

## 1. Core Principle

**Objective**: Verify that chora-base's fast-setup script creates working, production-ready projects with pre-configured SAPs at documented maturity levels. Test the actual user adoption path, not hypothetical manual SAP discovery.

**Key Insight**: Chora-base users adopt via fast-setup script (`python scripts/create-model-mcp-server.py`), which creates fully-configured projects in 1-2 minutes. Verification must test this actual workflow, not manual SAP adoption from GitHub.

**Two Verification Workflows**:
1. **Primary (Fast-Setup Workflow)**: Test that fast-setup script creates projects with working SAP configurations
2. **Secondary (Incremental SAP Adoption)**: Test adding new SAPs to fast-setup generated projects

---

## 2. Verification Framework Overview

### 2.1 Verification Lifecycle (Aligned with SAP-027)

```
Phase 1: Setup (Week 1)
├─ Define expected results for target maturity level
├─ Create verification plan (automated + manual checks)
├─ Set up metrics collection infrastructure
└─ Establish GO/NO-GO thresholds

Phase 2: Execution (Weeks 2-4)
├─ Guide Claude Code through SAP adoption
├─ Execute adoption steps from adoption-blueprint.md
├─ Collect metrics (time, errors, blockers, artifacts)
└─ Log events to verification.jsonl

Phase 3: Analysis (Week 5)
├─ Run automated verification checks
├─ Calculate quantitative metrics
├─ Assess qualitative outcomes
└─ Compare results vs expected outcomes

Phase 4: Decision (Week 6)
├─ Apply GO/NO-GO framework
├─ Document decision rationale
├─ Update SAP status (pilot → production or deprecated)
└─ Share verification report with ecosystem
```

---

## 3. Defining "Expected Results" by Maturity Level

### 3.1 Maturity Level Outcomes Framework

**For Fast-Setup Generated Projects**: Each SAP included in fast-setup should be pre-configured at a documented maturity level. Expected results are **evidence that the generated project meets those criteria out-of-the-box**.

**For Incremental SAP Adoption**: When adding new SAPs to a fast-setup project, expected results are **evidence that the adoption process (via adoption-blueprint.md) successfully achieves target maturity level**.

#### L1 (Configured) - Expected Results

**Definition**: Basic setup completed, minimal usage demonstrated.

**Expected Results**:
1. **Configuration Artifacts Present**:
   - Config files exist and are valid (e.g., `tailwind.config.ts`, `.eslintrc.js`, `vitest.config.ts`)
   - Required dependencies installed (`package.json` or `requirements.txt`)
   - Basic file structure matches SAP specification

2. **Minimal Functional Evidence**:
   - At least 1 working example (component, test, command)
   - Example can be executed without errors
   - README documents the SAP with basic usage

3. **Verification Methods**:
   - **Automated**: File existence checks, config validation, dependency version checks
   - **Quantitative**: Setup time < 2 hours, 0 blocking errors
   - **Qualitative**: README clarity (can a new user understand what was added?)

**Example (SAP-024 React Styling at L1)**:
- ✅ `tailwind.config.ts` exists and exports valid config object
- ✅ `npm list tailwindcss` shows installation
- ✅ At least 5 components use Tailwind utilities (verified by grep)
- ✅ README has "React Styling (SAP-024)" section
- ✅ Setup completed in < 2 hours (time-tracked)

---

#### L2 (Usage) - Expected Results

**Definition**: Comprehensive usage across multiple features, integration patterns established.

**Expected Results**:
1. **Usage Breadth**:
   - Multiple instances of SAP usage (10+ tests, 10+ styled components, 5+ Zustand stores, etc.)
   - Integration with other SAPs demonstrated (e.g., SAP-024 + SAP-020)
   - Patterns from AGENTS.md/awareness-guide.md actually used in codebase

2. **Documentation Maturity**:
   - README documents comprehensive usage patterns
   - Code examples match protocol-spec.md specifications
   - Patterns are findable via grep/search

3. **Verification Methods**:
   - **Automated**: Count usage instances (grep patterns), validate integration points, check documentation completeness
   - **Quantitative**: Usage count ≥ threshold (e.g., 10+ tests, 5+ stores), integration score (% of integration patterns adopted)
   - **Qualitative**: Pattern consistency (do usage instances follow documented patterns?)

**Example (SAP-021 React Testing at L2)**:
- ✅ 10+ component tests exist (`**/*.test.tsx`)
- ✅ Coverage threshold configured in `vitest.config.ts` (≥50%)
- ✅ Custom hooks tested with `renderHook` (≥1 instance)
- ✅ Async testing patterns used (`waitFor`, `findBy` - ≥3 instances)
- ✅ README documents test organization structure

---

#### L3 (Active) - Expected Results

**Definition**: Best practices adopted, advanced patterns used, AGENTS.md updated, CI/CD integration.

**Expected Results**:
1. **Best Practices Evidence**:
   - Advanced patterns from protocol-spec.md implemented
   - CI/CD integration configured (GitHub Actions, pre-commit hooks)
   - AGENTS.md documents SAP-specific patterns for AI agents
   - Performance/quality thresholds met (e.g., bundle size <300KB, test coverage >70%)

2. **Systematic Usage**:
   - Patterns used systematically across codebase (not just 1-2 examples)
   - Integration with 2+ other SAPs demonstrated
   - Metrics tracked (performance, quality, usage)

3. **Verification Methods**:
   - **Automated**: CI/CD config checks, AGENTS.md validation, performance metric extraction, pattern coverage analysis
   - **Quantitative**: Performance budgets met, coverage ≥70%, CI/CD green, AGENTS.md completeness score
   - **Qualitative**: Pattern quality (do implementations follow best practices?), AGENTS.md usefulness (can Claude Code use it effectively?)

**Example (SAP-023 React State Management at L3)**:
- ✅ Clear separation of client state (Zustand) vs server state (TanStack Query) vs local state
- ✅ Zustand persistence middleware configured for theme/preferences
- ✅ TanStack Query mutations with optimistic updates (≥1 instance)
- ✅ DevTools configured (Redux DevTools for Zustand, React Query DevTools)
- ✅ AGENTS.md documents state management decision tree
- ✅ Performance optimization (selectors, React.memo) used (≥5 instances)

---

#### L4 (Deep) - Expected Results

**Definition**: Optimization achieved, custom patterns developed, metrics dashboard, advanced integration.

**Expected Results**:
1. **Optimization Evidence**:
   - Performance optimized beyond baseline (bundle size, test speed, re-render reduction)
   - Custom utilities/patterns developed for project needs
   - Metrics tracked over time (trends, regressions detected)
   - IDE integration configured (VSCode extensions, auto-fix on save)

2. **Deep Integration**:
   - Advanced patterns from multiple SAPs combined
   - Custom improvements contributed back to chora-base (PRs, feedback)
   - Organization-wide standards enforced

3. **Verification Methods**:
   - **Automated**: Performance regression checks, custom pattern validation, metrics trend analysis
   - **Quantitative**: Performance improvement % vs baseline, custom pattern usage count, metric stability
   - **Qualitative**: Innovation assessment (are custom patterns valuable?), ecosystem contribution quality

**Example (SAP-025 React Performance at L4)**:
- ✅ Performance budget defined and enforced (<300KB initial bundle, <3s TTI)
- ✅ Bundle size optimized (<200KB actual vs <300KB target)
- ✅ React 18 concurrent features adopted (useTransition OR useDeferredValue - ≥3 instances)
- ✅ Virtual scrolling for long lists (`react-window` - ≥1 instance)
- ✅ Web Vitals monitoring configured (LCP, FID, CLS tracking)
- ✅ Performance profiling workflow documented in AGENTS.md

---

#### L5 (Mature) - Expected Results

**Definition**: SAP dogfooded and validated via SAP-027, contributing improvements to ecosystem, mentoring others.

**Expected Results**:
1. **Ecosystem Contribution**:
   - SAP validated using SAP-027 dogfooding methodology (GO decision documented)
   - Improvements contributed back to chora-base (PRs merged)
   - Patterns shared across multiple projects
   - Mentoring others (documentation, examples, support)

2. **Validation Evidence**:
   - SAP-027 pilot completed with GO decision
   - ROI analysis shows positive break-even
   - Satisfaction ≥4/5, time savings ≥5x, quality metrics met
   - Historical usage tracked in ledger.md

3. **Verification Methods**:
   - **Automated**: SAP-027 completion check, contribution tracking (PR count, merged status)
   - **Quantitative**: ROI calculation, pilot metrics (time savings, satisfaction, quality)
   - **Qualitative**: Ecosystem impact assessment, mentoring effectiveness

**Example (Any SAP at L5)**:
- ✅ SAP-027 pilot completed with documented GO decision
- ✅ Pilot metrics: Time savings ≥5x, satisfaction ≥4/5, 0 critical bugs
- ✅ Improvements contributed to chora-base (≥1 merged PR)
- ✅ Patterns shared across 2+ projects
- ✅ Ledger.md documents adoption history and feedback

---

## 4. Verification Method Categories

### 4.1 Automated Checks (Fast, Objective, Repeatable)

**Purpose**: Verify objective criteria without human judgment.

**Method Types**:

1. **File Existence Checks**:
   ```bash
   # Example: SAP-024 React Styling L1
   test -f tailwind.config.ts && echo "✅ Config exists" || echo "❌ Config missing"
   test -f postcss.config.js && echo "✅ PostCSS exists" || echo "❌ PostCSS missing"
   ```

2. **Configuration Validation**:
   ```python
   # Example: SAP-021 React Testing L1
   import json
   with open('vitest.config.ts') as f:
       config = f.read()
       assert 'react' in config.lower(), "Missing React environment"
       assert 'coverage' in config.lower(), "Missing coverage config"
   ```

3. **Usage Pattern Counting**:
   ```bash
   # Example: SAP-025 React Performance L2
   MEMO_COUNT=$(grep -r "React.memo" src/ | wc -l)
   [ $MEMO_COUNT -ge 3 ] && echo "✅ Memoization used ($MEMO_COUNT instances)" || echo "❌ Insufficient memoization"
   ```

4. **Dependency Version Checks**:
   ```bash
   # Example: SAP-020 React Foundation L1
   npm list react@^18 && echo "✅ React 18 installed" || echo "❌ Wrong React version"
   ```

5. **Command Success Tests**:
   ```bash
   # Example: SAP-022 React Linting L1
   npm run lint && echo "✅ Linting passes" || echo "❌ Linting errors"
   npm run format:check && echo "✅ Formatting OK" || echo "❌ Formatting needed"
   ```

6. **Performance Metric Extraction**:
   ```bash
   # Example: SAP-025 React Performance L4
   BUNDLE_SIZE=$(du -k dist/index.js | cut -f1)
   [ $BUNDLE_SIZE -lt 300 ] && echo "✅ Bundle size OK (${BUNDLE_SIZE}KB)" || echo "❌ Bundle too large"
   ```

**Advantages**:
- Fast execution (seconds)
- Objective (no human bias)
- Repeatable (same results every time)
- CI/CD integration ready

**Limitations**:
- Cannot assess quality or appropriateness
- Cannot verify subjective criteria (documentation clarity, pattern elegance)
- Cannot detect anti-patterns disguised as correct usage

---

### 4.2 Quantitative Metrics (Measurable, Comparable, Trend-Trackable)

**Purpose**: Measure adoption outcomes numerically for comparison against thresholds.

**Metric Categories**:

1. **Time Metrics**:
   - Setup time (start → L1 configured)
   - Adoption time per level (L1 → L2 → L3 → L4 → L5)
   - Time savings vs manual approach (SAP-027 dogfooding framework)
   - Break-even point (setup cost ÷ per-use savings)

2. **Quality Metrics**:
   - Error count during adoption (blocking errors = 0 target)
   - Test coverage % (varies by SAP: 50% L2, 70% L3, 85% L4)
   - Linting violations (0 violations target)
   - Bundle size (KB), performance scores (Lighthouse, Web Vitals)

3. **Usage Metrics**:
   - Pattern usage count (tests, components, stores, hooks)
   - Integration coverage (% of integration patterns adopted)
   - Documentation completeness (% of required touchpoints present)
   - AGENTS.md keyword coverage (% of keywords documented)

4. **Satisfaction Metrics**:
   - Developer rating (1-5 scale, ≥4/5 target)
   - Pain point count (blockers, friction, confusion)
   - Recommendation likelihood (Net Promoter Score)

**Example Metrics Dashboard (SAP-024 React Styling)**:

| Metric | L1 Target | L2 Target | L3 Target | Actual | Status |
|--------|-----------|-----------|-----------|--------|--------|
| Setup time | <2h | <4h | <6h | 1.5h | ✅ L1 |
| Components styled | ≥5 | ≥20 | ≥50 | 8 | ✅ L1 |
| Design tokens defined | ≥3 | ≥10 | ≥20 | 5 | ✅ L1 |
| Dark mode configured | No | Yes | Yes + persistence | No | ⏸️ L2 pending |
| Bundle size (CSS) | N/A | <50KB | <20KB gzipped | N/A | ⏸️ L2 pending |
| Satisfaction rating | ≥4/5 | ≥4/5 | ≥4/5 | 5/5 | ✅ Excellent |

**Advantages**:
- Comparable across SAPs (standardized metrics)
- Trend-trackable over time (regression detection)
- GO/NO-GO threshold application (SAP-027 framework)
- ROI calculation ready

**Limitations**:
- Requires baseline establishment (first adoption sets baseline)
- May miss qualitative issues (low satisfaction despite good metrics)

---

### 4.3 Qualitative Assessments (Subjective, Context-Dependent, High-Value)

**Purpose**: Assess quality, appropriateness, and effectiveness beyond numbers.

**Assessment Areas**:

1. **Documentation Quality**:
   - **Clarity**: Can a new user understand what was added and why?
   - **Completeness**: Are all required touchpoints present (README, AGENTS.md, examples)?
   - **Usefulness**: Can Claude Code effectively use AGENTS.md to adopt patterns?
   - **Accuracy**: Do examples match actual implementation?

2. **Pattern Quality**:
   - **Appropriateness**: Are the right patterns used for the use case?
   - **Consistency**: Do implementations follow protocol-spec.md consistently?
   - **Best Practices**: Are anti-patterns avoided (prop drilling, Context misuse, etc.)?
   - **Innovation**: Are custom patterns valuable or over-engineered?

3. **Integration Quality**:
   - **Coherence**: Do integrated SAPs work well together?
   - **Efficiency**: Is integration smooth or requires workarounds?
   - **Maintainability**: Is integration sustainable long-term?

4. **Developer Experience**:
   - **Ease of Adoption**: Were there unexpected blockers?
   - **Pain Points**: What caused friction during adoption?
   - **Satisfaction Drivers**: What contributed to high/low satisfaction?

**Assessment Methods**:

1. **Documentation Review Checklist**:
   ```markdown
   SAP-024 React Styling - Documentation Quality Assessment

   README Clarity (1-5): 5/5
   - ✅ Clear explanation of Tailwind CSS choice
   - ✅ Design tokens documented with examples
   - ✅ Dark mode implementation explained
   - ✅ Responsive design patterns shown

   AGENTS.md Usefulness (1-5): 4/5
   - ✅ Decision tree for styling approach
   - ✅ Code examples for common patterns
   - ⚠️ Missing: Troubleshooting section for common issues

   Overall: 4.5/5 - Excellent documentation, minor improvement needed
   ```

2. **Pattern Quality Review**:
   ```markdown
   SAP-023 React State Management - Pattern Quality Assessment

   Appropriateness (1-5): 5/5
   - ✅ Zustand used for client state (theme, preferences)
   - ✅ TanStack Query used for server state (API data)
   - ✅ Context used for DI only (auth, router)
   - ✅ Local state used for component-specific (form inputs)

   Consistency (1-5): 4/5
   - ✅ All stores follow Zustand pattern from AGENTS.md
   - ✅ All queries follow TanStack Query pattern
   - ⚠️ One component uses Context for frequently-changing state (anti-pattern)

   Best Practices (1-5): 4/5
   - ✅ Selectors used to prevent re-renders
   - ✅ Persistence middleware configured correctly
   - ⚠️ Missing: useMemo optimization in one expensive selector

   Overall: 4.3/5 - Strong patterns, minor anti-pattern found
   ```

3. **Developer Experience Interview** (Post-Adoption):
   ```markdown
   SAP-021 React Testing - Developer Experience Assessment

   Q: What was the biggest blocker during adoption?
   A: Configuring Vitest with React environment took 30 mins of trial-and-error.
      Documentation was clear but config syntax was unfamiliar.

   Q: What exceeded expectations?
   A: Test execution speed - Vitest is 5x faster than Jest, instant feedback loop.

   Q: What would you improve in the adoption guide?
   A: Add troubleshooting section for common Vitest errors (ESM issues, path aliases).

   Rating: 4/5 (would be 5/5 with better troubleshooting docs)
   ```

**Advantages**:
- Captures nuanced issues missed by automated checks
- Identifies improvement opportunities
- Assesses real-world effectiveness
- Provides actionable feedback for SAP refinement

**Limitations**:
- Subjective (different reviewers may disagree)
- Time-intensive (requires human review)
- Not automatable (requires judgment)

---

## 5. Verification Methods by Maturity Level

### 5.1 L1 (Configured) Verification Plan

**Goal**: Verify basic setup completed successfully.

**Automated Checks** (10 min):
```bash
#!/bin/bash
# verify-l1.sh - SAP-024 React Styling example

echo "=== L1 (Configured) Verification: SAP-024 React Styling ==="

# 1. Configuration files exist
test -f tailwind.config.ts && echo "✅ tailwind.config.ts exists" || exit 1
test -f postcss.config.js && echo "✅ postcss.config.js exists" || exit 1

# 2. Dependencies installed
npm list tailwindcss autoprefixer postcss | grep -q "tailwindcss" && echo "✅ Tailwind installed" || exit 1

# 3. Basic usage (5+ components)
COMPONENT_COUNT=$(grep -r "className=" src/ --include="*.tsx" | wc -l)
[ $COMPONENT_COUNT -ge 5 ] && echo "✅ $COMPONENT_COUNT components use Tailwind" || exit 1

# 4. README documents SAP
grep -q "React Styling (SAP-024)" README.md && echo "✅ README documents SAP-024" || exit 1

echo "=== L1 Verification: PASS ==="
```

**Quantitative Metrics** (5 min):
- Setup time: Track start → L1 completion (target: <2 hours)
- Error count: Count blocking errors (target: 0)
- Component count: Count styled components (target: ≥5)

**Qualitative Assessment** (15 min):
- README clarity: Can a new user understand what was added? (1-5 scale)
- Config validity: Are configs syntactically correct and semantically appropriate?
- Pattern correctness: Do the 5+ components use Tailwind correctly (no anti-patterns)?

**Total Time**: 30 min
**GO/NO-GO Threshold**: All automated checks pass + setup time <2h + clarity ≥3/5

---

### 5.2 L2 (Usage) Verification Plan

**Goal**: Verify comprehensive usage across multiple features.

**Automated Checks** (20 min):
```bash
#!/bin/bash
# verify-l2.sh - SAP-021 React Testing example

echo "=== L2 (Usage) Verification: SAP-021 React Testing ==="

# 1. Test count (10+ component tests)
TEST_COUNT=$(find src/ -name "*.test.tsx" | wc -l)
[ $TEST_COUNT -ge 10 ] && echo "✅ $TEST_COUNT component tests" || exit 1

# 2. Coverage threshold configured
grep -q "coverage" vitest.config.ts && echo "✅ Coverage configured" || exit 1

# 3. Custom hook testing
grep -r "renderHook" src/ | grep -q "test" && echo "✅ Custom hooks tested" || exit 1

# 4. Async testing patterns
ASYNC_COUNT=$(grep -r "findBy\|waitFor" src/ --include="*.test.tsx" | wc -l)
[ $ASYNC_COUNT -ge 3 ] && echo "✅ $ASYNC_COUNT async test patterns" || exit 1

# 5. README documents test organization
grep -q "test files" README.md && echo "✅ README documents tests" || exit 1

# 6. Run tests to ensure they pass
npm test -- --run && echo "✅ All tests pass" || exit 1

echo "=== L2 Verification: PASS ==="
```

**Quantitative Metrics** (15 min):
- Test count: ≥10 component tests
- Coverage %: Run `npm test -- --coverage` and extract coverage % (target: ≥50%)
- Async pattern usage: Count `waitFor`, `findBy` instances (target: ≥3)
- Test pass rate: 100% tests passing (target: 100%)

**Qualitative Assessment** (30 min):
- Pattern consistency: Do tests follow React Testing Library best practices? (query priority, user-centric assertions)
- Integration quality: Do tests integrate with other SAPs effectively? (mocked API calls, provider wrappers)
- Documentation completeness: Does README explain test organization clearly?

**Total Time**: 65 min (1 hour)
**GO/NO-GO Threshold**: All automated checks pass + coverage ≥50% + pattern consistency ≥4/5

---

### 5.3 L3 (Active) Verification Plan

**Goal**: Verify best practices adopted and systematic usage.

**Automated Checks** (30 min):
```bash
#!/bin/bash
# verify-l3.sh - SAP-023 React State Management example

echo "=== L3 (Active) Verification: SAP-023 React State Management ==="

# 1. Clear separation of state layers
grep -r "useThemeStore\|useUserStore" src/ | wc -l | xargs -I {} echo "✅ {} Zustand usage instances"
grep -r "useQuery\|useMutation" src/ | wc -l | xargs -I {} echo "✅ {} TanStack Query instances"

# 2. Zustand persistence
grep -q "persist" src/stores/ && echo "✅ Persistence middleware configured" || exit 1

# 3. TanStack Query mutations with optimistic updates
grep -r "useMutation" src/ | grep -q "onMutate\|onSuccess" && echo "✅ Mutations configured" || exit 1

# 4. DevTools configured
grep -q "ReactQueryDevtools\|Redux DevTools" src/ && echo "✅ DevTools configured" || exit 1

# 5. Performance optimization (selectors, React.memo)
OPTIMIZATION_COUNT=$(grep -r "useCallback\|useMemo\|React.memo" src/ | wc -l)
[ $OPTIMIZATION_COUNT -ge 5 ] && echo "✅ $OPTIMIZATION_COUNT optimization instances" || exit 1

# 6. AGENTS.md documents patterns
test -f AGENTS.md && grep -q "State Management" AGENTS.md && echo "✅ AGENTS.md updated" || exit 1

# 7. CI/CD runs tests
test -f .github/workflows/test.yml && echo "✅ CI/CD configured" || echo "⚠️ CI/CD missing"

echo "=== L3 Verification: PASS ==="
```

**Quantitative Metrics** (30 min):
- State separation score: Count Zustand/TanStack Query/Context/useState instances, verify appropriate usage
- Optimization count: ≥5 instances of useCallback/useMemo/React.memo
- AGENTS.md completeness: Check for decision tree, code examples, integration patterns (target: 80% of required sections)
- CI/CD green: Run CI/CD pipeline, verify all tests pass

**Qualitative Assessment** (60 min):
- Pattern quality: Are state layers separated correctly? (no server state in Zustand, no frequently-changing data in Context)
- AGENTS.md usefulness: Can Claude Code use AGENTS.md to adopt patterns effectively? (test by having Claude read AGENTS.md and implement new feature)
- Integration coherence: Do SAP-023 + SAP-020 + SAP-021 work well together?

**Total Time**: 2 hours
**GO/NO-GO Threshold**: All automated checks pass + AGENTS.md completeness ≥80% + pattern quality ≥4/5

---

### 5.4 L4 (Deep) Verification Plan

**Goal**: Verify optimization achieved and custom patterns developed.

**Automated Checks** (45 min):
```bash
#!/bin/bash
# verify-l4.sh - SAP-025 React Performance example

echo "=== L4 (Deep) Verification: SAP-025 React Performance ==="

# 1. Performance budget defined
grep -q "bundle.*size\|performance.*budget" README.md && echo "✅ Budget defined" || exit 1

# 2. Bundle size optimized
npm run build
BUNDLE_SIZE=$(du -k dist/assets/*.js | awk '{sum+=$1} END {print sum}')
[ $BUNDLE_SIZE -lt 300 ] && echo "✅ Bundle size: ${BUNDLE_SIZE}KB (target: <300KB)" || exit 1

# 3. React 18 concurrent features
CONCURRENT_COUNT=$(grep -r "useTransition\|useDeferredValue" src/ | wc -l)
[ $CONCURRENT_COUNT -ge 3 ] && echo "✅ $CONCURRENT_COUNT concurrent feature instances" || exit 1

# 4. Virtual scrolling
grep -r "react-window\|react-virtualized" src/ && echo "✅ Virtual scrolling implemented" || echo "⚠️ Virtual scrolling missing"

# 5. Web Vitals monitoring
grep -q "web-vitals" package.json && echo "✅ Web Vitals monitoring configured" || exit 1

# 6. AGENTS.md documents profiling workflow
grep -q "profiling.*workflow\|React DevTools Profiler" AGENTS.md && echo "✅ Profiling documented" || exit 1

echo "=== L4 Verification: PASS ==="
```

**Quantitative Metrics** (60 min):
- Bundle size: <300KB initial bundle (measure with `npm run build -- --analyze`)
- Performance improvement: Run Lighthouse, compare to baseline (target: +20% improvement)
- Concurrent feature usage: ≥3 instances of useTransition or useDeferredValue
- Web Vitals: Measure LCP, FID, CLS (target: LCP <2.5s, FID <100ms, CLS <0.1)

**Qualitative Assessment** (90 min):
- Optimization appropriateness: Are optimizations applied where needed (not premature)?
- Custom pattern quality: If custom utilities created, are they valuable or over-engineered?
- Metrics stability: Run performance tests 3x, verify results stable (low variance)
- AGENTS.md profiling workflow: Does documented workflow actually help identify bottlenecks?

**Total Time**: 3 hours
**GO/NO-GO Threshold**: Bundle size <300KB + Web Vitals meet targets + custom patterns ≥4/5 quality

---

### 5.5 L5 (Mature) Verification Plan

**Goal**: Verify SAP validated via SAP-027 dogfooding and ecosystem contribution.

**Automated Checks** (15 min):
```bash
#!/bin/bash
# verify-l5.sh - Generic SAP-027 validation check

echo "=== L5 (Mature) Verification: SAP-027 Dogfooding Validation ==="

# 1. SAP-027 pilot completed
test -f .chora/memory/events/dogfooding.jsonl && echo "✅ Dogfooding events logged" || exit 1

# 2. GO decision documented
grep -q "GO decision" inbox/coordination/*.jsonl && echo "✅ GO decision found" || exit 1

# 3. Ledger.md documents adoption
test -f docs/skilled-awareness/*/ledger.md && echo "✅ Ledger exists" || exit 1

# 4. Contributions to chora-base
# (Manual check: verify PR count, merged status)

echo "=== L5 Verification: Manual review required ==="
```

**Quantitative Metrics** (30 min):
- Time savings: Extract from dogfooding.jsonl (target: ≥5x vs manual approach)
- Satisfaction: Extract from pilot feedback (target: ≥4/5)
- Quality: Extract bug count from pilot (target: 0 critical bugs)
- ROI: Calculate break-even point (setup cost ÷ per-use savings)
- Contribution count: Count merged PRs to chora-base (target: ≥1)

**Qualitative Assessment** (60 min):
- Pilot decision rationale: Is GO decision justified by data?
- Ecosystem contribution quality: Are contributed improvements valuable?
- Pattern sharing effectiveness: Are patterns successfully used in 2+ projects?
- Mentoring impact: Has documentation/examples helped others adopt?

**Total Time**: 2 hours
**GO/NO-GO Threshold**: SAP-027 pilot GO decision + time savings ≥5x + satisfaction ≥4/5 + 0 critical bugs + ≥1 merged contribution

---

## 6. Prompt Sequences for Claude Code (Verification Repo)

### 6.1 Core Principle: Test Fast-Setup Workflow First

**The actual chora-base adoption path**:
- Users run fast-setup script: `python scripts/create-model-mcp-server.py`
- Result: Fully-configured project with chora-base infrastructure in 1-2 minutes
- Secondary workflow: Adding new SAPs to fast-setup generated project

**Verification approach**:
- Primary: Test that fast-setup creates working projects with pre-configured SAPs
- Secondary: Test adding new SAPs to fast-setup projects
- All verification scripts live externally (not in verification repo or generated projects)

---

### 6.2 Pre-Verification Setup (External - Not in Verification Repo)

**In chora-base repo** (or separate analysis repo), prepare:

1. **Define Target Level**: SAP-024 React Styling, L2 (Usage)
2. **Prepare Metrics Tracking** (external):
   ```bash
   # In chora-base or analysis repo
   mkdir -p .verification-analysis/sap-024-l2-run-001
   touch .verification-analysis/sap-024-l2-run-001/observations.md
   ```
3. **Set Timer**: Track total time from first prompt to completion
4. **Prepare Observation Template**: What to watch for during adoption

---

### 6.3 Primary Workflow: Fast-Setup Script Verification

**Context**: You're in chora-base-SAP-Verification repo with Claude Code. Testing the fast-setup script workflow.

#### Prompt 1: Use Fast-Setup Script to Create MCP Server Project

```
I want to create a new MCP server project using chora-base's fast-setup script.

The chora-base repository provides a fast-setup script that creates fully-configured
projects with pre-installed SAPs.

Please:
1. Clone the chora-base repository: https://github.com/liminalcommons/chora-base
2. Read the README to understand the fast-setup workflow
3. Run the fast-setup script to create a new MCP server project:
   python scripts/create-model-mcp-server.py \
     --name "Verification Test Server" \
     --namespace verification-test \
     --output ./verification-projects/test-server-001

I want to verify the generated project has all the documented SAP configurations.
```

**What to observe** (externally):
- Does Claude successfully find and clone chora-base?
- Can Claude locate the fast-setup script?
- Does the script run without errors?
- Time to complete project creation (target: <5 minutes)
- Are there any blockers during script execution?

---

#### Prompt 2: Navigate to Generated Project and Verify Structure

```
Great! Now let's navigate to the generated project and verify it was created successfully.

Please:
1. Navigate to ./verification-projects/test-server-001
2. List the directory structure (show key files and folders)
3. Read the README.md to understand what was generated
4. List any SAP-related documentation (check for AGENTS.md, docs/skilled-awareness/)
5. Show me the package.json dependencies

I want to understand what SAPs are pre-configured in this generated project.
```

**What to observe**:
- Does the generated project exist at expected location?
- Is the project structure complete?
- Are SAP documentation files present?
- Time to complete navigation (target: <2 minutes)

---

#### Prompt 3: Identify Pre-Configured SAPs

```
Let's identify which SAPs are pre-configured in this generated project.

Please:
1. Check if there's a sap-catalog.json or similar SAP registry
2. Read AGENTS.md (if present) to see documented SAP patterns
3. Look for SAP-specific config files:
   - Testing: vitest.config.ts, playwright.config.ts
   - Linting: .eslintrc.js, .prettierrc
   - CI/CD: .github/workflows/
   - Docker: Dockerfile, docker-compose.yml
4. List all SAPs you can identify with their apparent maturity levels

Based on what you find, tell me which SAPs appear to be included and at what level.
```

**What to observe**:
- Can Claude identify pre-configured SAPs from project structure?
- Are SAPs documented in AGENTS.md or sap-catalog.json?
- Time to identify SAPs (target: <5 minutes)
- Accuracy of SAP identification

---

#### Prompt 4: Verify SAP-000 (SAP Framework) Configuration

```
Let's verify that SAP-000 (SAP Framework) is properly configured.

Check for:
1. SAP registry file (sap-catalog.json or .sap/registry/)
2. SAP documentation structure (docs/skilled-awareness/)
3. SAP templates (.sap/templates/)
4. Validation tooling (scripts for SAP verification)

Tell me what you find and whether SAP-000 appears to be at L1, L2, or L3 level.
```

**What to observe**:
- Is SAP-000 properly configured?
- What maturity level appears to be achieved?
- Time to verify (target: <5 minutes)

---

#### Prompt 5: Verify Testing Configuration (SAP-021)

```
Let's verify the testing setup in this generated project.

Please:
1. Check for test configuration files (vitest.config.ts, jest.config.js, etc.)
2. Look for example tests in the codebase
3. Run the test command (npm test or equivalent) and show results
4. Check test coverage configuration

Based on what you find, tell me:
- Is testing configured (L1)?
- Are there multiple tests (L2)?
- What's the test coverage? (L3 target: ≥70%)
```

**What to observe**:
- Does testing framework exist and work?
- Are tests pre-written or just configured?
- Do tests pass?
- Time to verify and run tests (target: <5 minutes)

---

#### Prompt 6: Verify CI/CD Configuration (SAP-005)

```
Let's check if CI/CD is configured in the generated project.

Please:
1. Look for .github/workflows/ directory
2. List any GitHub Actions workflow files
3. Read the workflow files to understand what they do
4. Check if there's a Justfile with CI/CD commands

Tell me what CI/CD patterns are configured and what maturity level they represent.
```

**What to observe**:
- Is CI/CD pre-configured?
- What workflows exist (test, lint, build, deploy)?
- Time to verify (target: <5 minutes)

---

#### Prompt 7: Run Project Build and Tests

```
Let's verify the generated project actually works.

Please:
1. Install dependencies (npm install or equivalent)
2. Run linting (npm run lint)
3. Run tests (npm test)
4. Run build (npm run build)
5. Show me any errors or warnings

I want to confirm the project is production-ready out-of-the-box.
```

**What to observe**:
- Does dependency installation work?
- Do linting, testing, and building all succeed?
- Any errors or warnings?
- Total time to verify project works (target: <10 minutes)
- Quality of error messages (if any)

---

#### Prompt 8: Comprehensive SAP Maturity Assessment

```
Now let's do a comprehensive assessment of SAP maturity levels in this project.

For each SAP you identified earlier, assess the maturity level (L1-L5) by checking:

**SAP-000 (SAP Framework)**:
- L1: Registry exists, validation tooling present
- L2: Multiple SAPs documented, templates available
- L3: AGENTS.md documents SAP patterns

**SAP-005 (CI/CD)**:
- L1: GitHub Actions configured
- L2: Multiple workflows (test, lint, build)
- L3: Deployment workflow, quality gates

**SAP-021 (Testing)**:
- L1: Test framework configured, ≥1 test exists
- L2: ≥10 tests, coverage configured
- L3: ≥70% coverage, AGENTS.md documents testing patterns

For each SAP, provide:
1. Identified maturity level (L1-L5)
2. Evidence (file paths, counts, configurations)
3. Any gaps compared to documented criteria
```

**What to observe**:
- Accuracy of maturity assessment
- Does Claude reference SAP documentation criteria?
- Time to complete assessment (target: <15 minutes)

---

#### Prompt 9: Fast-Setup Workflow Feedback

```
Now let's evaluate the fast-setup workflow itself.

Please tell me:
1. How long did the entire process take (from running script to verifying project)?
2. Did the fast-setup script work without errors?
3. Were any manual interventions needed after project creation?
4. Rate the out-of-the-box project quality (1-5):
   - Completeness (all expected files present)
   - Correctness (tests pass, linting passes, builds successfully)
   - Documentation quality (README clarity, AGENTS.md usefulness)
5. Would you recommend this fast-setup workflow to new chora-base adopters?

Overall satisfaction rating (1-5):
```

**What to observe**:
- Claude's perception of fast-setup quality
- Any pain points or friction
- Satisfaction with generated project
- Recommendation likelihood

---

### 6.4 External Verification (After Fast-Setup Prompts Complete)

**From chora-base or external analysis repo**, run verification checks on the generated project:

```bash
# Navigate to generated project
cd /path/to/chora-base-SAP-Verification/verification-projects/test-server-001

# Run automated checks (from external analysis repo)
bash ~/chora-base/.verification-analysis/scripts/verify-fast-setup-project.sh

# Example automated checks:
# 1. Check project was created
test -d . && echo "✅ Project directory exists"

# 2. Check SAP registry
test -f sap-catalog.json && echo "✅ SAP catalog present"

# 3. Check AGENTS.md
test -f AGENTS.md && echo "✅ AGENTS.md present"

# 4. Count pre-configured SAPs
grep -c '"id": "SAP-' sap-catalog.json

# 5. Verify tests pass
npm test && echo "✅ All tests pass"

# 6. Verify linting passes
npm run lint && echo "✅ Linting passes"

# 7. Verify build succeeds
npm run build && echo "✅ Build succeeds"
```

**Collect metrics**:
```json
{
  "workflow": "fast-setup",
  "script_execution_time_seconds": 120,
  "total_verification_time_minutes": 35,
  "project_created_successfully": true,
  "saps_pre_configured_count": 8,
  "saps_identified": [
    {"id": "SAP-000", "name": "sap-framework", "level": "L2"},
    {"id": "SAP-001", "name": "inbox", "level": "L1"},
    {"id": "SAP-005", "name": "ci-cd-workflows", "level": "L2"},
    {"id": "SAP-010", "name": "memory-system", "level": "L1"},
    {"id": "SAP-011", "name": "docker-operations", "level": "L2"},
    {"id": "SAP-015", "name": "task-tracking", "level": "L1"}
  ],
  "tests_pass": true,
  "linting_pass": true,
  "build_success": true,
  "blockers": [],
  "satisfaction": 5,
  "recommendation": true,
  "fast_setup_quality_rating": {
    "completeness": 5,
    "correctness": 5,
    "documentation": 4.5
  }
}
```

---

### 6.5 Secondary Workflow: Incremental SAP Adoption to Fast-Setup Project

**Context**: You have a fast-setup generated project. Now testing adding a NEW SAP that wasn't pre-configured.

**Example: Adding SAP-024 React Styling to a Fast-Setup Generated Project**

#### Prompt 1: Identify SAP Documentation in Fast-Setup Project

```
I have a project generated by chora-base's fast-setup script.

I want to add SAP-024 React Styling (Tailwind CSS) to this project.

Please:
1. Check if this project already has chora-base documentation (docs/skilled-awareness/)
2. Look for a local copy of SAP-024 documentation
3. If not present, visit chora-base repository to find SAP-024 documentation:
   https://github.com/liminalcommons/chora-base
4. Read the SAP-024 adoption-blueprint.md
5. Tell me what prerequisites are needed and summarize L1 and L2 adoption steps
```

**What to observe**:
- Does the fast-setup project include chora-base documentation?
- Can Claude find SAP documentation locally or remotely?
- Time to locate documentation (target: <5 minutes)

---

#### Prompt 2: Check for Prerequisites

```
Before adopting SAP-024, let's verify prerequisites are met.

SAP-024 requires:
- SAP-020 React Foundation (React + TypeScript + Vite)

Please check if this fast-setup project has SAP-020 configured:
1. Check for React dependencies in package.json
2. Check for Vite configuration (vite.config.ts)
3. Check for TypeScript configuration (tsconfig.json)

Are we ready to adopt SAP-024, or do we need to set up prerequisites first?
```

**What to observe**:
- Does Claude correctly identify prerequisites?
- Are prerequisites already met (from fast-setup)?
- Time to verify (target: <3 minutes)

---

#### Prompt 3: Adopt SAP-024 at L1 (Configured)

```
Great! Let's adopt SAP-024 React Styling at L1 (Configured) level.

Follow the SAP-024 adoption guide and implement the L1 requirements:
1. Install Tailwind CSS and dependencies
2. Create tailwind.config.ts with basic design tokens
3. Configure PostCSS (postcss.config.js)
4. Add Tailwind directives to global CSS
5. Create 5+ components using Tailwind utilities
6. Update README to document SAP-024 adoption

Follow the adoption guide step-by-step.
```

**What to observe**:
- Does adoption work smoothly in fast-setup project?
- Time to reach L1 (target: <1 hour)
- Any conflicts with existing fast-setup configuration?
- Does Claude follow adoption-blueprint.md accurately?

---

#### Prompt 4: Verify L1 Achievement

```
Let's verify we've achieved L1 (Configured) for SAP-024.

Check against SAP-024 L1 criteria:
1. Tailwind CSS installed and configured
2. tailwind.config.ts with basic design tokens (colors, spacing, typography)
3. PostCSS configured with Tailwind and Autoprefixer
4. At least 5 components using Tailwind utilities
5. README documents SAP-024 styling approach

Provide a detailed verification report with evidence for each criterion.
```

**What to observe**:
- Self-verification accuracy
- Are all L1 criteria met?
- Time to verify (target: <5 minutes)

---

#### Prompt 5: Progress to L2 (Usage) - Optional

```
Excellent! Now let's progress to L2 (Usage) level.

Implement SAP-024 L2 requirements:
1. Comprehensive design tokens (extend colors, spacing, typography, shadows, border radius)
2. Configure dark mode with class-based strategy
3. Install and configure Tailwind plugins (forms, typography, aspect-ratio)
4. Implement responsive design with mobile-first breakpoints
5. Define custom utilities in Tailwind config
6. Create 20+ components using Tailwind utilities
7. Update README with design tokens and responsive patterns

Target completion time: 2 hours
```

**What to observe**:
- Time to reach L2
- Quality of implementation
- Integration with fast-setup project

---

#### Prompt 6: Incremental Adoption Feedback

```
Now let's evaluate the incremental SAP adoption experience.

Please tell me:
1. How long did SAP-024 L1 adoption take?
2. Did the adoption guide (adoption-blueprint.md) work smoothly?
3. Were there any conflicts with the fast-setup generated project structure?
4. Did you need to reference chora-base repository, or was local documentation sufficient?
5. Rate the adoption experience (1-5):
   - Documentation clarity
   - Integration smoothness (with fast-setup project)
   - Time efficiency
6. Would you recommend this incremental adoption approach?

Overall satisfaction rating (1-5):
```

**What to observe**:
- Adoption time vs expected time
- Blockers or friction points
- Integration quality with fast-setup project
- Documentation sufficiency

---

### 6.6 Generic Prompt Template: Fast-Setup Workflow

For rapid verification of fast-setup generated projects.

**Phase 1: Create Project with Fast-Setup**
```
I want to create a new project using chora-base's fast-setup script.

chora-base repository: https://github.com/liminalcommons/chora-base

Please:
1. Clone the chora-base repository
2. Read the README to understand the fast-setup workflow
3. Run the fast-setup script:
   python scripts/create-model-mcp-server.py \
     --name "{Project Name}" \
     --namespace {namespace} \
     --output ./verification-projects/{project-dir}

I want to verify the generated project meets documented quality standards.
```

**Phase 2: Verify Generated Project Structure**
```
Please navigate to the generated project and verify:
1. Project directory structure (list key files and folders)
2. README.md content (what was generated?)
3. SAP documentation presence (AGENTS.md, docs/skilled-awareness/)
4. Package dependencies (show package.json)
5. Pre-configured SAPs (list from sap-catalog.json or AGENTS.md)

Tell me what SAPs are pre-configured and at what apparent maturity levels.
```

**Phase 3: Verify Pre-Configured SAP Maturity**
```
For each pre-configured SAP, assess the maturity level (L1-L5):

For each SAP you identified, check:
1. Configuration files present
2. Usage examples exist
3. Tests exist and pass
4. Documentation in README/AGENTS.md
5. CI/CD integration (if applicable)

Provide:
- SAP ID and name
- Identified maturity level (L1-L5)
- Evidence (file paths, counts, configurations)
- Gaps (if any) compared to documented criteria
```

**Phase 4: Run Project Verification**
```
Verify the generated project actually works:
1. Install dependencies (npm install or equivalent)
2. Run linting (npm run lint)
3. Run tests (npm test)
4. Run build (npm run build)
5. Show any errors or warnings

Report:
- Did all commands succeed?
- Total time to verify
- Any blockers or issues
```

**Phase 5: Fast-Setup Workflow Feedback**
```
Evaluate the fast-setup workflow:
1. How long did project creation take? (script execution time)
2. How long did verification take? (total time)
3. Did the script work without errors?
4. Were manual interventions needed?
5. Rate out-of-the-box quality (1-5):
   - Completeness (all expected files)
   - Correctness (tests pass, lint passes, builds)
   - Documentation (README/AGENTS.md clarity)
6. Would you recommend fast-setup to new adopters?

Overall satisfaction rating (1-5):
```

**Variables**:
- `{Project Name}`: "Verification Test Server", "My MCP Server", etc.
- `{namespace}`: verification-test, my-namespace, etc.
- `{project-dir}`: test-server-001, my-project, etc.

---

### 6.7 Observation Checklist (External - During Verification)

**Track these externally** while Claude Code works:

**A. Fast-Setup Workflow Observations**

1. **Script Execution Phase**:
   - [ ] Script execution start time logged
   - [ ] Did Claude successfully find and clone chora-base?
   - [ ] Did Claude locate the fast-setup script?
   - [ ] Did the script run without errors?
   - [ ] Script execution time (target: <3 minutes)
   - [ ] Any errors or warnings during project creation?
   - [ ] Was output directory created successfully?

2. **Generated Project Verification Phase**:
   - [ ] Time to navigate to generated project
   - [ ] Is project structure complete?
   - [ ] Are all expected files present (README, package.json, config files)?
   - [ ] Does README clearly explain what was generated?
   - [ ] Is AGENTS.md present and populated?
   - [ ] Time to verify project structure (target: <5 minutes)

3. **SAP Identification Phase**:
   - [ ] Can Claude identify pre-configured SAPs?
   - [ ] Is sap-catalog.json or SAP registry present?
   - [ ] Are SAPs documented in AGENTS.md?
   - [ ] Number of SAPs pre-configured (expected: 6-10)
   - [ ] Time to identify SAPs (target: <5 minutes)
   - [ ] Accuracy of maturity level assessment

4. **Project Functionality Verification**:
   - [ ] Dependency installation successful? (npm install)
   - [ ] Linting passes? (npm run lint)
   - [ ] Tests pass? (npm test)
   - [ ] Build succeeds? (npm run build)
   - [ ] Any errors or warnings during verification?
   - [ ] Time to verify functionality (target: <10 minutes)

5. **Time Metrics**:
   - [ ] Fast-setup script execution time
   - [ ] Project structure verification time
   - [ ] SAP identification time
   - [ ] Functionality verification time (install, lint, test, build)
   - [ ] Total time (script start → verification complete)
   - [ ] Target total time: <30 minutes

6. **Quality Observations**:
   - [ ] Project completeness (all expected files present)
   - [ ] Project correctness (tests pass, lint passes, builds)
   - [ ] Documentation quality (README clarity, AGENTS.md usefulness)
   - [ ] SAP configuration accuracy (do maturity levels match documentation?)
   - [ ] Integration quality (do SAPs work together?)

7. **Blocker/Friction Log**:
   - [ ] Was chora-base repository easy to find?
   - [ ] Was fast-setup script discoverable from README?
   - [ ] Did script require any manual intervention?
   - [ ] Were there any dependency installation issues?
   - [ ] Were there any configuration errors in generated project?
   - [ ] Did tests/linting/building work out-of-the-box?

8. **Self-Assessment Accuracy**:
   - [ ] Did Claude accurately identify SAPs and maturity levels?
   - [ ] Did Claude correctly count files, tests, configurations?
   - [ ] Did Claude's assessment match external verification?
   - [ ] Were evidence and metrics provided (not just "yes, done")?

9. **Satisfaction Indicators**:
   - [ ] Did Claude express any confusion about fast-setup workflow?
   - [ ] Did Claude complete verification confidently?
   - [ ] Were there any quality warnings about generated project?
   - [ ] Did Claude's satisfaction rating seem justified?
   - [ ] Would Claude recommend fast-setup workflow?

---

**B. Incremental SAP Adoption Observations** (Secondary Workflow)

1. **SAP Documentation Discovery**:
   - [ ] Is SAP documentation included in fast-setup project?
   - [ ] Can Claude find documentation locally or needs to visit GitHub?
   - [ ] Time to locate SAP documentation (target: <5 minutes)
   - [ ] Documentation clarity and completeness

2. **Prerequisites Verification**:
   - [ ] Are prerequisites already met (from fast-setup)?
   - [ ] Does Claude correctly identify prerequisite SAPs?
   - [ ] Time to verify prerequisites (target: <3 minutes)

3. **Adoption Execution**:
   - [ ] Time to reach L1 (target: <1 hour)
   - [ ] Time to reach L2 (target: <2 hours additional)
   - [ ] Any conflicts with fast-setup configuration?
   - [ ] Quality of implementation

4. **Integration Quality**:
   - [ ] Does new SAP integrate smoothly with fast-setup project?
   - [ ] Any configuration conflicts?
   - [ ] Does incremental adoption match adoption-blueprint.md?

5. **Satisfaction Indicators**:
   - [ ] Adoption time vs expected time
   - [ ] Blockers or friction during incremental adoption
   - [ ] Documentation sufficiency (local vs remote)
   - [ ] Overall incremental adoption experience rating

---

## 7. External Verification Scripts (NOT in Verification Repo)

### 7.1 Directory Structure (External Analysis Repo or chora-base)

**IMPORTANT**: These scripts are NOT in the verification repo. They're in an external location (chora-base or separate analysis repo) used to analyze the verification repo AFTER Claude Code completes adoption.

```
chora-base/ (or separate analysis repo)
├── .verification-analysis/
│   ├── scripts/
│   │   ├── verify-l1-generic.sh      # Generic L1 checks (any SAP)
│   │   ├── verify-l2-generic.sh      # Generic L2 checks (any SAP)
│   │   ├── verify-l3-generic.sh      # Generic L3 checks (any SAP)
│   │   ├── verify-sap-024-l2.sh      # SAP-024 specific L2 checks
│   │   ├── verify-sap-021-l2.sh      # SAP-021 specific L2 checks
│   │   ├── calculate-metrics.py      # Quantitative analysis
│   │   └── generate-go-no-go.py      # Decision report
│   │
│   └── runs/
│       └── sap-024-l2-run-001/       # Specific verification run
│           ├── observations.md       # Manual observations during run
│           ├── metrics.json          # Collected metrics
│           ├── qualitative.md        # Qualitative assessment
│           └── go-no-go.md           # Final decision
│
└── README.md
```

---

### 7.2 Generic Verification Script Example

**File**: `.verification-analysis/scripts/verify-l2-generic.sh`

```bash
#!/bin/bash
# verify-l2-generic.sh - Generic L2 verification for any SAP
# Usage: bash verify-l2-generic.sh /path/to/verification-repo SAP-024

set -e

REPO_PATH=$1
SAP_ID=$2

echo "=== L2 Generic Verification: ${SAP_ID} ==="
echo "Analyzing: ${REPO_PATH}"
echo ""

cd "${REPO_PATH}"

# Generic L2 checks (applicable to all SAPs)
echo "--- Generic L2 Checks ---"

# 1. README documents SAP
if grep -q "${SAP_ID}" README.md; then
    echo "✅ README documents ${SAP_ID}"
else
    echo "❌ README missing ${SAP_ID} documentation"
    exit 1
fi

# 2. Project structure exists
if [ -d "src/" ]; then
    echo "✅ src/ directory exists"
else
    echo "❌ src/ directory missing"
    exit 1
fi

# 3. Dependencies installed (check package.json or pyproject.toml)
if [ -f "package.json" ] && [ -d "node_modules" ]; then
    echo "✅ Dependencies installed (npm)"
elif [ -f "pyproject.toml" ] && [ -d ".venv" ]; then
    echo "✅ Dependencies installed (python)"
else
    echo "⚠️  Dependencies may not be installed"
fi

echo ""
echo "=== L2 Generic Verification: PASS ==="
echo "Next: Run SAP-specific verification script"
```

---

### 7.3 Metrics Calculation Script

```python
#!/usr/bin/env python3
# calculate-metrics.py - Quantitative metrics calculation

import json
import sys
from pathlib import Path
from datetime import datetime

def load_metrics(sap_id):
    """Load metrics.jsonl for given SAP"""
    metrics_file = Path(f".verification/{sap_id}/metrics.jsonl")
    if not metrics_file.exists():
        print(f"❌ Error: {metrics_file} not found")
        sys.exit(1)

    with open(metrics_file) as f:
        return [json.loads(line) for line in f]

def calculate_setup_time(events):
    """Calculate setup time from adoption_start to target level complete"""
    start = next((e for e in events if e['event'] == 'adoption_start'), None)
    # Find most recent level completion event
    completions = [e for e in events if 'complete' in e['event']]
    if not completions:
        return None
    latest = completions[-1]
    return latest.get('duration_hours')

def calculate_time_savings(setup_time, baseline_time):
    """Calculate time savings percentage"""
    savings = ((baseline_time - setup_time) / baseline_time) * 100
    return savings

def extract_usage_metrics(sap_id):
    """Extract usage metrics from verification checks"""
    # This would parse output from automated checks
    # For now, placeholder
    return {
        "usage_count": None,
        "integration_count": None
    }

def compare_to_thresholds(metrics, thresholds):
    """Compare actual metrics to thresholds"""
    results = {}
    for key, target in thresholds.items():
        actual = metrics.get(key)
        if actual is None:
            results[key] = {"status": "MISSING", "actual": None, "target": target}
        elif isinstance(target, dict):
            # Handle range thresholds (e.g., {"min": 20, "max": 100})
            min_val = target.get("min", float('-inf'))
            max_val = target.get("max", float('inf'))
            status = "PASS" if min_val <= actual <= max_val else "FAIL"
            results[key] = {"status": status, "actual": actual, "target": target}
        else:
            # Handle simple thresholds (e.g., setup_time <= 4)
            if key.endswith("_max"):
                status = "PASS" if actual <= target else "FAIL"
            elif key.endswith("_min"):
                status = "PASS" if actual >= target else "FAIL"
            else:
                # Default: actual >= target
                status = "PASS" if actual >= target else "FAIL"
            results[key] = {"status": status, "actual": actual, "target": target}
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python calculate-metrics.py SAP-ID")
        sys.exit(1)

    sap_id = sys.argv[1]

    # Load events
    events = load_metrics(sap_id)

    # Calculate metrics
    setup_time = calculate_setup_time(events)
    usage_metrics = extract_usage_metrics(sap_id)

    # Load thresholds
    thresholds_file = Path(f".verification/{sap_id}/thresholds.json")
    if not thresholds_file.exists():
        print(f"⚠️  Warning: {thresholds_file} not found, using defaults")
        thresholds = {
            "setup_time_max": 4,
            "usage_count_min": 10,
            "satisfaction_min": 4
        }
    else:
        with open(thresholds_file) as f:
            thresholds = json.load(f)

    # Combine metrics
    all_metrics = {
        "setup_time": setup_time,
        **usage_metrics
    }

    # Compare to thresholds
    results = compare_to_thresholds(all_metrics, thresholds)

    # Output results
    print(json.dumps({
        "sap_id": sap_id,
        "metrics": all_metrics,
        "thresholds": thresholds,
        "results": results,
        "overall_status": "PASS" if all(r['status'] == 'PASS' for r in results.values()) else "FAIL"
    }, indent=2))

if __name__ == "__main__":
    main()
```

---

### 7.4 GO/NO-GO Report Generation

```python
#!/usr/bin/env python3
# generate-report.py - GO/NO-GO decision report generation

import json
import sys
from pathlib import Path
from datetime import datetime

def load_results(sap_id):
    """Load verification results"""
    quantitative = Path(f".verification/{sap_id}/quantitative-results.json")
    qualitative = Path(f".verification/{sap_id}/qualitative-review.md")
    satisfaction = Path(f".verification/{sap_id}/satisfaction.md")

    results = {}

    if quantitative.exists():
        with open(quantitative) as f:
            results['quantitative'] = json.load(f)

    if qualitative.exists():
        with open(qualitative) as f:
            results['qualitative'] = f.read()

    if satisfaction.exists():
        with open(satisfaction) as f:
            results['satisfaction'] = f.read()

    return results

def make_decision(results):
    """Apply GO/NO-GO framework"""
    quant = results.get('quantitative', {})

    # Check if all quantitative metrics passed
    quant_status = quant.get('overall_status')
    if quant_status != 'PASS':
        return {
            "decision": "NO-GO",
            "rationale": "Quantitative thresholds not met",
            "blockers": [r for r in quant.get('results', {}).values() if r['status'] != 'PASS']
        }

    # For GO decision, require qualitative review (manual)
    if 'qualitative' not in results:
        return {
            "decision": "PENDING",
            "rationale": "Qualitative assessment not completed",
            "blockers": []
        }

    # If both passed, default to GO (manual override possible)
    return {
        "decision": "GO",
        "rationale": "All quantitative thresholds met, qualitative assessment completed",
        "blockers": []
    }

def generate_markdown_report(sap_id, sap_name, target_level, results, decision):
    """Generate GO/NO-GO report in markdown"""
    template = f"""# {sap_name} - L{target_level} Verification GO/NO-GO Decision

**Verification Date**: {datetime.now().strftime('%Y-%m-%d')}
**SAP ID**: {sap_id}
**Target Level**: L{target_level}
**Verifier**: Claude Code Agent (chora-base-SAP-Verification repo)

---

## Quantitative Results

"""

    # Add quantitative results table
    quant = results.get('quantitative', {})
    if 'results' in quant:
        template += "| Metric | Target | Actual | Status |\n"
        template += "|--------|--------|--------|--------|\n"
        for key, result in quant['results'].items():
            target = result.get('target', 'N/A')
            actual = result.get('actual', 'N/A')
            status = "✅ PASS" if result['status'] == 'PASS' else "❌ FAIL"
            template += f"| {key} | {target} | {actual} | {status} |\n"

    template += f"\n**Overall**: {quant.get('overall_status', 'UNKNOWN')}\n\n---\n\n"

    # Add qualitative results
    template += "## Qualitative Results\n\n"
    if 'qualitative' in results:
        template += results['qualitative']
    else:
        template += "⚠️ Qualitative assessment not completed\n"

    template += "\n\n---\n\n"

    # Add decision
    template += f"""## GO/NO-GO Decision

**Decision**: {"✅ GO" if decision['decision'] == 'GO' else "❌ NO-GO" if decision['decision'] == 'NO-GO' else "⏸️ PENDING"}

**Rationale**:
{decision['rationale']}

"""

    if decision['blockers']:
        template += "**Blockers**:\n"
        for blocker in decision['blockers']:
            template += f"- {blocker}\n"

    template += f"""
---

**Signed**: Claude Code Agent
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Next Verification**: L{target_level + 1} - Target date TBD
"""

    return template

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate-report.py SAP-ID SAP-NAME TARGET-LEVEL")
        sys.exit(1)

    sap_id = sys.argv[1]
    sap_name = sys.argv[2]
    target_level = int(sys.argv[3])

    # Load results
    results = load_results(sap_id)

    # Make decision
    decision = make_decision(results)

    # Generate report
    report = generate_markdown_report(sap_id, sap_name, target_level, results, decision)

    # Save report
    output_file = Path(f".verification/{sap_id}/go-no-go-decision.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"✅ GO/NO-GO report generated: {output_file}")
    print(f"Decision: {decision['decision']}")

if __name__ == "__main__":
    main()
```

---

## 8. Integration with chora-base

### 8.1 Verification Results Feedback Loop

**Workflow**:
```
1. Run verification in chora-base-SAP-Verification repo
2. Generate GO/NO-GO decision report
3. Open issue in chora-base with verification results
4. Chora-base maintainers review and refine SAP if needed
5. Update SAP ledger.md with verification metrics
```

**Issue Template**:
```markdown
**Title**: [Verification] SAP-024 React Styling - L2 Verification Results

**Labels**: verification, sap-024, L2

**Body**:

## Verification Summary

**SAP**: SAP-024 React Styling
**Level**: L2 (Usage)
**Decision**: ✅ GO
**Date**: 2025-11-07

---

## Key Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Setup Time | ≤4h | 2.25h | ✅ |
| Components Styled | ≥20 | 24 | ✅ |
| Satisfaction | ≥4/5 | 4.5/5 | ✅ |

---

## Recommendations

1. **Documentation Improvement**: Clarify dark mode is L3 feature (not L2) in adoption-blueprint.md
2. **AGENTS.md Addition**: Add troubleshooting section for inline styles anti-pattern

---

## Full Report

See: https://github.com/liminalcommons/chora-base-SAP-Verification/blob/main/.verification/SAP-024/go-no-go-decision.md
```

---

### 8.2 SAP Ledger.md Updates

After verification, update the SAP's `ledger.md` with verification results:

```markdown
## 11. Stakeholder Feedback

### Feedback Log

**Feedback 4**: 2025-11-07 - chora-base-SAP-Verification
- **Source**: L2 verification run (chora-base-SAP-Verification repo)
- **Feedback**: "SAP-024 adoption completed in 2.25 hours (44% under 4h target). All 24 components use Tailwind correctly. Satisfaction: 4.5/5. Minor issue: dark mode documentation unclear (mentioned for L2 but should be L3)."
- **Action**: Update adoption-blueprint.md to clarify dark mode is L3 feature. Add AGENTS.md troubleshooting section for inline styles anti-pattern.
- **Status**: Open (documentation update pending)
```

---

## 9. Success Criteria for Verification Methodology

### 9.1 Methodology Validation Metrics

**The verification methodology itself must be validated**. Success criteria:

1. **Reproducibility**: Same SAP verification produces consistent results (±10% variance)
2. **Coverage**: All L1-L5 maturity levels have clear verification methods
3. **Efficiency**: Verification time ≤50% of adoption time (e.g., L2 adoption 4h → verification 2h)
4. **Actionability**: GO/NO-GO decisions provide clear next steps (SAP refinement or ecosystem release)
5. **Adoption**: chora-base maintainers use verification results to improve SAPs

**How to measure**:
- Run same SAP verification 3x, compare results (reproducibility)
- Verify all SAPs L1-L5 have verification scripts (coverage)
- Track verification time vs adoption time (efficiency)
- Count actionable recommendations per verification (actionability)
- Track SAP refinements triggered by verification feedback (adoption)

---

### 9.2 Meta-Question: How Do We Know Verification Works?

**Answer**: Dogfood the verification methodology itself using SAP-027.

**Pilot Plan**:
1. **Setup** (Week 1): Run 3 SAP verifications (SAP-024, SAP-021, SAP-023) to establish baseline
2. **Execution** (Weeks 2-4): Verify 5 more SAPs (SAP-020, SAP-022, SAP-025, SAP-029, SAP-027)
3. **Analysis** (Week 5): Calculate reproducibility, coverage, efficiency, actionability metrics
4. **Decision** (Week 6): GO/NO-GO on verification methodology itself

**Success Thresholds**:
- Reproducibility: ±10% variance across 3 runs
- Coverage: 100% of L1-L5 levels have verification methods
- Efficiency: Verification time ≤50% of adoption time
- Actionability: ≥2 actionable recommendations per verification
- Adoption: ≥1 SAP refined based on verification feedback

---

## 10. Next Steps

### 10.1 Immediate Actions (This Week)

1. **Create chora-base-SAP-Verification Repository**:
   ```bash
   # On GitHub: Create new repo liminalcommons/chora-base-SAP-Verification
   git clone https://github.com/liminalcommons/chora-base-SAP-Verification.git
   cd chora-base-SAP-Verification
   ```

2. **Set Up Verification Infrastructure** (External to verification repo):
   ```bash
   # In chora-base or separate analysis repo
   mkdir -p .verification-analysis/{scripts,runs,templates}
   mkdir -p .verification-analysis/runs/fast-setup-run-001
   touch .verification-analysis/runs/fast-setup-run-001/observations.md
   ```

3. **Create First Verification Plan** (Fast-Setup Workflow as Pilot):
   - Define expected SAPs in fast-setup generated projects
   - Set thresholds (script time ≤3min, total verification time ≤30min, satisfaction ≥4/5)
   - Create observation checklist for fast-setup workflow

4. **Write Verification Scripts** (External - not in verification repo):
   - `verify-fast-setup-project.sh` (automated checks for generated projects)
   - `calculate-fast-setup-metrics.py` (quantitative metrics)
   - `generate-fast-setup-report.py` (GO/NO-GO decision)

---

### 10.2 Pilot Verification Run (Week 1)

1. **Run Fast-Setup Script to Generate Project**:
   - Clone chora-base repository in verification repo
   - Run fast-setup script:
     ```bash
     python scripts/create-model-mcp-server.py \
       --name "Verification Test Server" \
       --namespace verification-test \
       --output ./verification-projects/test-server-001
     ```
   - Log script execution time
   - Track any errors or blockers

2. **Verify Generated Project**:
   ```bash
   # Navigate to generated project
   cd verification-projects/test-server-001

   # Install dependencies
   npm install

   # Run verification commands
   npm run lint    # Should pass
   npm test        # Should pass
   npm run build   # Should succeed
   ```

3. **Run External Verification** (from chora-base or analysis repo):
   ```bash
   # Automated checks
   bash .verification-analysis/scripts/verify-fast-setup-project.sh \
     /path/to/verification-projects/test-server-001

   # Quantitative metrics
   python .verification-analysis/scripts/calculate-fast-setup-metrics.py \
     test-server-001

   # Qualitative assessment (manual)
   vim .verification-analysis/runs/fast-setup-run-001/qualitative-review.md

   # Generate GO/NO-GO report
   python .verification-analysis/scripts/generate-fast-setup-report.py \
     test-server-001 "Fast-Setup Generated MCP Server"
   ```

4. **Review and Iterate**:
   - Did fast-setup script work without errors?
   - Are pre-configured SAPs at documented maturity levels?
   - Do tests/linting/building work out-of-the-box?
   - Are thresholds appropriate?
   - Refine methodology based on learnings

---

### 10.3 Test Incremental SAP Adoption (Week 2)

**Secondary Workflow**: Test adding new SAPs to fast-setup generated projects.

1. **Use fast-setup generated project from Week 1**
2. **Adopt SAP-024 React Styling** (or another SAP not pre-configured):
   - Follow prompt sequence from Section 6.5
   - Track adoption time (target: L1 in <1 hour)
   - Log blockers and friction points
   - Collect satisfaction feedback

3. **Verify Incremental Adoption**:
   - Does new SAP integrate smoothly with fast-setup project?
   - Are there configuration conflicts?
   - Is documentation sufficient (local vs remote)?
   - Calculate metrics and generate report

**Goal**: Validate that fast-setup projects support incremental SAP adoption smoothly.

---

### 10.4 SAP-027 Dogfooding Validation (Weeks 5-6)

**Treat verification methodology as a new SAP** (conceptually):

1. **Analysis** (Week 5):
   - Calculate reproducibility (run same verification 3x)
   - Calculate efficiency (verification time / adoption time)
   - Count actionable recommendations
   - Measure chora-base adoption (SAP refinements triggered)

2. **Decision** (Week 6):
   - Apply GO/NO-GO framework to verification methodology itself
   - Document decision in `docs/project-docs/plans/sap-verification-methodology-decision.md`
   - If GO: Recommend verification methodology to chora-base ecosystem
   - If NO-GO: Refine methodology and re-pilot

---

## 11. Summary: Answering Your Question

**Your Question**: *"What methods can we devise to determine whether the expected results are achieved?"*

**Answer** (Refocused on Fast-Setup Workflow):

### 11.1 Define "Expected Results" for Fast-Setup Workflow

**Expected results = Evidence that fast-setup script creates production-ready projects with pre-configured SAPs at documented maturity levels.**

**Two Verification Workflows**:

**A. Primary (Fast-Setup Workflow)**:
- **Script Success**: Fast-setup script executes without errors in <3 minutes
- **Project Completeness**: All expected files present (README, AGENTS.md, configs, tests)
- **Project Correctness**: Tests pass, linting passes, build succeeds out-of-the-box
- **SAP Configuration**: Pre-configured SAPs are at documented maturity levels (e.g., SAP-000 at L2, SAP-005 at L2)
- **Documentation Quality**: README clearly explains what was generated, AGENTS.md documents patterns
- **Total Verification Time**: <30 minutes from script start to verification complete

**B. Secondary (Incremental SAP Adoption)**:
- **Adoption Success**: New SAPs can be added to fast-setup projects following adoption-blueprint.md
- **Integration Smoothness**: No configuration conflicts with fast-setup generated structure
- **Adoption Time**: L1 in <1 hour, L2 in <2 hours additional (same as documented)
- **Documentation Sufficiency**: Local or remote SAP documentation supports adoption

---

### 11.2 Verification Methods (3 Categories)

1. **Automated Checks** (Fast, Objective):
   - File existence, config validation, usage pattern counting, command success tests
   - Example: `grep -r "React.memo" src/ | wc -l` (count memoization usage)

2. **Quantitative Metrics** (Measurable, Comparable):
   - Time metrics (setup time, adoption time), quality metrics (error count, test coverage), usage metrics (pattern count, integration coverage), satisfaction metrics (1-5 rating)
   - Example: Setup time 2.25h vs 4h target = 44% under target = PASS

3. **Qualitative Assessments** (Subjective, High-Value):
   - Documentation quality, pattern quality, integration quality, developer experience
   - Example: "Pattern consistency: 4/5 - one component uses anti-pattern (inline styles)"

---

### 11.3 Verification Execution Protocol

**4-Phase Process** (aligned with SAP-027, adapted for fast-setup):

**A. Fast-Setup Workflow Verification**:

1. **Setup** (Before script execution): Define expected SAPs, create verification plan, set thresholds (script time ≤3min, total time ≤30min)
2. **Execution** (During verification): Run fast-setup script, navigate to generated project, verify structure, run tests/lint/build
3. **Analysis** (After verification): Run automated checks, calculate metrics (script time, SAP count, maturity levels), conduct qualitative review (documentation quality, project correctness)
4. **Decision** (GO/NO-GO): Compare to thresholds, document rationale, share with chora-base

**B. Incremental SAP Adoption Verification** (Secondary):

1. **Setup** (Before adoption): Identify SAP to add, define target level, set time thresholds
2. **Execution** (During adoption): Follow adoption-blueprint.md, track time, log blockers
3. **Analysis** (After adoption): Verify maturity level achieved, check integration with fast-setup project
4. **Decision** (GO/NO-GO): Compare to thresholds, assess integration smoothness

---

### 11.4 GO/NO-GO Framework

**Decision Criteria**:

**A. Fast-Setup Workflow**:
- **GO**: Script executes successfully + all tests/linting/building pass + total time ≤30min + SAPs at documented levels + satisfaction ≥4/5
- **CONDITIONAL NO-GO**: Script completes with warnings/errors + fixable blockers identified + fix effort <2 hours + verification can be re-run
- **NO-GO**: Script fails completely + critical architectural issues + fix effort >4 hours + satisfaction <3/5
- **PENDING**: Quantitative pass but qualitative review incomplete (manual review required)

**Thresholds Example** (Fast-Setup Workflow):
- Script execution time ≤3min (actual: 2min ✅)
- Total verification time ≤30min (actual: 25min ✅)
- Tests pass: Yes (actual: ✅)
- Linting passes: Yes (actual: ✅)
- Build succeeds: Yes (actual: ✅)
- SAPs pre-configured ≥6 (actual: 8 ✅)
- Satisfaction ≥4/5 (actual: 5/5 ✅)
- → Decision: GO

**B. Incremental SAP Adoption** (Secondary):
- **GO**: All maturity criteria met + adoption time meets target + no integration conflicts + satisfaction ≥4/5
- **NO-GO**: Critical criteria missed + adoption time >2x target + major integration conflicts + satisfaction <3/5

**Thresholds Example** (Incremental SAP-024 L1):
- Adoption time ≤1h (actual: 0.75h ✅)
- L1 criteria met: Yes (actual: 5/5 ✅)
- Integration conflicts: None (actual: ✅)
- Satisfaction ≥4/5 (actual: 4.5/5 ✅)
- → Decision: GO

**Real Case Study: Fast-Setup L1 Verification (2025-11-08)**

*First production verification run - resulted in CONDITIONAL NO-GO with successful fix-verify iteration*

**Initial Verification Results**:
- Script execution: ⚠️ Completed with errors (template rendering failure, Windows encoding)
- Verification time: 12 minutes (✅ under 30-minute threshold)
- SAPs configured: 8/8 (✅ meets threshold)
- Test files generated: 0 ❌ (expected ≥1)
- Workflows: ⚠️ Unsubstituted template variables
- Decision: **CONDITIONAL NO-GO** (4 fixable blockers, estimated 70-minute fix)

**Critical Blockers Identified**:
1. Template rendering error: `.gitignore` undefined variable `include_memory_system`
2. Missing test files: `tests/` directory empty, no example tests
3. Windows Unicode errors: Emoji characters cause encoding failures
4. Unsubstituted variables: CI/CD workflows contain `{{ package_name }}` patterns

**Fix-Verify Iteration (3 iterations, same-day)**:

**Iteration 1: Initial Fixes**
- Issues created: #2, #3, #4, #5 in chora-base repository
- Fixes implemented: 60 minutes (✅ under 2-hour threshold)
  - Fixed variable name in `.gitignore.template`
  - Created `test_server.py.template` with 23 test cases
  - Added UTF-8 encoding for Windows compatibility
  - Moved workflows to templates for Jinja2 rendering
- Release: v4.13.0
- Commits: [9dd95b5](https://github.com/liminalcommons/chora-base/commit/9dd95b5), [01f2956](https://github.com/liminalcommons/chora-base/commit/01f2956)

**Iteration 2: Re-Verification**
- Decision: CONDITIONAL NO-GO (75% improvement, 4 → 1 blocker)
- Result: 3 of 4 original blockers resolved ✅
- New blocker: Syntax error in `mcp__init__.py.template` (regression)
- Time: 8 minutes verification (33% faster than initial)
- Test files: 23 test cases generated (vs 0 initially)

**Iteration 3: Hot-Fix (Syntax)**
- Fix: Syntax error `dict[str, str}}` → `dict[str, str]]` (2 lines)
- Time: 2 minutes (100% estimate accuracy)
- Release: v4.13.1
- Commits: [6fbf944](https://github.com/liminalcommons/chora-base/commit/6fbf944), [f1f08cd](https://github.com/liminalcommons/chora-base/commit/f1f08cd)
- Status: All 5 blockers resolved (4 original + 1 regression)

**Iteration 4: Third Verification + Hot-Fix (Boolean)**
- Decision: CONDITIONAL NO-GO (83% progress, 5 of 6 resolved)
- Result: Syntax fix verified ✅, new boolean filter regression identified
- New blocker: `| lower` filter outputs `true` instead of `True` → NameError
- Time: 6 minutes verification + 2 minutes fix
- Fix: Remove `| lower` filter from 3 boolean variables, use Python booleans
- Release: [v4.14.1](https://github.com/liminalcommons/chora-base/releases/tag/v4.14.1)
- Commits: [d61a94d](https://github.com/liminalcommons/chora-base/commit/d61a94d), [89be4dd](https://github.com/liminalcommons/chora-base/commit/89be4dd)
- Status: All 6 code blockers resolved (4 original + 2 regressions)
- Expected: GO on fourth verification

**Iteration 5: Fourth Verification + Hot-Fix (Test Template)**
- Decision: CONDITIONAL NO-GO (code 100%, tests 39%)
- Result: All 6 code blockers verified ✅, new test template incompatibility identified
- New blocker: Test template tries to call `FunctionTool`/`FunctionResource` objects directly → TypeError
- Impact: 14 of 23 tests fail (61% failure rate) despite code working correctly
- Time: 5 minutes verification + 30 minutes fix
- Fix: Update 14 test functions to access underlying functions via `.fn` attribute
- Release: [v4.14.2](https://github.com/liminalcommons/chora-base/releases/tag/v4.14.2)
- Commits: [df9e1a2](https://github.com/liminalcommons/chora-base/commit/df9e1a2), [985d5b3](https://github.com/liminalcommons/chora-base/commit/985d5b3)
- Status: All 7 blockers resolved (6 code + 1 test)
- Expected: GO on fifth verification

**Lessons Learned**:
1. **CONDITIONAL NO-GO is valuable**: Distinguishes "needs minor fixes" from "fundamentally broken"
2. **Fix effort estimation works**: 70-minute estimate (actual: 60 min), 2-minute estimates (actual: 2 min each), 30-minute estimate (actual: 30 min)
3. **Fast iteration pays off**: 5 iterations in same day, momentum maintained
4. **Template testing needed**: Missing variables only caught during verification, not development
5. **Cross-platform testing essential**: Windows-specific issues require testing on Windows
6. **Regressions happen repeatedly**: 100% of fix iterations introduced new template errors (2 syntax + 1 test)
7. **Systemic issues need systemic solutions**: Automated template validation recommended over continued fix-regression cycles
8. **Framework-aware testing essential**: Tests must understand framework behavior (e.g., FastMCP decorators)
9. **Code working ≠ tests passing**: Fourth verification showed perfect code generation but failing tests

**Total Cycle**: 5 iterations, same-day resolution, 7 blockers resolved (6 code + 1 test), 3 regressions handled

---

### 11.5 Feedback Loop to chora-base

**Verification → Fast-Setup/SAP Refinement**:

**A. Fast-Setup Workflow Feedback**:

**1. Initial Verification**
- Run fast-setup verification in chora-base-SAP-Verification repo
- Generate GO/NO-GO/CONDITIONAL NO-GO report with:
  - Script execution issues (if any)
  - Pre-configured SAP maturity gaps
  - Documentation improvements needed
  - Generated project quality issues
  - **Fix effort estimation** for CONDITIONAL NO-GO

**2. Issue Creation**
- Open GitHub issues in chora-base for each critical blocker
- Include:
  - Error message and root cause
  - Expected behavior
  - Impact assessment (severity, user experience)
  - Proposed fix
  - Estimated effort

**3. Fix-Verify Iteration** (for CONDITIONAL NO-GO)
- Chora-base maintainers implement fixes:
  - Fast-setup script improvements
  - Pre-configured SAP configurations
  - Generated project templates
  - Cross-platform compatibility fixes
- Close GitHub issues with commit references
- Re-run verification to confirm fixes

**4. Iteration Cycle**
- **GO**: Verification complete, proceed to next maturity level or new SAP
- **CONDITIONAL NO-GO**: Execute fix-verify cycle (steps 2-3), aim for same-day resolution
- **NO-GO**: Major refactoring needed, schedule architecture review

**5. Lessons Capture**
- Update verification methodology with lessons learned
- Add real case studies to guide future verifications
- Refine GO/NO-GO thresholds based on experience

**B. Incremental SAP Adoption Feedback** (Secondary):
1. Run incremental adoption verification
2. Generate report with recommendations:
   - Adoption guide clarity improvements
   - Integration conflict resolutions
   - Documentation sufficiency gaps
3. Update SAP ledger.md with verification metrics
4. Refine SAP adoption guides based on feedback

---

## 12. Conclusion

This verification methodology provides **systematic, repeatable methods** to verify chora-base's actual user adoption path: the fast-setup workflow.

**Key Focus**: Test how chora-base users actually adopt the framework (via fast-setup script), not hypothetical manual SAP discovery.

**Two Verification Workflows**:

1. **Primary (Fast-Setup Workflow)**: Verify that fast-setup script creates production-ready projects with pre-configured SAPs at documented maturity levels
   - Script executes successfully in <3 minutes
   - Generated projects work out-of-the-box (tests pass, linting passes, build succeeds)
   - Pre-configured SAPs are at documented maturity levels
   - Total verification time <30 minutes

2. **Secondary (Incremental SAP Adoption)**: Verify that new SAPs can be added to fast-setup projects
   - Adoption guides (adoption-blueprint.md) work smoothly
   - No integration conflicts with fast-setup generated structure
   - Adoption time meets documented targets (L1 in <1 hour, L2 in <2 hours additional)

**Methodology Components**:
1. **Defining expected results** for fast-setup workflow and incremental adoption
2. **Categorizing verification methods** (automated, quantitative, qualitative)
3. **Creating prompt sequences** for Claude Code to test actual user workflows
4. **Establishing GO/NO-GO framework** aligned with SAP-027 dogfooding
5. **Creating feedback loop** to refine fast-setup script and SAP configurations

**Status**: ✅ **Methodology Validated** (2025-11-08)

The first production verification run successfully validated this methodology:
- Identified 4 critical blockers in fast-setup script (CONDITIONAL NO-GO)
- Executed fix-verify cycle with 60-minute turnaround
- All fixes verified and merged same-day
- Methodology proven effective for rapid quality improvement

**Key Validation Outcomes**:
1. **CONDITIONAL NO-GO works**: Distinguishes fixable issues from fundamental problems
2. **Fix effort estimation accurate**: Predicted 70 minutes, actual 60 minutes
3. **Same-day iteration feasible**: Fast feedback loop prevents context loss
4. **Issue-driven workflow effective**: GitHub issues provide clear tracking and accountability
5. **Real verification finds real bugs**: Template errors only caught through actual execution

**Lessons Learned from First Verification**:

1. **Cross-platform testing is essential**
   - Windows-specific Unicode errors require Windows testing
   - Don't assume Unix compatibility means Windows compatibility
   - Add Windows to CI/CD for script validation

2. **Template validation needed**
   - Undefined variables only caught at runtime
   - Consider pre-commit hooks for template variable validation
   - Test template rendering in CI/CD

3. **Out-of-box experience matters**
   - Missing test files = poor developer experience
   - Empty directories confuse new adopters
   - Include working examples for all configured SAPs

4. **Documentation is living**
   - Verification uncovered gaps in methodology itself
   - Real case studies more valuable than hypothetical examples
   - Update methodology based on actual experience

5. **Fast iteration compounds value**
   - 60-minute fix + same-day verification = momentum maintained
   - Delayed fixes lose context and motivation
   - Prioritize verification feedback for immediate action

**Next Steps**:
1. **Re-run L1 verification** with fixed script (expected: GO)
2. **Proceed to Week 2**: Incremental SAP adoption testing
3. **Expand verification coverage**: Test additional decision profiles (minimal, full)
4. **Automate verification**: Convert manual checks to CI/CD integration tests
