(?# single line sed possible solutions sed 's/&/&amp;/g; s/</\&lt;/g; s/>/\&gt;/g;' 0.txt > 1.txt)
(?# maybe https://docs.python.org/3/library/stdtypes.html#str.translate)

&
&amp;

<
\&lt;

>
\&gt;

(?# multi line python out = re.sub(r'^$\n{2,}', r'\n\n', open(f_i, "r".read(, flags=re.M)
^$\n{2,}
\n\n