# Git Workflow Maintenance Schedule (SAP-051)

**Frequency**: Quarterly + As-Needed
**Owner**: Repository maintainer or team lead
**Time**: 30-60 minutes per quarter

---

## Quarterly Maintenance (Every 3 Months)

### Q1: Hook Updates & Validation

**When**: January, April, July, October (first week)

**Tasks**:
1. **Update hooks from upstream** (if using chora-base):
   ```bash
   cd chora-base
   git pull origin main
   cd ..
   just git-setup  # Re-install updated hooks
   ```

2. **Validate hooks still work**:
   ```bash
   just git-check
   # Test with dummy commit
   git commit --allow-empty -m "test: verify hooks working"
   ```

3. **Check for new Conventional Commits types**:
   ```bash
   # Review if team needs new types
   just git-config-show
   # Add if needed
   just git-config-custom "feat,fix,docs,new-type" "72" "false"
   ```

4. **Update git version** (if outdated):
   ```bash
   git --version
   # If <2.40, consider updating
   ```

---

### Q2: Team Compliance Review

**When**: February, May, August, November (mid-month)

**Tasks**:
1. **Check team adoption rate**:
   ```bash
   # Count conventional commits in last 3 months
   TOTAL=$(git log --since="3 months ago" --oneline | wc -l)
   VALID=$(git log --since="3 months ago" --grep="^(feat|fix|docs|refactor|test|chore|perf|ci|build|revert):" --oneline | wc -l)
   echo "Adoption rate: $(($VALID * 100 / $TOTAL))%"
   ```

2. **Identify non-compliant commits**:
   ```bash
   # Find commits without conventional format
   git log --since="3 months ago" --format="%h %s" | grep -vE "^[a-f0-9]+ (feat|fix|docs|refactor|test|chore|perf|ci|build|revert)[(:]"
   ```

3. **Review branch naming compliance**:
   ```bash
   # Check recent branches
   git branch -r --sort=-committerdate | head -20 | grep -vE "(feature|bugfix|hotfix|chore|docs|refactor|test)/"
   ```

4. **Team feedback collection**:
   - Survey: "Are git hooks helping or hindering?"
   - Pain points with current setup
   - Requests for new features/types

---

### Q3: Documentation Updates

**When**: March, June, September, December (end of month)

**Tasks**:
1. **Update CHANGELOG.md**:
   ```bash
   # Generate changelog for quarter
   just changelog --since="3 months ago" --output=CHANGELOG-q$(date +%q).md
   # Review and merge into main CHANGELOG.md
   ```

2. **Update onboarding docs** (if outdated):
   - Review [git-workflow-quickstart.md](git-workflow-quickstart.md)
   - Update examples if needed
   - Add new FAQ items from team questions

3. **Review and update SAP-051 artifacts**:
   - capability-charter.md: Update adoption metrics
   - ledger.md: Update ecosystem adoption status
   - adoption-blueprint.md: Add new tips/troubleshooting

4. **Generate team metrics**:
   ```bash
   # Save metrics for quarterly report
   echo "=== Q$(date +%q) Git Workflow Metrics ===" > metrics-q$(date +%q).txt
   git log --since="3 months ago" --format="%s" | grep -E "^(feat|fix|docs):" | wc -l >> metrics-q$(date +%q).txt
   ```

---

### Q4: CI/CD Review

**When**: Quarterly, after hook updates

**Tasks**:
1. **Review GitHub Actions runs**:
   - Check failure rate of git-validation workflow
   - Identify common validation failures
   - Update workflow if needed

2. **Update GitHub Actions dependencies**:
   ```yaml
   # In .github/workflows/git-validation.yml
   - uses: actions/checkout@v4  # Check for v5
   - uses: actions/setup-python@v4  # Check for v5
   ```

3. **Test workflow locally** (optional):
   ```bash
   # Install act (GitHub Actions local runner)
   # https://github.com/nektos/act
   act pull_request
   ```

4. **Review changelog generation**:
   - Verify changelog previews in PRs are working
   - Update changelog format if needed

---

## As-Needed Maintenance

### When: Git Version Update

**Trigger**: New git release with breaking changes or security updates

**Tasks**:
1. Review git release notes
2. Test hooks with new git version
3. Update minimum git version in docs if needed
4. Notify team of required git update

---

### When: Conventional Commits Spec Update

**Trigger**: New Conventional Commits specification release

**URL**: https://www.conventionalcommits.org/

**Tasks**:
1. Review spec changes
2. Update hooks to match new spec (if needed)
3. Update documentation with new examples
4. Announce to team

---

### When: Team Workflow Changes

**Trigger**: New project requirements, team growth, process changes

**Examples**:
- Adding new commit type: `just git-config-custom "feat,fix,docs,deploy" ...`
- Changing branch naming: Update pre-push hook
- New SAP/COORD integration: Update git-commit-template

**Tasks**:
1. Update git config or hooks
2. Test changes with pilot team
3. Update documentation
4. Roll out to full team
5. Provide training if needed

---

### When: Major Bug Found in Hooks

**Trigger**: Hook causing commits to fail incorrectly

**Tasks**:
1. **Immediate**: Disable problematic hook
   ```bash
   git config hooks.commit-msg-enabled false
   # Or hooks.pre-push-enabled false
   ```

