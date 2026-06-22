# FlowFence revised manuscript package

This package contains the revised LaTeX manuscript and compiled PDF for the WINE 2026-oriented version.

Main changes in this revision:

- Retitled the paper as `FlowFence: Runtime Mediation for Privacy Propagation Externalities in AI-Mediated Platforms`.
- Rewrote the abstract and introduction around the WINE-facing platform-externality framing.
- Tightened claims and removed scattered defensive wording from the main narrative.
- Reorganized the method section around event mediation, safe-view construction, quarantine, propagation-right narrowing, and a formal raw-containment proposition.
- Compressed the experimental-design section and moved role/topology/configuration tables to the appendix.
- Added the RQ2 topology-support table to the main results section.
- Preserved the main MiniMax, label-free, and retrieval-memory evidence tables.
- Updated Figure 1 central label to `FlowFence Runtime Guard` for consistency with the revised title.

Build command used in this environment:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex8 main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
