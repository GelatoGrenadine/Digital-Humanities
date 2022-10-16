library(readr)
library(ggplot2)
library(hrbrthemes)
library(dplyr)

dados <- read_csv("dados_sent.csv")

g1 <- ggplot(dados, aes(x = dados$X1, fill = dados$SENT)) +
  geom_histogram() +
  ggtitle("Sentimento x X1")

g2 <-ggplot(dados, aes(x = dados$X2, fill = dados$SENT)) +
  geom_histogram() +
  ggtitle("Sentimento x X2")

g3 <-ggplot(dados, aes(x = dados$X3, fill = dados$SENT)) +
  geom_histogram() +
  ggtitle("Sentimento x X3")

g4 <-ggplot(dados, aes(x = dados$X4, fill = dados$SENT)) +
  geom_histogram() +
  ggtitle("Sentimento x X4")

# juntar gráficos
g1 + g2 + g3 + g4

# média e desvio padrão de X1
dados %>% 
      group_by(SENT) %>% 
      summarise(mean(X1), sd(X1))

# Box plot de X1 com SENT
ggplot(dados, aes(x=X4, fill=SENT)) + 
  ggtitle("Distribuição ") +
  geom_boxplot() 


# gráfico de dispersão de x3 e x4
ggplot(dados, aes(x=dados$X3, y=dados$X4, color=dados$SENT)) + 
  geom_point(size=6) +
  geom_smooth(method=lm, se=FALSE) +
  theme_ipsum()

