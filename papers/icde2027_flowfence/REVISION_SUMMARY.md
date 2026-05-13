# Revision Summary

## Narrative Shift

The draft was rewritten from a defense-experiment report into a data systems paper about governing the retrieval--exposure boundary in agentic data pipelines. The new narrative centers on the distinction that raw retrieval is not exposure: poisoned records may remain in storage and may be retrieved, but they should not automatically cross into model-visible execution context.

The title is now:

`FlowFence: Governing the Retrieval--Exposure Boundary in Agentic Data Pipelines`

The main text now uses `FlowFence` instead of `FlowFence-Lite`, except where the implementation is described as a lightweight runtime operator. The paper frames the contribution as runtime exposure control, exposure-state accounting, quarantine semantics, and auditability.

## Unsupported Claims Removed or Tightened

The revision removes or avoids claims that FlowFence is secure, universal, generally robust, generally faster, utility-improving, or superior to all weak defenses. The revised claim is scoped to the evaluated adapted AgentPoison MiniMax retrieval-memory poisoning axis.

The text explicitly preserves the following caveats:

- The comparator is adapted and is not full official AgentPoison reproduction.
- Static keyword filtering is strong on the known-trigger axis.
- The paraphrase stress test is a tested family set, not broad held-out generalization.
- FlowFence is detector-dependent; missed unsafe records can still cross the boundary.
- Cost evidence separates 25-question proxy traces from the 10-question measured slice.

## AgentDojo Handling

AgentDojo is no longer presented as a main experiment or table. It is compressed into the `Scope of Interpretation` subsection as a methodological note: MiniMax search hits existed, but selected reruns were unstable, so AgentDojo is not used for defense-effect claims.

## New Tables and Algorithm

The revision adds or reorganizes:

- `Table I`: runtime relations maintained by FlowFence: `Retrieved`, `Decision`, `ContextView`, `Quarantine`, `ActionTrace`, and `Outcome`.
- `Algorithm 1`: runtime exposure control before prompt construction, implemented as a LaTeX `figure` with boxed pseudocode to avoid adding algorithm-package dependencies.
- Main containment and mechanism ablation table focused on the adapted AgentPoison MiniMax axis.
- Retrieval-pressure sensitivity table.
- Paraphrased poisoned-instruction stress-test table.
- Combined clean false-positive and audit semantics table.
- Short cost evidence table separating proxy and measured-slice evidence.

## Figure 1

Figure 1 was not redrawn and the image path was not changed:

`figures/flowfence_architecture.png`

Only the caption was lightly revised to match the retrieval--exposure boundary narrative. A later publication-quality redraw should align the figure with the new data-systems framing, but no figure file was changed in this revision.

## Compilation Status

Attempted local compilation with:

`latexmk -pdf main.tex`

Result: blocked because `latexmk` is not installed on the local machine. `pdflatex`, `xelatex`, and `tectonic` are also unavailable locally. A quick remote check on `wentian-server` found no `latexmk` or `pdflatex` in PATH either.

Static checks completed:

- Figure path exists.
- `IEEEtran.cls` exists.
- `references.bib` exists.
- Cited keys in the revised draft are present in `references.bib`.
- No standalone AgentDojo result table remains.
- No `FlowFence-Lite` occurrences remain in `main.tex`.

## Remaining TODO

- Compile the paper in an environment with a LaTeX engine and inspect page count, table widths, float placement, and bibliography formatting.
- Clean `references.bib` author fields before submission.
- Fill in the AI-generated content acknowledgement according to final submission instructions.
- Redraw Figure 1 later to better match the retrieval--exposure boundary narrative, without changing the evidence or claims.
