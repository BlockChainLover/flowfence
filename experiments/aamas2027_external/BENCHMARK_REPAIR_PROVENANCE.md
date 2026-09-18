# Benchmark repair provenance

PINNED_COMMIT: 8d60fa17b5596b44458a52d4296061b9fc13d6f2
FAILING_FILE: marble/evaluator/evaluator.py
FAILING_BLOB_SHA: 0557ac1037d086019d119cc9927119cf73e5d102
FAILURE_CLASS: UPSTREAM_SOURCE_BUG
UPSTREAM_FIX_FOUND: YES (official maintainer branch fix/coding, not merged main)
UPSTREAM_FIX_COMMIT: 40ddb54b5a379b53196d1bdf20e861dc6f922e19
UPSTREAM_FIX_DIFF: patches/marble_evaluator_parse.patch
LOCAL_FIX_REQUIRED: NO independently derived repair; exact file-specific official-branch backport
RECOMMEND_REPIN: NO
CANDIDATE_COMMIT: 40ddb54b5a379b53196d1bdf20e861dc6f922e19
SEMANTIC_DELTA: full branch not adopted; evaluator parse fix only

Canonical repository https://github.com/ulab-uiuc/MARBLE . GitHub contents API at the exact pin returns blob0557ac1, base64-decoded bytes identical to pristine local file and git blob. Python3.10.9 (supported by pyproject) and3.14.7 both raise SyntaxError at line324 column13. Command: python -c "import ast; ast.parse(open('marble/evaluator/evaluator.py').read())". No dependency-generated source involved.

Surrounding source lines312–329 contain an outer try, an inner if with json.loads/int conversion, an except wrongly indented beneath the if, then an else. Introducing commit03f4f30be6ec1ce376c253e02cbd8df4e642b418 (PR171) moved extraction into an outer try but left prior exception indentation. Parent revision used regex extraction and an inner try; restoring that whole older method would change extraction and is not done.

Search: fetched complete canonical history and all51 advertised branches. Main remains the pin. GitHub SyntaxError issue search returned0; evaluator search returned8 historical feature/evaluator PRs, no matching parser report. Inspected latest100 PRs and official evaluator history. Found maintainer branch fix/coding:40ddb54 fixes exactly this parse method; subsequent c5d50755ffd66510bbb61ec1b0ec449f2b7d634a changes coding paths and is NOT included. MASEval changelog documents other reproduction/path/default discrepancies but supplies no preferred fix over this official branch. Search records are stored in REPAIR_SEARCH.json.

Classification was recorded in RECOVERY_START.json before any edit to benchmark source. Strategy B: apply exact evaluator-only diff from40ddb54 to pristine pin. Preserve all other upstream bytes, prompts/tasks/gold, class/function signatures, metric names and scoring constants. The fixed try catches only JSONDecodeError; invalid rating int conversion still raises ValueError. Valid JSON returns integer mapping; absent/invalid JSON returns{}. Since original module cannot execute, equivalence is intent/interface equivalence supported by upstream repair, not empirical equivalence to a runnable original.

UPSTREAM_BASE_SHA: 8d60fa17b5596b44458a52d4296061b9fc13d6f2
UPSTREAM_FIX_SHA: 40ddb54b5a379b53196d1bdf20e861dc6f922e19
BACKPORT_PATCH_SHA256: 8019ffcdf3affd9698c6702d5ae106b4b63ef651d4a7383d42bce5a885afc68f

Validation:93 Python files compile on Python3.10.9; exact Evaluator class loaded with inert dependencies and static judge; all AST outside parse_research_ratings unchanged. Full package dependency import remains unvalidated (litellm missing), distinguished from successful fixture loading. Pristine source is recoverable with git show at base; source working-tree diff contains exactly the documented evaluator patch.
