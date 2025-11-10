# Week 8 Verification Plan - Tier 3 Kickoff

**Created**: 2025-11-09
**Week**: 8 (Tier 3 Start)
**Target SAPs**: SAP-014 (mcp-server-development) L1 + SAP-020 (react-foundation) L1
**Estimated Time**: 5-6 hours
**Strategic Goal**: Begin Tier 3 (Technology-Specific) verification, validate MCP and React foundations

---

## Executive Summary

### Context from Week 7

**Week 7 Results**:
- ✅ SAP-011 (docker-operations) L1: CONDITIONAL GO (3/5 files, 1h 20min)
- ✅ SAP-013 (metrics-tracking) L3: GO (5/5 L3 criteria, 45min)
- ✅ First fully mature SAP (SAP-013 L1+L2+L3)
- ✅ Tier 2: 80% complete (4/5 SAPs)
- ⭐ Operational synergy pattern identified

**Campaign Progress**:
- Overall: 39% (12/31 SAPs + 1 L2 + 1 L3)
- Tier 1: 100% COMPLETE ✅
- Tier 2: 80% (likely complete, final SAP unclear)
- Tier 3: 0% → **Starting now**
- Total time: 24.25 hours across 7 weeks

### Week 8 Strategy

**Rationale for SAP Selection**:

1. **SAP-014 (mcp-server-development)** - First Tier 3 SAP
   - **Why First**: Fast-setup script already uses SAP-014 patterns (11 templates)
   - **Implicit Verification**: Week 1 verified MCP template generation works
   - **L1 Focus**: Verify incremental adoption of MCP templates to existing projects
   - **Time Estimate**: 2-2.5 hours
   - **Dependencies**: SAP-000, SAP-003, SAP-004, SAP-012 (all verified ✅)

2. **SAP-020 (react-foundation)** - Start React suite
   - **Why Second**: Foundation for 6 React SAPs (SAP-020 through SAP-025)
   - **Blocking Dependency**: Must verify before other React SAPs
   - **L1 Focus**: Verify Next.js 15 + TypeScript templates work
   - **Time Estimate**: 2.5-3 hours (includes Node.js environment setup)
   - **Dependencies**: SAP-000, SAP-003 (verified ✅)

**Why Not Other SAPs**:
- ❌ **SAP-015 (task-tracking/beads)**: Tier 5 advanced, not Tier 3
- ❌ **Tier 2 completion**: Unclear which SAP is the 5th (will clarify in Week 8)
- ❌ **L2/L3 enhancements**: Focus on Tier 3 breadth first

**Strategic Milestone**: Week 8 marks transition from **Development Support (Tier 2)** to **Technology-Specific (Tier 3)** SAPs.

---

## Pre-Flight Checks

### Environment Prerequisites

**Python Environment** (already verified):
```bash
python --version  # 3.11 or 3.12
pip --version
pytest --version
```

**Node.js Environment** (NEW for React SAPs):
```bash
node --version    # Should be 18.x, 20.x, or 22.x (LTS)
npm --version     # Should be 9.x or 10.x
npx --version     # Should be bundled with npm
```

**Docker** (verified Week 7):
```bash
docker --version
docker info  # Verify daemon running
```

**Git**:
```bash
git --version
git status  # Verify repo clean
```

### SAP-014 Pre-Flight Checks

**Verify MCP Templates Exist**:
```bash
ls -la docs/skilled-awareness/mcp-server-development/
# Expect: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

ls -la static-template/mcp-templates/
# Expect: 11 MCP templates (tool-*.py, resource-*.py, prompt-*.py, etc.)
```

**Verify Fast-Setup Integration** (implicit verification from Week 1):
```bash
grep -r "mcp-templates" scripts/create-model-mcp-server.py
# Should show template copying logic
```

**Expected Findings**:
- ✅ 11 MCP templates in `static-template/mcp-templates/`
- ✅ Templates copied to generated projects during fast-setup
- ❓ Incremental adoption workflow for adding MCP templates to existing projects

### SAP-020 Pre-Flight Checks

**Verify React Templates Exist**:
```bash
ls -la docs/skilled-awareness/react-foundation/
# Expect: capability-charter.md, protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

ls -la templates/react/
# Expect: nextjs-15-app-router/, vite-react-spa/, configs/
```

**Verify Node.js Installed**:
```bash
node --version
# If not installed: Download from https://nodejs.org/en (LTS version recommended)
# Windows: Use installer
# Linux/macOS: Use nvm (nvm install --lts)
```

