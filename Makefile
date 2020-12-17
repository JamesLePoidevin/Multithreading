./bin/send.o : ./bin/send.o
	gcc -o ./bin/send.o -c ./capteur/send.c -W -Wall -ansi -pedantic

./bin/receive.o : ./bin/receive.o
	gcc -o ./bin/reveive.o -c ./service/receive.c -W -Wall -ansi -pedantic

clean:
	rm -rf ./bin/*.o