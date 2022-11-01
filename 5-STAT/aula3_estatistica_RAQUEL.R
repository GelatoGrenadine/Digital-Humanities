library(readr)
library(dplyr)
library(tidyverse)

scopus <- read_csv("aula3/scopus.csv")

dados_2009 <- scopus %>% filter(`Year` == "2009") 

# Author Keywords
v <- c("k01","k02","k03","k04","k05","k06","k07","k08","k09","k10","k11","k12","k13","k14","k15","k16","k17","k18","k19","k20","k21","k22","k23","k24","k25","k26","k27","k28","k29","k30")
dados_2009_expandido <- dados_2009 %>% separate(`Author Keywords`,v,sep = ";") 

dados_2009t <- dados_2009_expandido %>% pivot_longer(cols=v, names_to ='n',values_to = 'keyword')
dados_2009tna <- dados_2009t[!is.na(dados_2009t$keyword),]

# Author 
v <- c("k01","k02","k03","k04","k05","k06","k07","k08","k09","k10","k11","k12","k13","k14","k15","k16","k17","k18","k19","k20","k21","k22","k23","k24","k25","k26","k27","k28","k29","k30")
dados_2009tAuthor <- dados_2009tna %>% separate(`Authors`,v,sep = ",")

dados_2009t <- dados_2009tAuthor %>% pivot_longer(cols=v, names_to ='n2',values_to = 'Authors2')
dados_2009tna2 <- dados_2009t[!is.na(dados_2009t$Authors2),]

dados2009<- apply(dados_2009tna2,2,function(x)gsub('^\\s+', '',x))


write.csv(dados2009,"aula3/data_2009.csv", row.names = FALSE)