**Expected Findings**:
- ✅ React templates exist (added in v4.3.0 release)
- ✅ Next.js 15 templates with App Router
- ✅ Vite templates for SPA projects
- ❓ TypeScript configs, ESM support

---

## Week 8 Target SAPs

### SAP-014: MCP Server Development

**Basic Info**:
- **Full Name**: MCP Server Development
- **Version**: 1.0.0
- **Status**: Active
- **Included by Default**: false
- **Size**: 234 KB
- **Category**: Incremental + Technology-Specific
- **Tier**: 3 (Technology-Specific)

**Capabilities**:
1. FastMCP patterns
2. 11 MCP templates (tool, resource, prompt definitions)
3. Tool definition patterns
4. Testing strategies
5. Deployment workflows

**Dependencies**:
- ✅ SAP-000 (sap-framework) - verified Week 1
- ✅ SAP-003 (project-bootstrap) - verified Week 1
- ✅ SAP-004 (testing-framework) - verified Week 1
- ✅ SAP-012 (development-lifecycle) - verified Week 5

**Artifacts to Verify**:
- [ ] capability-charter.md (defines what MCP server development provides)
- [ ] protocol-spec.md (MCP protocol patterns, FastMCP conventions)
- [ ] awareness-guide.md (CLAUDE.md section, AGENTS.md section)
- [ ] adoption-blueprint.md (L1 adoption steps)
- [ ] ledger.md (decision log, adoption history)
- [ ] mcp-conventions.md (MCP-specific naming, patterns)

**System Files**:
```
static-template/mcp-templates/
├── tool-basic.py
├── tool-file-operations.py
├── tool-api-integration.py
├── resource-static.py
├── resource-dynamic.py
├── prompt-basic.py
├── prompt-structured.py
├── example-mcp-server.py
├── example-mcp-server-advanced.py
├── testing-mcp-tools.py
└── deployment-mcp-server.md
```

**L1 Verification Criteria** (from adoption-blueprint.md):

1. **Criterion 1**: MCP templates accessible and documented
   - [ ] 11 templates present in `mcp-templates/`
   - [ ] Each template has clear header comments explaining purpose
   - [ ] Templates follow FastMCP patterns

2. **Criterion 2**: MCP conventions guide exists
   - [ ] `mcp-conventions.md` documents naming patterns
   - [ ] Tool naming: `<domain>_<action>_<object>` (e.g., `file_read_content`)
   - [ ] Resource naming: `<domain>://<path>` (e.g., `file://path/to/resource`)

3. **Criterion 3**: Integration with existing SAPs
   - [ ] Templates use SAP-004 (pytest) for testing
   - [ ] Templates follow SAP-012 (development-lifecycle) patterns
   - [ ] Templates integrate with project structure (SAP-003)

4. **Criterion 4**: Adoption blueprint provides clear L1 steps
   - [ ] Step-by-step guide for adding MCP templates
   - [ ] Copy commands clearly specified
   - [ ] Example usage included

5. **Criterion 5**: Awareness integration complete
   - [ ] CLAUDE.md section describes MCP capabilities
   - [ ] AGENTS.md section guides agent usage
   - [ ] Templates discoverable via justfile recipes (if applicable)

**Verification Workflow**:

**Phase 1: Pre-Existing Verification (Implicit)** (15 min)
- Review Week 1 fast-setup results (MCP templates in generated project)
- Confirm 11 templates present in generated project from Week 1
- Verify templates have correct Jinja2 variables ({{ project_name }}, etc.)

**Phase 2: Incremental Adoption Verification** (45 min)
- Use generated project from Week 7 (or create new minimal project)
- Follow adoption-blueprint.md L1 steps
- Copy MCP templates to project
- Verify templates render correctly
- Test basic MCP tool (e.g., `tool-basic.py`)

**Phase 3: Awareness Integration Verification** (30 min)
- Verify CLAUDE.md section exists and describes MCP patterns
- Verify AGENTS.md section guides agent MCP usage
- Check justfile recipes for MCP-related commands

**Phase 4: Cross-Validation with SAP-004, SAP-012** (30 min)
- Run pytest on MCP tool templates
- Verify MCP templates follow development-lifecycle patterns
- Test integration points:
  1. MCP tools use pytest fixtures
  2. MCP tools follow project structure
  3. MCP deployment docs reference CI/CD workflows

**Time Estimate**: 2-2.5 hours

**Success Criteria**:
- ✅ 5/5 L1 criteria met → **GO**
- ⚠️ 4/5 criteria met → **CONDITIONAL GO**
- ⚠️ 3/5 criteria met → **CONDITIONAL NO-GO**
- ❌ <3/5 criteria met → **NO-GO**

