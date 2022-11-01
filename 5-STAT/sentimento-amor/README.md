---
title: "UMinho - Corpora/Estatística"
author: "Henri"
date: "20221025T18"
output:
  pdf_document: default
  html_document: default
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
library("dplyr")
library("tidyverse")
library("skimr")
library("haven")
library("readxl")
library("stringr")
library("archive")

```

## RAW DATA & DATA INPUTTING

_Amor de Perdição_ **Camillo Castello Branco** 18¿? portuguese version, ISBN: ¿10/13?
[source](https://docs.google.com/spreadsheets/d/1YQ8hXYM5l4cfrvbzYx-pogehIv5zu48Ww1L2E3a3rb8/edit#gid=2087957772)


```{r read_csv, echo=TRUE}
# Read csv & add to data frame
camilo_frases <- 
  read.csv(
           "~/Desktop/UMinho/4-STAT/camilo_frases.csv\ -\ FRASES_a_ANOTAR.csv") 
```

## TIDYING UP DATA

As raw data — taken at 2022-10-25 13:33Z — was inputted by different people, a standardization is due!

- Global sentiment [SENTIMENTO.GLOBAL] needs to be standardized into 3 types + NA. Extra headers will be stripped later on.

- The Positive/Negative columns should read `Bollean` + NA. Here's a tricky N/A type typed response that will be flattened into representing that the sentiment is **not present**.

> One can see in `unique(camilo_frases$SENTIMENTO.NEGATIVO)` that there's a semi-colon separated list of strings that is probably missplaced; there's also a strange "5". 
>> PS: As I'm the author of one of the _faux-pas_ I'll ammend it here.
>>> ``` c_f1[445,7] = c_f1[445,6] ```
>>> ``` c_f1[445,6] = "1" ```

```{r data_tidying, echo=TRUE}

unique(camilo_frases$SENTIMENTO.GLOBAL)

c_f <- camilo_frases %>% 
                  mutate(SENTIMENTO.GLOBAL = gsub('^\ *[P|p].*', 
                                                  '+positivo', SENTIMENTO.GLOBAL)) %>% 
                  mutate(SENTIMENTO.GLOBAL = gsub('^\ *[N|n].+g.*', 
                                                  '-negativo', SENTIMENTO.GLOBAL)) %>% 
                  mutate(SENTIMENTO.GLOBAL = gsub('^\ *[N|n].+[tro].*', 
                                                  '=neutro', SENTIMENTO.GLOBAL)) %>%
                  mutate(SENTIMENTO.GLOBAL = na_if(
                                                   SENTIMENTO.GLOBAL, 
                                                   ""))
unique(c_f$SENTIMENTO.GLOBAL)


unique(camilo_frases$SENTIMENTO.POSITIVO)
unique(camilo_frases$SENTIMENTO.NEGATIVO)

c_f1 <- c_f
c_f1[445,7] = c_f1[445,6]
c_f1[445,6] = "1"


c_f2 <- c_f1 %>% 
            mutate(SENTIMENTO.POSITIVO = gsub('(^\ *[P|p].*)|1',
                                              TRUE, SENTIMENTO.POSITIVO)) %>% 
            mutate(SENTIMENTO.POSITIVO = gsub('(^\ *[N|n].*)|0',
                                              FALSE, SENTIMENTO.POSITIVO)) %>%
            mutate(SENTIMENTO.POSITIVO = na_if(
                                              SENTIMENTO.POSITIVO, 
                                              "")) %>% 
            mutate(SENTIMENTO.POSITIVO = SENTIMENTO.POSITIVO == "TRUE")

unique(c_f2$SENTIMENTO.POSITIVO)


c_f3 <- c_f2 %>% 
            mutate(SENTIMENTO.NEGATIVO = gsub('(^\ *[P|p].*)|1',
                                              TRUE, SENTIMENTO.NEGATIVO)) %>% 
            mutate(SENTIMENTO.NEGATIVO = gsub('(^\ *[N|n].*)|0',
                                              FALSE, SENTIMENTO.NEGATIVO)) %>%
            mutate(SENTIMENTO.NEGATIVO = na_if(
                                              SENTIMENTO.NEGATIVO, 
                                              "")) %>% 
            mutate(SENTIMENTO.NEGATIVO = SENTIMENTO.NEGATIVO == "TRUE")

