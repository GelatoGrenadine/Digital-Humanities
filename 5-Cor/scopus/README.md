---
title: "UMinho - Corpora/Estatística"
author: "Henri"
date: "20221015T17"
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

## RAW DATA : EXTRACTION & BIDING

By going into the [scopus website](https://www.scopus.com/search/form.uri?display=basic#basic) logging in with UMinho's credentials and queryinng `"digital humanities"` as of Oct 14th 2022 we arise into **4 037 document results**. Due to site limitations simple download of the document entries table is capped at 2 000 documents. They thus need to be downloaded in three parts, for instance: 1999-2017; 2018; 2019-2022.

![Scopus export parameters: Citation Information; Abstract & keywords](~/Desktop/UMinho/4-STAT/scopus.parameters.png)

```{r colating_input include=FALSE echo=FALSE eval=FALSE}
# Concatenating files by first stripping headers of the bottom ones

write.csv(
          rbind(
                read.csv("~/Desktop/UMinho/4-STAT/scopus.2022-2019.csv"),
                read.csv("~/Desktop/UMinho/4-STAT/scopus.2018-2013.csv"), 
                read.csv("~/Desktop/UMinho/4-STAT/scopus.2012-1999.csv") 
            
          ),
          "~/Desktop/UMinho/4-STAT/scopus.2022-1999.csv", 
          row.names = FALSE)
```

## DATA INPUTTING

Taking the binded RAW Data from before and assigning it to a data frame `digital_humanities`:

```{r read_csv, echo=TRUE}
# Read csv & add to data frame
digital_humanities <- 
  read.csv(
           "~/Desktop/UMinho/4-STAT/scopus.2022-1999.csv") 
```

## DATA PROCESSING

**GOAL**: Get all **Authors** on separate cells, the same applying for **Keywords**.

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


### CONSTRUCTING A WIDE TABLE BY EXPANDING AUTHORS & KEYWORDS

So, using the aforementioned function, the `Authors` were expanded into prefixed *a_* columns — Keywords into *k_*.

```{r wide, echo=TRUE}
dh_w <- 
  digital_humanities %>%
    bind_cols(
              split_into_multiple(
                                  digital_humanities$Authors,", ", "a")) %>%
    bind_cols(
              split_into_multiple(
                                  tolower(
                                          digital_humanities$Author.Keywords),"; ", "k"))
```

That does generate a wide format table. Here's more [on wide and long format tables](http://www.cookbook-r.com/Manipulating_data/Converting_data_between_wide_and_long_format/).

### MAKE LONG FORM TABLE 

We'll need a long format one, so will pivot it:

```{r long, echo=TRUE}
# so that every line will have a single author and a single keyword
dh_l <- 
  dh_w %>% 
    pivot_longer(
                  cols = starts_with('k_'), names_to ='key_n',values_to = 'keyword') %>% 
    pivot_longer( 
                  cols = starts_with('a_'), names_to ='aut_n',values_to = 'author') 

nrow(dh_l)
```

But that generates lot's of rows with missing values. Actually almost 6.5 million rows in excess !

### TIDYING UP BEFORE OUTPUTTING

To eliminate rows with missing values will filter our data to only rows containing both a `keyword` and an `author`.

```{r tidying, echo=TRUE}
# delete lines in which either keyword or author is NA
dh <- 
  dh_l  %>% 
      select(!c('key_n', "aut_n")) %>%
      filter(!is.na(keyword)) %>% 
      filter(!is.na(author))

nrow(dh)
```

To which we arise at around 41k rows.

### CHECKING BEFORE OUTPUTTING

To make sure everything checks, let's probe our refined data

```{r checking, echo=TRUE}
skim(dh)
view(dh)
length(unique(dh$author))
length(unique(dh$keyword))
view(unique(dh$keyword))

skim(digital_humanities)
length(unique(digital_humanities$Title))
length(unique(digital_humanities$Authors))
digital_humanities %>%  group_by(Title) %>% add_count(Title) %>% filter(n > 1)

length(unique(digital_humanities$Authors))
length(unique(dh$Authors))
# further standardization aproaches
## strip the 'digital ' pre-fix
```
#### Summary

01. `Authors` in the input I had a set of 3 613 different authorial groups which decreased to 2 639
02. `Title` may show as that we lost some entries as it pegs 2 800 against the 4 037 that we saw querying for "digital humanities" at scopus website. By further research on the `digital_humanities` input data I've noticed there's entries titled _Introduction_, _Conclusion_ and also more specific ones terminating by _ICDAR_ that appear in 80 rows. In other words, there's 3 982 unique Titles names.
03. `Year` is present in all rows, by it's histogram we see publishing is speeding up
04. `Source.title` may probe usefull in the future, could include more data from: `Volume`, `Issue`, `Art..No.`
05. `Volume`: see `Source.title`
06. `Issue`: see `Source.title`
07. `Art..No.`: see `Source.title`
08. `Page.start`: see `Page.count`
09. `Page.end`: see `Page.count`
10. `Page.count` seems unusable as it's completion rate is around 1% but it could be boosted by calculating 1 + `Page.end` + `Page.start`
11. `Cited.by` can probably be used as it's completing rate is 63%, but it ranges from 1 to 1 062 when it's present.
12. `DOI` may be useful in the future
13. `Link` with a complete rate of 100% in the input file and being unique at 4 037 has decreased to 2 814. I think it's safe to say that the input was indexed by `Link` rather than any other variable as it's the single one which matches with number of rows.
14. `Abstract` may be useful in the future.
15. `Author.Keywords` shows 2 789 unique sets of `keywords` on the input data which fell by a single case to 2 788. Something for [further questioning](#to-do).
16. `Index.Keywords` will not be dealt as the scopus was `Author.Keywords`.
17. `Document.Type` may be useful in the future
18. `Open.Access` 40% complete rate, discard ?
19. `Source` it's allways "scopus" so irrelevant as it's invariable
20. `keyword` is still high at 7 869, [further refinement needed](#to-do).
21. `author` there's 5 607 unique authors, but including a so-called _[No author name available]_ that came from original input data. By tracing back into input data:

##### To-Do
- [ ] Check the single instance of  `Author.Keywords` lost from input to output
- [ ] Refine  `keyword` to a more tenable amount
- [x] Set empty fields to NA

##### Learned

- `mutate_all(na_if,"")` change every empty cell into a `na` cell.
- `colnames()`

So we supposedly have 5.6k unique authors, and 7.8k different keywords.

```{r tidying_p2, echo=TRUE}
# delete lines in which either keyword or author is NA
dh_2 <- 
  dh  %>% 
      mutate_all(na_if,"") %>%
      filter(author!="[No author name available]") %>%
      select(!c('Volume', 'Issue', 'Art..No.', 'Page.start', 'Page.end', 'Page.count', 'Index.Keywords', 'Source'))

skim(dh_2)
```

### DEPRECATED FIRST DRAFT

On class I had made a quick fix, but for that I had to previously generate keyword and author vectors to use as the new columns. A [function](#an-useful-function) is a more elegant solution. The code below won't execute.

```{sh deprecated_bash include=FALSE echo=FALSE eval=FALSE}
# Concatenating files by first stripping headers of the bottom ones
tail -n +2 scopus.1999-2017.csv > scopus.1999-2017.nh.csv  
tail -n +2 scopus.2018.csv > scopus.2018.nh.csv  
cat scopus.2019-2022.csv scopus.2018.nh.csv scopus.1999-2017.nh.csv > digital_humanities-scopus.1999-2022.csv
```

```{r deprecated_r, eval=FALSE}
digital_humanities <- read.csv("~/Desktop/UMinho/4-STAT/digital_humanities-scopus.1999-2022.csv") 
k_30 <- sprintf("k%02s", seq.int(1:30)); 
a_54 <- sprintf("a%02s", seq.int(1:54));  
dh_wide <- digital_humanities %>% mutate(Author.Keywords=tolower(Author.Keywords)) %>% separate(Author.Keywords,k_30,sep = "; ") %>% separate(Authors,a_54,sep = ", ")
dh_long <- dh_wide %>% pivot_longer(cols = k_30, names_to ='key_n',values_to = 'keyword') %>% pivot_longer( cols = a_54, names_to ='aut_n',values_to = 'authors') 
dh <- dh_l  %>% select(!c('key_n', "aut_n")) %>% filter(!is.na(keyword)) %>% filter(!is.na(author))
```


## OUTPUTTING TO .csv & .zip FILES


```{r outputting, echo=TRUE}

write.csv(
          dh,
          "~/Desktop/UMinho/4-STAT/dh_2.2022-1999.csv", 
          row.names = FALSE)
# ziped version
write_csv(
          dh, 
          archive_write("~/Desktop/UMinho/4-STAT/dh_2.2022-1999.csv.zip",
                        "~/Desktop/UMinho/4-STAT/dh_2.2022-1999.csv",
                        format = 'zip',
                        filter = 'gzip',))
```

Future development, wrap it all up into a single file. 
Or [Why u no work](https://www.tidyverse.org/blog/2021/11/archive-1-1-2/#writing-multiple-files-to-an-archive)

```{r outputting_2, echo=TRUE eval=FALSE}
# rapping it all up
archive_write_files("~/Desktop/UMinho/4-STAT/dh_20221015T16.zip",
                    c(
                      "~/Desktop/UMinho/4-STAT/dh_2.2022-1999.csv",
                      "~/Desktop/UMinho/4-STAT/Corpora.Aula04-scopus-digita_humanities.Rmd",
                      "~/Desktop/UMinho/4-STAT/scopus.parameters.png"
                    ),
                    format = 'zip'
                    )
```