2. **Debug**: Reproduce and identify root cause
   ```bash
   export GIT_WORKFLOW_DEBUG=true
   git commit --allow-empty -m "test: debug"
   ```

3. **Fix**: Update hook script
4. **Test**: Verify fix with test suite
   ```bash
   cd chora-base
   pytest tests/test_sap_051/ -v
   ```

5. **Deploy**: Re-enable and notify team
   ```bash
   just git-setup
   git config hooks.commit-msg-enabled true
   ```

---

## Monitoring & Alerts

### Key Metrics to Track

1. **Adoption Rate** (target: >90%):
   ```bash
   # Percentage of commits following Conventional Commits
   ```

2. **Hook Failure Rate** (target: <5%):
   ```bash
   # From CI/CD logs or team reports
   ```

3. **Time to First Commit** (for new team members):
   - Track in onboarding docs
   - Target: <10 minutes from setup to first valid commit

4. **Branch Naming Compliance** (target: 100%):
   ```bash
   # All feature branches follow convention
   ```

### Setting Up Alerts

**Option 1: GitHub Actions notifications**
- Configure Slack/email notifications for validation failures
- Alert on repeated failures from same contributor

**Option 2: Monthly report**
```bash
# Create monthly report script
#!/usr/bin/env bash
# scripts/monthly-workflow-report.sh

echo "=== Monthly Git Workflow Report ===" > report-$(date +%Y-%m).txt
echo "Period: $(date -d '1 month ago' +%Y-%m-01) to $(date +%Y-%m-%d)" >> report-$(date +%Y-%m).txt
echo "" >> report-$(date +%Y-%m).txt

# Metrics
COMMITS=$(git log --since="1 month ago" --oneline | wc -l)
VALID=$(git log --since="1 month ago" --grep="^(feat|fix|docs):" --oneline | wc -l)
ADOPTION=$((VALID * 100 / COMMITS))

echo "Total commits: $COMMITS" >> report-$(date +%Y-%m).txt
echo "Valid commits: $VALID" >> report-$(date +%Y-%m).txt
echo "Adoption rate: $ADOPTION%" >> report-$(date +%Y-%m).txt

# Email or post to team chat
```

---

## Rollback Procedures

### If Hooks Cause Major Issues

1. **Temporary disable**:
   ```bash
   git config hooks.commit-msg-enabled false
   git config hooks.pre-push-enabled false
   ```

2. **Notify team**:
   "Git hooks temporarily disabled due to [issue]. Commits will not be validated until [date]."

3. **Fix and test**:
   - Fix hook issue
   - Test with pilot team
   - Verify no regressions

4. **Re-enable**:
   ```bash
   just git-setup
   ```

5. **Cleanup** (if needed):
   ```bash
   # Find and fix non-compliant commits made during downtime
   git log --since="[downtime-start]" --format="%H %s" | grep -vE "(feat|fix|docs):"
   ```

---

## Annual Review

### When: Once per year (January recommended)

**Tasks**:
1. **Comprehensive metrics analysis**:
   - Year-over-year adoption trends
   - Time saved from automation
   - Team satisfaction surveys

2. **ROI calculation**:
   - Time saved: Estimated from changelog automation, validation
   - Time invested: Setup + quarterly maintenance
   - Break-even analysis

3. **Strategic planning**:
   - Should we move to Level 3 features?
   - New SAP integrations needed?
   - Workflow improvements from team feedback

4. **Documentation refresh**:
   - Archive outdated docs
   - Update all examples
   - Refresh quick-start guide

5. **Update SAP-051 ledger**:
   - Document year's progress
   - Update adoption status across ecosystem
   - Plan next year's enhancements

---

## Checklist Templates

### Quarterly Maintenance Checklist

```markdown
## Q[1-4] 2025 Git Workflow Maintenance

**Date**: YYYY-MM-DD
**Maintainer**: [Name]

### Hook Updates
- [ ] Pull latest chora-base (if applicable)
- [ ] Re-run `just git-setup`
- [ ] Test hooks with dummy commit
- [ ] Check git version (minimum 2.40)

### Compliance Review
- [ ] Calculate adoption rate (target: >90%)
- [ ] Review non-compliant commits
- [ ] Check branch naming compliance
- [ ] Collect team feedback

### Documentation
- [ ] Generate quarterly changelog
- [ ] Update onboarding docs
- [ ] Update SAP-051 ledger
- [ ] Generate metrics report

### CI/CD
- [ ] Review GitHub Actions runs
- [ ] Update action dependencies
- [ ] Test workflow changes
- [ ] Verify changelog previews

### Notes
[Any issues, improvements, or action items]
```

---

## Resources

- [Git Workflow Quick Start](git-workflow-quickstart.md) - Team onboarding
- [Adoption Blueprint](skilled-awareness/git-workflow-patterns/adoption-blueprint.md) - Full setup guide
- [Protocol Spec](skilled-awareness/git-workflow-patterns/protocol-spec.md) - Technical details
- [Conventional Commits Spec](https://www.conventionalcommits.org/) - Upstream spec

---

**Version**: 1.0.0 (2025-11-16)
**SAP**: SAP-051
**Schedule**: Quarterly + As-Needed
