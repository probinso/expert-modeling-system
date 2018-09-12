default: pres.pdf

pres.pdf: pres.tex coffee4.sty Train.png Test.png
	pdflatex pres.tex
	pdflatex pres.tex

veryclean: clean
	rm -f pres.pdf

clean:
	rm -f pres.aux  pres.log  pres.nav  pres.out  pres.snm  pres.toc *~