---

### SAP-020: React Project Foundation

**Basic Info**:
- **Full Name**: React Project Foundation
- **Version**: 1.0.0
- **Status**: Active
- **Included by Default**: false
- **Size**: 210 KB
- **Category**: Incremental + Technology-Specific
- **Tier**: 3 (Technology-Specific)

**Capabilities**:
1. Next.js 15 with App Router
2. TypeScript strict mode
3. Project structure (feature-based + layer-based)
4. Basic state management setup
5. 8-12 starter templates

**Dependencies**:
- ✅ SAP-000 (sap-framework) - verified Week 1
- ✅ SAP-003 (project-bootstrap) - verified Week 1

**Dependents** (blocks 6 React SAPs):
- ⏳ SAP-021 (react-testing)
- ⏳ SAP-022 (react-linting)
- ⏳ SAP-023 (react-state-management)
- ⏳ SAP-024 (react-styling)
- ⏳ SAP-025 (react-performance)
- ⏳ SAP-026 (react-accessibility)

**Artifacts to Verify**:
- [ ] capability-charter.md (defines React foundation scope)
- [ ] protocol-spec.md (Next.js 15 + TypeScript patterns)
- [ ] awareness-guide.md (CLAUDE.md section, AGENTS.md section)
- [ ] adoption-blueprint.md (L1 adoption steps)
- [ ] ledger.md (decision log, React ecosystem adoption history)

**System Files**:
```
templates/react/
├── nextjs-15-app-router/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── components/
│   │   └── lib/
│   ├── tsconfig.json
│   ├── next.config.ts
│   └── package.json
├── vite-react-spa/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── components/
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
└── configs/
    ├── tsconfig.base.json
    └── tsconfig.strict.json
```

**L1 Verification Criteria** (estimated from SAP scope):

1. **Criterion 1**: Next.js 15 template exists and builds
   - [ ] Template structure follows Next.js 15 App Router conventions
   - [ ] `app/layout.tsx` and `app/page.tsx` present
   - [ ] TypeScript configured (`tsconfig.json` with strict mode)
   - [ ] Builds successfully: `npm run build` (or equivalent)

2. **Criterion 2**: Vite React SPA template exists and builds
   - [ ] Template structure follows Vite conventions
   - [ ] `src/main.tsx` and `src/App.tsx` present
   - [ ] `vite.config.ts` configured for React
   - [ ] Builds successfully: `npm run build`

3. **Criterion 3**: TypeScript configs support strict mode
   - [ ] `tsconfig.strict.json` enforces strict type checking
   - [ ] Templates extend base TypeScript config
   - [ ] No TypeScript errors in template files

4. **Criterion 4**: Project structure patterns documented
   - [ ] Feature-based structure explained (domains/features)
   - [ ] Layer-based structure explained (components/lib/utils)
   - [ ] Examples included in templates

5. **Criterion 5**: Adoption blueprint provides clear L1 steps
   - [ ] Step-by-step guide for integrating React templates
   - [ ] Node.js version requirements specified (18.x, 20.x, 22.x)
   - [ ] npm install commands provided

**Verification Workflow**:

**Phase 1: Environment Setup** (30 min)
- Install Node.js (if not installed)
- Verify npm and npx versions
- Test basic Next.js creation: `npx create-next-app@latest test-nextjs`
- Test basic Vite creation: `npm create vite@latest test-vite -- --template react-ts`

**Phase 2: Template Verification** (60 min)
- Copy Next.js 15 template to test directory
- Install dependencies: `npm install`
- Run development server: `npm run dev`
- Verify TypeScript strict mode: `npm run type-check` (or tsc --noEmit)
- Build for production: `npm run build`
- Repeat for Vite template

**Phase 3: Adoption Blueprint Verification** (30 min)
- Follow adoption-blueprint.md L1 steps
- Verify steps match actual template structure
- Test incremental adoption (add React to existing project)

**Phase 4: Awareness Integration Verification** (30 min)
- Verify CLAUDE.md section describes React patterns
- Verify AGENTS.md section guides React development
- Check for React-specific justfile recipes

**Time Estimate**: 2.5-3 hours

**Success Criteria**:
- ✅ 5/5 L1 criteria met → **GO**
- ⚠️ 4/5 criteria met → **CONDITIONAL GO**
- ⚠️ 3/5 criteria met → **CONDITIONAL NO-GO**
- ❌ <3/5 criteria met → **NO-GO**

---

## Cross-Validation Plan

