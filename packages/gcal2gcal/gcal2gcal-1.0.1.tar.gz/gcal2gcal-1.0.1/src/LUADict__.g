lexer grammar LUADict;
options {
  language=Python;

}

T10 : '=' ;
T11 : '{' ;
T12 : '}' ;
T13 : ',' ;
T14 : '[' ;
T15 : ']' ;
T16 : 'nil' ;
T17 : 'true' ;
T18 : 'false' ;

// $ANTLR src "LUADict.g" 30
fragment
EscapeSequence
	:	'\\' ('b' | 't' | 'n' | 'f' | 'r' | '\"' | '\'' | '\\' );
	
// $ANTLR src "LUADict.g" 34
String:	'"' ( EscapeSequence | ~('\\'|'"') )* '"';

// $ANTLR src "LUADict.g" 36
LINE_COMMENT
    : '--' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN};

// $ANTLR src "LUADict.g" 39
NUM	:	('0'..'9')+ ('.' ('0'..'9')+)?;

// $ANTLR src "LUADict.g" 41
WS	:       (' ' | '\n' | '\t' | '\r' )+ {$channel=HIDDEN};

// $ANTLR src "LUADict.g" 43
ID	:	('a'..'z'|'A'..'Z'|'_')+;
