default:report.pdf

report.pdf: report.tex references.bib
	pdflatex report.tex
	bibtex report
	pdflatex report.tex
	pdflatex report.tex

clean:
	rm -f *.{log,aux,bbl,blg}
	rm -f *~

veryclean:
	rm -f report.pdf

archive:default clean
	tar -cjvf philip_robinson.tar.bz2 *
