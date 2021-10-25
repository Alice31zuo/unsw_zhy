puzzle: puzzle.o boardADT.o
	dcc -o puzzle puzzle.o boardADT.o

boardADT.o: boardADT.c boardADT.h
	dcc -c boardADT.c

puzzle.o : puzzle.c boardADT.h
	dcc -c puzzle.c

clean:
	rm -f puzzle *.o *.gch
