<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs"
    xmlns="http://www.w3.org/1999/xhtml" version="2.0">
    <!-- 
        Title: up converter from plain-text to XML
        Author: dhumanity (2022-12)
        Repo: https://github.com/dhumanity
        Synopsis:
            Up-convert plain-text file of Camilo Castelo Branco into XML
        Note:
           To be run from the command line as:
            saxon -xsl:upConcerter.xsl -it:init -o:upconverted.xml
            
            No input XML; run from the command line as:
            saxon -xsl:unparsed-text_sonnets.xsl -it:init -o:sonnets.xhtml
        License: GNU Affero General Public License v3.0
            based upon
                Title: unparsed-text_sonnets.xsl
                Author: djb (2017-04-09)
                Repo: https://github.com/xstuff
                Synopsis:
                    Illustrates using XSLT to process plain text
                    Up-translates plain-text file of Shakespearean sonnets to HTML
                Note:
                    No input XML; run from the command line as:
                    saxon -xsl:unparsed-text_sonnets.xsl -it:init -o:sonnets.xhtml
                License: GNU Affero General Public License v3.0
    -->
    <xsl:output method="xml" indent="yes" doctype-system="about:legacy-compat"/>
    <!-- Read plain text document into $input, later to  -->
    <xsl:variable name="input" as="xs:string"
        select="unparsed-text('../Obras/Camilo-A_Brasileira_de_Prazins.txt')"/>
    <!-- 
        split into paragraphs on blank line;
        select titles, regex? 
            (^(?: {12,})([A-Z]+[^a-z\n]*)\n

            if only rooman numbers:
                                    (XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?)\n
    -->
    <xsl:variable name="titles" as="xs:string+" select="tokenize($input, '\n                  ', 's')"/>
    <xsl:variable name="paragraphs" as="xs:string+" select="tokenize($input, '\n         ', 's')"/>
    <!-- specify initial template with "it" parameter to saxon on command line -->
    <xsl:template name="init">
        <html>
            <head>
                <title>A BRASILEIRA DE PRAZINS</title>
            </head>
            <body>
                <h1>Title</h1>
                <xsl:for-each select="$paragraphs">
                    <!-- break each sonnet into lines, the first of which is the number -->
                    <xsl:variable name="p" as="xs:string*" select="tokenize(., '\n')"/>
                    <!-- the test filters out the last one, which is blank (see above) -->
                    <xsl:if test="count($lines) gt 0">
                        <h2>
                            <!-- the first "line" is the roman numeral -->
                            <xsl:sequence select="$lines[1]"/>
                        </h2>
                        <p>
                            <!-- process all real lines of poetry -->
                            <xsl:for-each select="$lines[position() gt 1]">
                                <xsl:sequence select="."/>
                                <!-- don't add <br/> after last line -->
                                <xsl:if test="position() ne last()">
                                    <br/>
                                </xsl:if>
                            </xsl:for-each>
                        </p>
                    </xsl:if>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
