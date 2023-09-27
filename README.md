## Back-end sistema Meu Treino

Execute os codigos abaixo no terminal em ordem para e rodar a aplicação.

python3 -m venv env

pip install --upgrade pip

.\env\Scripts\activate

pip install -r requirements.txt

flask run --host 0.0.0.0 --port 5000 --reload

OBS: Caso ocorra algum erro referente a dependencias desatualizadas, busque a mais recente para executar no terminal.

## Executando com Docker

Com o serviço docker executando use os seguintes comandos em seu terminal:

Para criar a imagem (com o "ponto"):
docker build -t back-mvp .

para executar a imagem:
docker run -p 5000:5000 back-mvp

## Biblioteca da API "Fitness Calculator"

https://rapidapi.com/malaaddincelik/api/fitness-calculator/details

