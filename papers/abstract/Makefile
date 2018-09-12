default:abstract.pdf

abstract.pdf: abstract.tex references.bib
	pdflatex abstract.tex
	bibtex abstract
	pdflatex abstract.tex
	pdflatex abstract.tex

clean:
	rm -f *.{log,aux,bbl,blg}
	rm -f *~

veryclean:
	rm -f abstract.pdf

archive:default clean
	tar -cjvf philip_robinson.tar.bz2 *
