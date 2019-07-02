# Lista6_LucasMaciel_2019.1 - Grafos

nome | matrícula
-|-
Lucas Maciel Aguiar | 17/0070735

### Dependências
Para utilizar este programa, deve-se instalar as dependências:

    $ sudo apt-get update
    $ sudo apt-get install python3-pip
    $ sudo pip3 install -r requirements.txt

### Utilização
Para iniciar o programa:

    $ python3 graph.py

Quando o Programa é iniciado, nele é questionado qual url deve ser consultada

#### Parâmetros extras

    $ python3 graph.py -f -l

* -f = baixar arquivos dos sites e linkar nos arquivos html
* -l = flag para quando o programa iniciar, indicar quantas camadas em largura devem ser percorridas
* -n = indica que a busca pode procurar por urls que não fazem parte da url principal passada (Não Recomendado)