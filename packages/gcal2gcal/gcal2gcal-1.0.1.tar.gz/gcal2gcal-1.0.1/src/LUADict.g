grammar LUADict;

options {language=Python;}

savedVars returns [l] : {l={}} (r=top {l[$r.val[0]] = $r.val[1]})*;

top returns [val]     :	ID '=' dict { 
    $val = ($ID.text,$dict.val)
    };

dict returns [val]	:	'{' r=members {$val = $members.val} '}';

members	returns [val] :	{val = {}} (r=pair {val[$r.val[0]] = $r.val[1]})*;

pair returns [val]	:	(key '=')? value ','? {val = ($key.val,$value.val)};

key returns [val]	:	'['? luaVal {val = $luaVal.val} ']'?;

value returns [val]	:	luaVal {val = $luaVal.val} | dict {val = $dict.val};

luaVal returns [val]	
    : String {val = $String.text[1:-1]}
    | NUM {val = int($NUM.text)} 
    | bool { val = $bool.val }
    | 'nil';

	
bool returns [val] :	'true' {val=True}| 'false' {val=False};

fragment
EscapeSequence
	:	'\\' ('b' | 't' | 'n' | 'f' | 'r' | '\"' | '\'' | '\\' );
	
String:	'"' ( EscapeSequence | ~('\\'|'"') )* '"';

LINE_COMMENT
    : '--' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN};

NUM	:	('0'..'9')+ ('.' ('0'..'9')+)?;

WS	:       (' ' | '\n' | '\t' | '\r' )+ {$channel=HIDDEN};

ID	:	('a'..'z'|'A'..'Z'|'_')+;
