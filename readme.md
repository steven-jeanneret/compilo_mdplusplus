# MD++
MD++ est un compilateur de markdown améliorée vers HTML.
Notre version de markdown ajoute la possibilités de faire des boucles (for et while), des conditions (if, elif, else), des variables ($varName) et des fonctions.

Notre langage accepte 1 instructions par ligne.

Avec les conditions et les variables, on peut avoir quelques chose du type :
```md
# Exemple avec un test :

Bonjour,
_if($genre == homme)
  Monsieur
_elif($genre == femme)
  Madamme
_else
  Something
_endif
```

Un exemple de boucle et de fonction
```md
# Exemple avec une boucle for :

_func liste0To10() {
  _for($i=0;i<10;$i++) {
    * Element $i
  _endfor
_endfunc

_liste0To10()
```

# Lexèmes
| Input | Output |
|---|---|
| Simple text | Simple text |
| \*italic\*  | \<i>italic\</i> |
| \*\*bold\*\* | \<b>bold\</b> |
| # Title 1 | \<h1>Title 1\</h1> |
| ## Title 1.1 | \<h2>Title 1.1\</h2>|
| ### Title 1.1.1 | \<h3>Title 1.1.1\</h3>|
| * Elem 1 <br> * Elem 2 <br> &emsp; * Elem 1 | \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ul>\<li>Elem 1\</li>\</ul>\</ul> |
| 1. Elem 1 <br> 2. Elem 2 <br> &emsp; 1. Elem 1 | \<ol>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ol>\<li>Elem 1\</li>\</ol>\</ol> |
| \|header1\|header2\|<br>\|\---\|\---\|<br>\| cell 1\| cell 2\| | \<table>\<tr>\<th>header 1\</th>\<th>header 2\</th>\</tr>\<tr>\<td>cell 1\</td>\<td>cell 2\</td>\</tr>\</table>  |
| _if(\$var == c)<br>Plouc<br>_elif(\$var==k)<br>Plouk <br>_else<br>Plouque<br>_endif | Plouc |
| _for($i=0;i<3;i++)<br>* Elem $i<br>_endforeach| \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<li>Elem 3\</li>\</ul> |
| _while($i<3)<br>* Elem $i<br>\$i+=1_endwhile | \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<li>Elem 3\</li>\</ul |
| _func myFunc(\$i) <br> # Titre $i<br>_endfunc <br> _myFunc(3) | \<h1>Titre 3\</h1> |

# Grammaire
| expression | définition | commentaires |
|---|---|---|
| text | line text| Une ligne suivis d'autres |
| text | line | Dernière ligne|
| line | statement newline | Statement suivis par d'autres |
| line | statement | Dernier statement |
| statement | word | |
| statement | bold |  |
| statement | italic | |
| bold | \*\* WORD \*\* | lex |
| italic |\* WORD \* | lex |
| list | list_elem list | Liste composé de plusieurs list_elem|
| list | list_elem | Dernier éléments de la liste |