### SAP-014 ↔ SAP-020 Integration

**Integration Hypothesis**: MCP servers can serve React applications (e.g., MCP resource serving React components as prompts, MCP tools building React apps)

**Integration Points to Test**:

1. **MCP Tool for React Component Generation**
   - MCP tool that generates React components from templates
   - Uses SAP-020 templates as input
   - Tests both MCP and React foundations

2. **MCP Resource for React Documentation**
   - MCP resource serving React patterns from SAP-020
   - Tests resource patterns from SAP-014

3. **Unified Testing Strategy**
   - Both MCP and React use pytest (SAP-004)
   - React may also use Vitest (SAP-021, future)

4. **Deployment Patterns**
   - MCP servers and React apps both use Docker (SAP-011)
   - CI/CD workflows support both (SAP-005)

**Validation Steps**:
1. Create MCP tool that uses React templates
2. Test MCP tool with pytest
3. Verify React template renders correctly
4. Document integration pattern in cross-validation report

**Integration Quality Target**: ⭐⭐⭐ (3/5 - Moderate Synergy)
- Not as tight as SAP-010 ↔ SAP-013 (data flow)
- Not as tight as SAP-011 ↔ SAP-013 (operational)
- Complementary capabilities, shared infrastructure

**Time Estimate**: 1-1.5 hours

---

## Timeline and Milestones

### Day 1: SAP-014 Verification (2.5 hours)

**Morning** (1.5 hours):
- [ ] Run pre-flight checks for SAP-014
- [ ] Review Week 1 fast-setup results (MCP templates)
- [ ] Verify 11 MCP templates exist and have correct structure
- [ ] Read adoption-blueprint.md L1 steps

**Afternoon** (1 hour):
- [ ] Follow incremental adoption workflow
- [ ] Copy MCP templates to test project
- [ ] Test basic MCP tool (tool-basic.py)
- [ ] Run pytest on MCP templates

### Day 2: SAP-020 Verification (3 hours)

**Morning** (1.5 hours):
- [ ] Run pre-flight checks for SAP-020
- [ ] Install/verify Node.js environment
- [ ] Review React templates (Next.js 15, Vite)
- [ ] Read adoption-blueprint.md L1 steps

**Afternoon** (1.5 hours):
- [ ] Test Next.js 15 template (install, dev, build)
- [ ] Test Vite React template (install, dev, build)
- [ ] Verify TypeScript strict mode
- [ ] Document any issues or blockers

### Day 3: Cross-Validation and Reporting (1.5 hours)

**Morning** (1 hour):
- [ ] Test SAP-014 ↔ SAP-020 integration points
- [ ] Create MCP tool using React templates
- [ ] Document integration quality

**Afternoon** (30 min):
- [ ] Create WEEK_8_REPORT.md
- [ ] Update PROGRESS_SUMMARY.md
- [ ] Commit Week 8 artifacts

---

## Risks and Mitigation

### Risk 1: Node.js Not Installed

**Probability**: Medium (Windows environment may not have Node.js)
**Impact**: High (blocks SAP-020 verification)

**Mitigation**:
1. Check Node.js installation in pre-flight checks
2. If not installed, download from https://nodejs.org/en
3. Install LTS version (20.x recommended)
4. Verify installation: `node --version`, `npm --version`

**Contingency**: If Node.js installation fails, defer SAP-020 to Week 9 and substitute with SAP-015 (task-tracking/beads) which is Python-based.

### Risk 2: React Templates Don't Build

**Probability**: Medium (templates are new, may have issues)
**Impact**: Medium (CONDITIONAL GO instead of GO)

**Mitigation**:
1. Test templates in isolated environment first
2. Verify package.json dependencies are correct
3. Check for missing dependencies or version conflicts

**Contingency**: Document build issues in verification report, classify as CONDITIONAL GO if 4/5 criteria met.

### Risk 3: MCP Templates Missing from Fast-Setup

**Probability**: Low (Week 1 implicitly verified MCP templates work)
**Impact**: Medium (would require fixing fast-setup script)

**Mitigation**:
1. Review Week 1 verification results before starting
2. Confirm MCP templates in generated project from Week 1
3. If missing, check `create-model-mcp-server.py` template copying logic

**Contingency**: If MCP templates missing, this is a regression - file as blocker and fix before continuing.

### Risk 4: Time Overrun

**Probability**: Medium (React setup may take longer than estimated)
**Impact**: Low (can continue into Day 4)

**Mitigation**:
1. Start with pre-flight checks to identify blockers early
2. Prioritize SAP-014 (less risky) before SAP-020
3. Defer cross-validation if time is short

