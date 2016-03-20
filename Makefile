report.pdf: report.tex
	pdflatex --halt-on-error $^
