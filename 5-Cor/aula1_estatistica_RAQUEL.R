library(haven)
library (ggplot2)
library(dplyr)
library(gmodels)

dados <- read_sav("Downloads/estatistica/aula1/dados_opiniao.sav")

# unidade - qualitativa nominal
# curso - qualitativa nominal
# tipo de aluno - qualitativa ordinal
# idade - quantitativa continua
# faixa etária - qualitativa ordinal
# classe de sentimento - qualitativa ordinal
# opinião -qualitativa
# n de palavras - quantitativa discreta

# média, mediana e desvio padrão
summary(dados$idade)
mean(dados$idade) 
median(dados$idade)
sd(dados$idade) 
# em média a idade dos alunos é de 24.97 anos.
# o desvio padrão de idade dos alunos entrevistados é de 2.82 em relação a média.

# tipo de aluno
aluno2 <- as.numeric(as.factor(dados$TIPO_ALUNO))
mean(aluno2)
median(aluno2)
sd(aluno2)

# n palavras
mean(dados$n_palavras)
median(dados$n_palavras)
sd(dados$n_palavras)

# plot idade e faixa etaria
ggplot(dados, aes(x=idade )) + 
  ggtitle("Idade x Faixa etária") +
  geom_bar(aes(fill = FX_ETARIA))

ggplot( dados, aes(x=idade)) +
  geom_histogram( binwidth=3, fill="#69b3a2", color="#e9ecef", alpha=0.9) +
  ggtitle("Distribuição Idade") +
  theme(plot.title = element_text(size=15))
    
ggplot(dados, aes(x=as.factor(FX_ETARIA), fill=as.factor(FX_ETARIA))) + 
  geom_bar( ) +
  ggtitle("Distribuição Faixa Etária") +
  scale_fill_hue(c = 40) +
  theme(legend.position="none")

# plot n_palavras e sentimento
ggplot(dados, aes(x=n_palavras))+
  ggtitle("N de palavras x Sentimento") +
  geom_bar(aes(fill = CLASSEDESENTIMENTO))

ggplot(dados, aes(x=n_palavras, fill=n_palavras)) + 
  ggtitle("Distribuição do N de palavras") +
  geom_boxplot() 

ggplot(dados, aes(x=as.factor(CLASSEDESENTIMENTO), fill=as.factor(CLASSEDESENTIMENTO))) + 
  geom_bar( ) +
  ggtitle("Distribuição Sentimento") +
  scale_fill_hue(c = 40) +
  theme(legend.position="none")

# com filtro
n_palavras2 <- dados %>% filter(dados$n_palavras >=74)

ggplot(n_palavras2, aes(x=n_palavras, fill=n_palavras)) + 
  ggtitle("Distribuição do N de palavras") +
  geom_boxplot() 

# tabela de dupla entrada com os dados de ”tipo de aluno” e ”sentimento”. 
CrossTable(dados$TIPO_ALUNO,dados$CLASSEDESENTIMENTO,prop.r=FALSE, prop.c=TRUE,
           prop.t=FALSE, prop.chisq=FALSE)

# gráfico de barras
ggplot(dados, aes(x=TIPO_ALUNO )) + 
  ggtitle("Idade x Faixa etária") +
  geom_bar(aes(fill = CLASSEDESENTIMENTO))

# n_palavras 

# amplitude
range(dados$n_palavras)
AT <- ceiling((max(dados$n_palavras)- min(dados$n_palavras)))
AT

# classes
length(dados$n_palavras)
k <- nclass.Sturges(dados$n_palavras)
k

# tamanho classe
h <- ceiling(AT/k)
h

infclass <- min(dados$n_palavras)
supclass <- infclass+(k*h)

# tabelas freq

brk <-seq(infclass,supclass,h)
brk

freq_absoluta<-table(cut(dados$n_palavras,breaks = brk, right = FALSE))
freq_absoluta


freq_relativa <- prop.table(freq_absoluta)
freq_relativa

# Histograma de frequência absoluta

ggplot( dados, aes(x=n_palavras)) +
  geom_histogram( binwidth=15, fill="#69b3a2", color="#e9ecef", alpha=0.9) +
  ggtitle("Histograma de frequência absoluta") +
  theme(plot.title = element_text(size=15))

# Histograma de frequência relativa

ggplot( aes(x = dados$n_palavras, y=freq_absoluta))+
  geom_bar( width = 0.8, position = position_dodge(width = 0.9), stat = "identity")+ 
  labs(x="Idade (anos)", y=" ", fill = " ") +
  ggtitle("Conceito de Efluente") +
  scale_y_continuous(labels = scales::percent) 
