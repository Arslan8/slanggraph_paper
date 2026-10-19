.PHONY: all clean check figures

all: main.pdf

figures: figures/motivation.pdf figures/architecture.pdf figures/exposure.pdf figures/overhead.pdf

figures/motivation.pdf figures/architecture.pdf figures/exposure.pdf figures/overhead.pdf: scripts/generate_figures.py
	python3 scripts/generate_figures.py

main.pdf: main.tex references.bib usenix-2020-09.sty figures
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	bibtex main
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex

check: main.pdf
	@test "$$(pdfinfo main.pdf | awk '/^Pages:/ {print $$2}')" -le 20
	@pdffonts main.pdf | awk 'NR > 2 && $$6 != "yes" { bad=1 } END { exit bad }'

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf
