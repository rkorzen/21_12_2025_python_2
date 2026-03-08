# podstawy

## budowanie obrazu

docker build -t <nazwa> .

## uruchamianie obrazu

docker run <nazwa> <args>

docker run hello Rafal


## Zadanie

Utworz prosta aplikacje i ja zdokeryzuj. 
Aplikacja to kalkulator

docker run kalkulator 1 2 +
3
docker run kalkulator 2 2 *
4

+-/* ** %

uzyj wszelkich dobrych praktych do obiektowej implementacji kalkulatora.
stworz nowy projekt


1. Zmien aplikacje w ten sposob, by dzialala jako serwer. (w oparciu o socket i threads)
2. docker-compose urucjamia serwer. Clienta odpalamy w innm terminalu z reki

python calc_client.py 1 10 +
11
python calc_client.py 2 2 *
4