grammar funx;

root: (fun_declaration)* (expr)?;

fun_declaration: FUN_IDENT declare_params block;

expr:
	expr A_LA expr
	| expr (PER | ENTRE | MOD) expr
	| expr (MES | MENYS) expr
	| '(' expr ')'
	| fun_call
	| (MENYS | MES)? NUMBER
	| IDENT;

declare_params: (IDENT)*;

block: '{' (logical_expr | show)* expr? '}';

fun_call: FUN_IDENT call_params;

show: SHOW (expr | StringLiteral);

logical_expr: if_expr | while_expr | assignment;

call_params: (expr)*;

StringLiteral: UnterminatedStringLiteral '"';

UnterminatedStringLiteral: '"' (~["\\\r\n] | '\\' (. | EOF))*;

if_expr:
	IF condition_block (ELSE IF condition_block)* (ELSE block)?;

while_expr: WHILE condition_block;

assignment: IDENT ASSIGN expr;

condition_block: condition block;

condition:
	condition AND condition
	| condition OR condition
	| condition XOR condition
	| condition GT condition
	| condition GE condition
	| condition LT condition
	| condition LE condition
	| condition EQ condition
	| condition NE condition
	| '(' condition ')'
	| expr;

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

// show
SHOW: 'show';

// logical_expr
IF: 'if';
ELSE: 'else';
WHILE: 'while';

// logical_operators
AND: 'and';
OR: 'or';
XOR: 'xor';
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

// atoms
LETTER: (MINUS | MAJUS);
MAJUS: [A-Z];
MINUS: [a-z];
DIGIT: [0-9];

// helpers
WS: [ \r\n]+ -> skip;