unique(c_f3$SENTIMENTO.POSITIVO)




tail(
     sort(
          table(
                camilo_frases$TERMOS.EXPRESSÕES..POSITIVOS
      )  )     )

tail(sort(table(camilo_frases$TERMOS.EXPRESSÕES..NEGATIVOS)))

to_na = c("", "0", "n/a", "N/A")

c_f4 <- c_f3 %>%
            mutate(TERMOS.EXPRESSÕES..POSITIVOS = na_if(
                                                        TERMOS.EXPRESSÕES..POSITIVOS,
                                                        to_na[1]
                                                       ),
                   TERMOS.EXPRESSÕES..POSITIVOS = na_if(TERMOS.EXPRESSÕES..POSITIVOS, to_na[2]),
                   TERMOS.EXPRESSÕES..POSITIVOS = na_if(TERMOS.EXPRESSÕES..POSITIVOS, to_na[3]),
                   TERMOS.EXPRESSÕES..POSITIVOS = na_if(TERMOS.EXPRESSÕES..POSITIVOS, to_na[4])
            )
tail(sort(table(c_f4$TERMOS.EXPRESSÕES..POSITIVOS)))

c_f5 <- c_f4 %>%
            mutate(TERMOS.EXPRESSÕES..NEGATIVOS = na_if(TERMOS.EXPRESSÕES..NEGATIVOS, to_na[1]),
                   TERMOS.EXPRESSÕES..NEGATIVOS = na_if(TERMOS.EXPRESSÕES..NEGATIVOS, to_na[2]),
                   TERMOS.EXPRESSÕES..NEGATIVOS = na_if(TERMOS.EXPRESSÕES..NEGATIVOS, to_na[3]),
                   TERMOS.EXPRESSÕES..NEGATIVOS = na_if(TERMOS.EXPRESSÕES..NEGATIVOS, to_na[4])
            )
tail(sort(table(c_f5$TERMOS.EXPRESSÕES..NEGATIVOS)))


cf_t <-c_f5 %>% 
          rename(phrase = CAPÍTULO.I..FILIPA.GUIMARÃES) %>%
          rename(global_emotion = SENTIMENTO.GLOBAL) %>%
          rename(has_pos_term = SENTIMENTO.POSITIVO) %>%
          rename(has_neg_term = SENTIMENTO.NEGATIVO) %>%
          rename(pos_terms = TERMOS.EXPRESSÕES..POSITIVOS) %>%
          rename(neg_terms = TERMOS.EXPRESSÕES..NEGATIVOS) %>%
          filter(!str_detect(phrase,"^CAPÍTULO")) %>%
          select(!X)

skim(cf_t)
view(cf_t$pos_terms)
to_na <- append(to_na, "     ")
cf <- cf_t %>%
   mutate(pos_terms = na_if(pos_terms, to_na[5])) %>%
   mutate(pos_terms = gsub('\"\ *;*,*\ *\"',
                                              '"; "', pos_terms),
           neg_terms = gsub('\"[\ \\.;,]*\"', '"; "', neg_terms)) 
view(unique(cf$pos_terms))

skim(cf)
rm(c_f1)
rm(c_f2)
rm(c_f3)
rm(c_f4)
rm(c_f5)

