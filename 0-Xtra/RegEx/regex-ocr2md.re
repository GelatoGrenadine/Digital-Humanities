(?# set page breaks from tesseract to TEI XML)

<pb n="">

(?# smaake horizontal ellypsis characters)
...
…

(?# set hyphenated line breaks from to TEI XML/HTML)
-$[\n]*^
<pc force="inter" style="display: none">\-</pc><lb /

(?# !NEEDS IMPROVING set paragraph when two or more lines are present)
(?!<)((^.+\n){2,})
<p>$1</p>

(?# !NEEDS IMPROVING set line breaks TEI XML Style)
^(?!<)(?! )(.)
<lb />$1

(?# !NEEDS IMPROVING set from MarkDown's _i_ to HTML <i><i/>)
(?# Glenn Slaven https://stackoverflow.com/questions/2013124/regex-matching-up-to-the-first-occurrence-of-a-character)
_(?!<)(.[^_]*)_
<i>$1</i>