**Contingency**: If Week 8 exceeds 6 hours, split SAP-020 into Week 9 and add one more Tier 3 SAP.

---

## Success Metrics

### Completion Criteria

**Minimum Success** (Week 8 considered successful if):
- ✅ SAP-014 verified (GO or CONDITIONAL GO)
- ✅ SAP-020 verified (GO or CONDITIONAL GO)
- ✅ Cross-validation report created
- ✅ WEEK_8_REPORT.md published
- ✅ Tier 3: 0% → 29% (2/7 SAPs)

**Stretch Goals**:
- ✅ Both SAPs receive GO decisions (not CONDITIONAL GO)
- ✅ Integration quality ≥4/5 stars
- ✅ Time under 6 hours (efficiency target)
- ✅ Zero blockers requiring fast-setup script changes

### Campaign Progress Targets

**After Week 8**:
- Overall: 39% → 45% (14/31 SAPs)
- Tier 1: 100% (unchanged)
- Tier 2: 80% (unchanged)
- Tier 3: 0% → 29% (2/7 SAPs)
- Total Time: 24.25h → 29.25-30.25h (5-6h added)

**ROI Targets**:
- Time saved: ~8-10 hours (MCP templates + React setup automation)
- ROI: 150-180% (8-10h saved / 5-6h invested)
- Cumulative ROI: ~500% maintained

---

## Deliverables

### Required Artifacts

1. **SAP-014-VERIFICATION.md** (~600-800 lines)
   - Pre-flight check results
   - L1 criteria verification (5 criteria)
   - MCP template testing results
   - Awareness integration verification
   - Decision: GO/CONDITIONAL GO/CONDITIONAL NO-GO/NO-GO

2. **SAP-020-VERIFICATION.md** (~600-800 lines)
   - Environment setup results (Node.js installation)
   - Next.js 15 template verification
   - Vite template verification
   - TypeScript strict mode verification
   - Decision: GO/CONDITIONAL GO/CONDITIONAL NO-GO/NO-GO

3. **CROSS_VALIDATION.md** (~500-700 lines)
   - SAP-014 ↔ SAP-020 integration testing
   - 4 integration points verified
   - Integration quality rating (1-5 stars)
   - Integration patterns documented

4. **WEEK_8_REPORT.md** (~500-600 lines)
   - Executive summary
   - SAP-014 and SAP-020 results
   - Key discoveries and patterns
   - Time tracking and ROI
   - Tier 3 progress update

5. **PROGRESS_SUMMARY.md** (updates)
   - Add SAP-014 and SAP-020 to verified SAPs table
   - Update tier progress (Tier 3: 0% → 29%)
   - Add Week 8 timeline entry
   - Update time tracking table
   - Update decisions breakdown

### Optional Artifacts

1. **MCP-REACT-INTEGRATION-PATTERN.md** - Document MCP + React integration pattern
2. **NODE-SETUP-GUIDE.md** - Guide for setting up Node.js on Windows
3. **REACT-TEMPLATE-ISSUES.md** - Issues found in React templates (if any)

---

## Next Steps (Week 9)

**Week 9 Targets** (tentative):
- SAP-021 (react-testing) L1
- SAP-022 (react-linting) L1
- Continue Tier 3 React suite verification
- Target: Tier 3 → 57% (4/7 SAPs)

**Week 10 Targets** (tentative):
- SAP-023 (react-state-management) L1
- SAP-024 (react-styling) L1
- SAP-025 (react-performance) L1
- Complete Tier 3: 100% (7/7 SAPs)

**Week 11 Targets** (tentative):
- Begin Tier 4 (Ecosystem & Coordination)
- SAP-001 (inbox-coordination) L1
- SAP-017, SAP-018, SAP-019 (chora-compose suite)

---

## Conclusion

Week 8 marks a **strategic transition** from Development Support (Tier 2) to Technology-Specific (Tier 3) SAPs. By verifying SAP-014 (MCP) and SAP-020 (React), we establish foundations for:

1. **MCP Ecosystem**: Template-driven MCP server development
2. **React Ecosystem**: Modern React with Next.js 15 and TypeScript
3. **Integration Patterns**: MCP + React synergies

**Key Risks**: Node.js installation, React template build issues
**Key Opportunities**: First verification of non-Python technology stacks
**Expected Outcome**: 2 GO decisions, Tier 3 at 29%, campaign at 45%

---

**Created**: 2025-11-09
**Status**: Ready for Execution
**Next Action**: Run pre-flight checks for SAP-014 and SAP-020