#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[P|p].*', '+positivo' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[N|n].+g.*', '-negativo' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[N|n].+[tro].*', '=neutro' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- na_if(camilo_frases$SENTIMENTO.GLOBAL, "")
```


### AN USEFUL FUNCTION

Since we do not previously know how many authors can be mentioned, nor the quantity of keywords, something akin to Excel's TEXT to Columns is needed. I've though useful to use [Yannis P.](https://stackoverflow.com/users/1885713/yannis-p)'s function found on a Stack Overflow thread named [Split data frame string column into multiple columns](https://stackoverflow.com/questions/4350440/split-data-frame-string-column-into-multiple-columns).

```{r functions, echo=FALSE}
split_into_multiple <- function(column, pattern = ", ", into_prefix){
  cols <- str_split_fixed(column, pattern, n = Inf)
  # Sub out the ""'s returned by filling the matrix to the right, with NAs which are useful
  cols[which(cols == "")] <- NA
  cols <- as.tibble(cols)
  # name the 'cols' tibble as 'into_prefix_1', 'into_prefix_2', ..., 'into_prefix_m' 
  # where m = # columns of 'cols'
  m <- dim(cols)[2]

  names(cols) <- paste(into_prefix, 1:m, sep = "_")
  return(cols)
}
```


### CONSTRUCTING A WIDE TABLE BY EXPANDING TERMS

So, using the aforementioned function, both the `TERMOS.EXPRESSÕES` were expanded into prefixed *p_* & *n_* columns.

```{r wide, echo=TRUE}
cf_w <- cf %>%
    bind_cols(
              split_into_multiple(
                                  cf$pos_terms,'; ', 'p')) %>%
    bind_cols(split_into_multiple(cf$neg_terms,'; ', 'n')) 


```

That does generate a wide format table. Here's more [on wide and long format tables](http://www.cookbook-r.com/Manipulating_data/Converting_data_between_wide_and_long_format/).

### MAKE LONG FORM TABLE 

We'll need a long format one, so will pivot it:

```{r long, echo=TRUE}
# so that every line will have a single author and a single keyword
cf_l <- 
  cf_w %>% 
    rowid_to_column("index") %>%
    pivot_longer(
                  cols = starts_with('p_'), names_to ='pos_p',values_to = 'positivo') %>% 
    pivot_longer( 
                  cols = starts_with('n_'), names_to ='neg_n',values_to = 'negativo')

cf_f <- cf_l %>%
    select(!c(pos_p,neg_n,pos_terms,neg_terms)) %>%
    distinct() %>%
    filter(has_neg_term | has_pos_term) %>%
    filter(!(
               (
                  is.na(negativo) 
                & 
                  has_neg_term
                )
            |
               (
                  is.na(positivo) 
                & 
                  has_pos_term
                )
              )
            ) 

cf_f2 <- cf_f %>% 
    filter(grepl('^\ *\"', negativo))

skim(cf_l)


nrow(cf_l)
```

But that generates lot's of rows with missing values. Actually almost 6.5 million rows in excess !

### TIDYING UP BEFORE OUTPUTTING

To eliminate rows with missing values will filter our data to only rows containing both a `keyword` and an `author`.

```{r tidying, echo=TRUE}
# delete lines in which either keyword or author is NA
cf1 <- 
  cf_l  %>% 
      filter(!is.na(positivo)) %>% 
      filter(!is.na(negativo))

nrow(cf1)
```

To which we arise at around 41k rows.

### CHECKING BEFORE OUTPUTTING

To make sure everything checks, let's probe our refined data

```{r checking, echo=TRUE}
skim(cf1)
view(cf1)
length(unique(cf1$positivo))
view(unique(cf1$postivo))
length(unique(cf1$negativo))
view(unique(cf1$negativo))
# further standardization aproaches
## strip the 'digital ' pre-fix
```
#### Summary


##### To-Do


##### Learned




### DEPRECATED FIRST DRAFT

```{sh deprecated_bash include=FALSE echo=FALSE eval=FALSE}
#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[P|p].*', '+positivo' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[N|n].+g.*', '-negativo' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- sub('^\ *[N|n].+[tro].*', '=neutro' , camilo_frases$SENTIMENTO.GLOBAL)
#camilo_frases$SENTIMENTO.GLOBAL <- na_if(camilo_frases$SENTIMENTO.GLOBAL, "")
```



## OUTPUTTING TO .csv & .zip FILES


```{r outputting, echo=TRUE}

write.csv(
          cf_f2,
          "~/Desktop/UMinho/4-STAT/cf_f2.csv", 
          row.names = FALSE)

write.csv(
          cf_f,
          "~/Desktop/UMinho/4-STAT/cf_f.csv", 
          row.names = FALSE)
s# ziped version
write_csv(
          cf1, 
          archive_write("~/Desktop/UMinho/4-STAT/cf1.csv.zip",
                        "~/Desktop/UMinho/4-STAT/cf1.csv",
                        format = 'zip',
                        filter = 'gzip',))
```
