# MD++
MD++ est un compilateur de markdown améliorée vers HTML.
Notre version de markdown ajoute la possibilités de faire des boucles (for et while), des conditions (if, elif, else), des variables ($varName) et des fonctions.

Notre langage accepte 1 instructions par ligne.

Avec les conditions et les variables, on peut avoir quelques chose du type :
```md
# Exemple avec un test :

Bonjour,
@if($genre == homme) 
  Monsieur
@elif($genre == femme) 
  Madamme
@else 
  Something
@endif
```

Un exemple de boucle et de fonction
```md
# Exemple avec une boucle for :

<<<<<<< HEAD
@func liste0To10()
  @for($i=0;$i<10;$i++)
=======
$liste0To10() {
  @for($i=0;i<10;$i++) {
>>>>>>> 51ef57b0116e58dd8392fa6c0f1ce5ff4ca1e9ec
    * Element $i
  @endfor
@endfunc

@liste0To10()
```

# Lexèmes
| Input | Output |
|---|---|
| Simple text | Simple text |
| \*italic\*  | \<i>italic\</i> |
| \*\*bold\*\* | \<b>bold\</b> |
| \*\*\* bold and italic \*\*\* | \<i>\<b>bold and italic\</b>\</i> |
| # Title 1 | \<h1>Title 1\</h1> |
| ## Title 1.1 | \<h2>Title 1.1\</h2>|
| ### Title 1.1.1 | \<h3>Title 1.1.1\</h3>|
| * Elem 1 <br> * Elem 2 <br> &emsp; * Elem 1 | \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ul>\<li>Elem 1\</li>\</ul>\</ul> |
| 1. Elem 1 <br> 2. Elem 2 <br> &emsp; 1. Elem 1 | \<ol>\<li>Elem 1\</li>\<li>Elem 2\</li>\<ol>\<li>Elem 1\</li>\</ol>\</ol> |
| \|header1\|header2\|<br>\|\---\|\---\|<br>\| cell 1\| cell 2\| | \<table>\<tr>\<th>header 1\</th>\<th>header 2\</th>\</tr>\<tr>\<td>cell 1\</td>\<td>cell 2\</td>\</tr>\</table>  |
| @if(\$var == c)<br>Plouc<br>@elif(\$var==k)<br>Plouk <br>@else<br>Plouque<br>@endif | Plouc |
| @for($i=0;i<3;i++)<br>* Elem $i<br>@endforeach| \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<li>Elem 3\</li>\</ul> |
| @while($i<3)<br>* Elem $i<br>\$i+=1@endwhile | \<ul>\<li>Elem 1\</li>\<li>Elem 2\</li>\<li>Elem 3\</li>\</ul |
| @func myFunc(\$i) <br> # Titre $i<br>@endfunc <br> @myFunc(3) | \<h1>Titre 3\</h1> |

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
