# droitesdiscretes
Droites discrètes et formes quasi affines en Python

## Création du dictionnaire français

    aspell --lang fr dump master | aspell --lang fr expand | tr ' ' '\n' > french.dic
    