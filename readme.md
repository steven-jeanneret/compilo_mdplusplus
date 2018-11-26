# MD++
MD++ est un compilateur de markdown améliorée vers HTML.
Notre version de markdown ajoute la possibilités de faire des boucles (for et while), des conditions (if, elif, else), des variables ($varName) et des fonctions.

Notre langage accepte 1 instructions par ligne.

Avec les conditions et les variables, on peut avoir quelques chose du type :
```md
# Exemple avec un test :

Bonjour,
if($genre == "homme") {
  Monsieur
} elif($genre == "femme") {
  Madamme
} else {
  Something
}
```

Un exemple de boucle et de fonction
```md
# Exemple avec une boucle for :

$liste0To10() {
  for($i=0;i<10;$i++) {
    * Element $i
  }
}

$liste0To10()
```