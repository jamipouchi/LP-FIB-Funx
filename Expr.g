grammar Expr;

root: (fun_declaration)* expr?;

fun_declaration: FUN_IDENT declare_params block;

expr:
	expr A_LA expr
	| expr (PER | ENTRE | MOD) expr
	| expr (MES | MENYS) expr
	| '(' expr ')'
	| fun_call
	| NUMBER
	| IDENT;

declare_params: (IDENT)*;

block: '{' (logical_expr)* expr? '}';

fun_call: FUN_IDENT call_params;

logical_expr: if_expr | while_expr | assignment;

call_params: (expr)*;

if_expr:
	IF condition_block (ELSE IF condition_block)* (ELSE block)?;

while_expr: WHILE condition_block;

assignment: IDENT ASSIGN expr;

condition_block: condition block;

condition:
	condition GT condition
	| condition GE condition
	| condition LT condition
	| condition LE condition
	| condition EQ condition
	| condition NE condition
	| '(' condition ')'
	| NUMBER
	| IDENT;

// comment
LINE_COMMENT: '#' ~[\r\n]* -> skip;

// operators
A_LA: '^';
PER: '*';
ENTRE: '/';
MOD: '%';
MES: '+';
MENYS: '-';

// assignment
ASSIGN: '<-';

// logical_expr
IF: 'if';
ELSE: 'else';
WHILE: 'while';

// logical_operators
GT: '>';
GE: '>=';
LT: '<';
LE: '<=';
EQ: '=';
NE: '!=';

// constructions
NUMBER: (DIGIT)+;
IDENT: MINUS (LETTER | DIGIT)*;
FUN_IDENT: MAJUS (LETTER | DIGIT)*;
COMMENT_START: '#';

// fragments
LETTER: (MINUS | MAJUS);
MAJUS: [A-Z];
MINUS: [a-z];
DIGIT: [0-9];

// helpers
EOL: '\n';
WS: [ \n]+ -> skip;