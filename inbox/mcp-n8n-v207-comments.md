Final Answer: v2.0.7 STILL FAILS - Copier Not Using Bracket Delimiters
Result: ❌ v2.0.7 fails with IDENTICAL ERROR as v2.0.0-v2.0.6
What We Verified
✅ Bracket delimiters ARE in the template:
674 [[ variable delimiters
593 [% block delimiters
ZERO {{ or {% old delimiters
✅ Configuration IS present in copier.yml:
_envops:
  block_start_string: "[%"
  variable_start_string: "[["
✅ Line 289 IS plain Python (no wrapping needed):
test_name = "test_{}_bash_example_{}".format(safe_title, idx)
❌ Copier STILL fails:
TemplateSyntaxError: unexpected char '#' at 9814
File "...extract_tests.py.jinja", line 293
The Problem
Copier 9.10.3 is NOT respecting the _envops delimiter configuration and is still trying to parse the template with curly braces {{ }} and {% %} instead of brackets [[ ]] and [% %].
Why This Is Critical
8 versions tested, 8 versions failed, all with identical error:
v2.0.0 - v2.0.7: Same TemplateSyntaxError at line 293, char 9814
Despite:
Converting f-strings to .format()
Wrapping in {% raw %} blocks
Converting entire template to bracket delimiters
None of it works because Copier isn't loading the delimiter configuration.
Recommendation
For mcp-n8n:
STAY ON v1.9.3
STOP testing v2.0.x releases - this appears to be a Copier bug
Wait for chora-base team to file issue with Copier project
For chora-base team:
File bug report with Copier project
Include minimal reproduction case
Test if this works with different Copier versions
Consider alternative template solutions
This is beyond what can be fixed in the template itself. The configuration is correct but Copier isn't using it.