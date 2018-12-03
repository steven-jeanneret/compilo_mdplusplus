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

# Lexèmes
| Input | Output |
|---|---|
| \*italic\*  | \<i>italic\</i> |
| \*\*bold\*\* | \<b>bold\</b> |
| \*\*\* bold and italic \*\*\* | \<i>\<b>bold and italic\</b>\</i> |
| # Title 1 | \<h1>Title 1\</h1> |
| ## Title 1.1 | \<h2>Title 1.1\</h2>|
| ### Title 1.1.1 | \<h3>Title 1.1.1\</h3>|
| * Elem 1 <br> * Elem 2 <br> &emsp; * Elem 1 | \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ul>\<li>Elem 1\</li>\</ul>\</ul> |
| 1. Elem 1 <br> 2. Elem 2 <br> &emsp; 1. Elem 1 | \<ol>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ol>\<li>Elem 1\</li>\</ol>\</ol> |
| \|header1\|header2\|<br>\|\---\|\---\|<br>\| cell 1\| cell 2\| | \<table>\<tr>\<th>header 1\</th>\<th>header 2\</th>\</tr>\<tr>\<td>cell 1\</td>\<td>cell 2\</td>\</tr>\</table>  |