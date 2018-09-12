default: flow.pdf

flow.pdf: flow.tex coffee4.sty Train.png Test.png
	pdflatex flow.tex
	pdflatex flow.tex

veryclean: clean
	rm -f flow.pdf

clean:
	rm -f flow.aux  flow.log  flow.nav  flow.out  flow.snm  flow.toc *~
