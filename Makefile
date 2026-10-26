PYTHON ?= python3
FIGURES = figures/motivation.pdf figures/architecture.pdf figures/overhead.pdf
TEX_SOURCES = main.tex $(wildcard sections/*.tex)

.PHONY: all clean check figures
.DELETE_ON_ERROR:

all: main.pdf

# The generator writes all figures together; run it only once, including with -j.
figures: scripts/generate_figures.py
	"$(PYTHON)" scripts/generate_figures.py
	@for figure in $(FIGURES); do test -s "$$figure" || exit 1; done

main.pdf: $(TEX_SOURCES) references.bib usenix-2020-09.sty figures
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	bibtex main
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex

# Basic PDF integrity only; venue-specific submission rules require review.
check: main.pdf
	@test -s main.pdf
	@pdfinfo main.pdf > /dev/null
	@fonts="$$(pdffonts main.pdf)" && printf '%s\n' "$$fonts" | awk 'NR > 2 && $$(NF - 4) != "yes" { print "Unembedded font: " $$1; bad=1 } END { exit bad }'

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf $(FIGURES)

