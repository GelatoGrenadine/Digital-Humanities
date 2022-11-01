library(readxl)
library(readr)
library(ggplot2)
library(dplyr)
library(gmodels)

dados1 <- read_excel("grammar in action _EN.xlsx")
dados2 <- read_excel("grammar in action _EN.xlsx", 
                                   sheet = "Notas")

ggplot(dados1, aes(x=as.factor(dados1$`What is your foreign language I`), fill=as.factor(dados1$`What is your foreign language I`)))+
  geom_bar() +
  ggtitle("Distribuição frequência lingua estrangeira") +
  theme(legend.position="none")

dados_count <- dados1 %>% count(`What is your foreign language I`)

dados_filter<- dados1 %>% filter(`What language(s) do you speak at home?` == "French" &
                                   `What is your foreign language I` == "English") 

CrossTable(dados_filter$Gender,dados_filter$`Level of Foreign language I`,prop.r=TRUE, prop.c=FALSE,
           prop.t=FALSE, prop.chisq=FALSE)

library(hrbrthemes)
ggplot(dados2, aes(x=dados2$pré, y=dados2$post, color=dados2$Gender)) + 
  geom_point(size=6) +
  theme_ipsum()


ggplot(dados2, aes(x=Gender, y=post, fill="red")) + 
  ggtitle("") +
  geom_boxplot() 

ggplot(dados2, aes(x=Gender, y=pré, fill="red")) + 
  ggtitle("") +
  geom_boxplot() 

