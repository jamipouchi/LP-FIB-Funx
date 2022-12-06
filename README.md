# Funx

Funx es un llenguatge de programació orientat a expressions i funcions. Amb Funx podem definir funcions i acabar, opcionalment, amb una expressió.

Un exemple d'una expressió és:
```
2 + 3^(3*2)
```
```
Out #: 731
```

Un exemple d'una funció és:
```
# funció que rep dos nombres enters i en torna la seva suma
Suma x y
{
  x + y
}

Suma (2 * 3) 4 
```
```
Out #: 10
```

Com es pot veure, es pot comentar amb '#'.

El llenguatge permet fer ús de la recursivitat:
```
Fact n
{
    if n < 0 
    {
        show "invalid entry"
        -1
    }
    else if n <= 1 
    {
        1 
    } 
    else
    {
        n * Fact n - 1 
    }
}

Fact 5
```
```
Out #: 120
```

Totes les variables son de tipus enter. Els paràmetres es passen per còpia, i les variables no declarades tenen el valor per defecte 0.

En cas de que una funció no surti a través d'una expressió, retorna ``None`` 

## Especificació de Funx

Les instruccions de Funx són:

- l'assignació amb ``<-`` 
- la invocació de funcions
- el condicional amb ``if``, ``else if``, ``else``
- la iteració amb ``while``
- la impressió per pantalla amb ``show``

## Expressions

La unitat mínima és la expressió, així doncs, es poden comparar, ensenyar i assignar expressions:

```
Comparex2 x 
{
    if ((2*x) > 10) 
    {
        show (2*x)
        x <- x - 1
        show "x modified: "
        show x
    }
}
Comparex2 6
```
```
Out #: None
> 12
> x modified:
> 5
```
Els operadors son els habituals, més la potència: (`` +``, ``-``, ``*``, ``/``, ``%``, ``^``) i tenen la mateixa prioritat que els de C.

## Condicions

Tant amb l'if com amb el while, avaluem condicions. 

```
FizzBuzz 
{
    x <- 1
    while x <= 100 
    {
        if ((x % 15) = 0) 
        {
            show "Fizz Buzz"
        }
        else if ((x % 5) = 0) 
        {
            show "Buzz"
        }
        else if ((x % 3) = 0) 
        {
            show "Fizz"
        }
        else 
        {
            show x
        }
        x <- x + 1
    }
}

FizzBuzz
```
```
Out #: None
> 1
> 2
> Fizz
> 4
> Buzz
> Fizz
> 7
> 8
> Fizz
> Buzz
> 11
> Fizz
> 13
> 14
> Fizz Buzz
...

...
> Fizz Buzz
> 91
> 92
> Fizz
> 94
> Buzz
> Fizz
> 97
> 98
> Fizz
> Buzz
```

## Condicions

Tenim els operadors habituals: (``=``, ``!=``, ``>``, ``<``, ``>=``, ``<=``), i es poden concatenar amb les opearacions típiques: (``and``, ``or``, ``xor``). Nota que l'igualtat és amb ``=``.


## Àmbit de visibilitat

No importa l'ordre de declaració de les funcions. Les variables són locals a cada invocació de cada procediment. No hi ha variables globals ni manera d'accedir a variables d'altres procediments (només a través dels paràmetres).

## Errors

Es tenen el compte els següents errors:

- Divisió per zero:
```
2/0
```
```
Out #: Zero division attempt
```

- Programa infinit: (Para quan no es surt d'un while en 10000 iteracions)
```
ForeverStuck 
{
    while 1 = 1 
    {
        x <- x + 1
    }
}

ForeverStuck
```
```
Out #: Probably stuck in while loop
```

- Redeclaració de funció amb nom ja existent:
```
SayHi 
{
    show "hi"
}

SayHi x 
{
    show "hi"
    show "x"
}
```
```
Out #: This function name is already used: SayHi
```

- Crida d'una funció inexistent
```
MakeMeRich 1
```
```
Out #: You are calling an undefined function: MakeMeRich
```

- Número de paràmetres no coincidents
```
Suma x y 
{
    x + y
}

Suma 1 2 3
```
```
Out #: The number of arguments doesn't match the function signature: 3!=2
```

## L'intèrpret

L'intèrpret, permet introduir codi vàlid funx, i retorna el resultat.
Té 3 zones:
- Consola: On s'introdueix el codi

- Resultats: Mostra les 5 últimes entrades amb els resultats.

- Funcions: Una llista amb les funcions declarades i els seus paràmetres.

## Fer-lo funcionar

Per provar l'intèrpret, aixequeu el servidor flask, ``funx.py``, i a jugar!
S'adjunten els fitxers: ``test-*.py`` per provar les funcionalitats afegides, junt amb els exemples que s'han anat ensenyant, és una bona manera de començar a jugar amb el llenguatge! 
