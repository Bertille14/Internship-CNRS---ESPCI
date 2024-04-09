install.packages("ggplot2")
install.packages("multcomp")
library(ggplot2)
library(readxl)
library(dplyr)
library(tidyr)
library(gridExtra) 
library(readr) 
library(dunn.test)
library(lsmeans)
library(tidyverse)
library(car)
library(multcomp)



sheet_name <- "jour1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_sequences_first_day.xlsx", sheet=sheet_name)



graphelist <- list()





#graphes quantification pour une journée, moment: la moyenne de chaque individu pour le paramètre sur une journée
#utiliser la feuille excel qui contient la colonne moment, souvent "jour1", "jour2" ou stats

donnees_first_frame <- data %>%
  select(moment,catégorie,individu)
print(n=30,donnees_first_frame)

resume_stats2 <- donnees_first_frame %>%
  group_by(catégorie) %>%
  summarise(Moyenne = mean(moment,na.rm = TRUE),
            EcartType = sd(moment,na.rm = TRUE)/sqrt(90))
print(resume_stats2)
str(resume_stats2)
resume_stats2$catégorie <- factor(resume_stats2$catégorie)

couleurs <- c(s = "blue", i = "red", w = "black", t = "orange", ma= "purple", ms= "pink", fa= "green", fs="yellow")

diagramme_first_frame <- ggplot(donnees_first_frame, aes(x = catégorie, y = moment ,color = catégorie)) +
  geom_line(aes(linetype = "solid"), size = 1 ) +
  geom_point(size = 3) +
  geom_point(data = resume_stats2, aes(x = catégorie, y = Moyenne), color = "black", shape = 16, size = 3, group=1) +
  geom_errorbar(data = resume_stats2, aes(x = catégorie, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), width = 0.2, color = "black", group=1) +
  labs(title = "mouse at the lever 6 seconds before beam day7",
       x = "Strategy",
       y = "mouse at the lever ") +
  scale_fill_manual(values = couleurs) +  
  scale_color_manual(values = couleurs) +
  theme_minimal()

print(diagramme_first_frame)

#### test influence catégorie sur heure première séquence complète

##  test influence de la categorie sur le jour : moment: moyenne de la valeur sur toutes les heures de la journée
model_first_frame<- aov(moment~catégorie, data=data)
summary(model_first_frame)
## test comparaisons entre groupes 
comparaisons <- TukeyHSD(model_first_frame)
print(comparaisons)







#######graphe regroupement par 10 levers avant et après séquence complètes
sheet_name <- "regroupé"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/time_before_sequence1.xlsx", sheet=sheet_name)

donnees_long_regroupement <- data %>%
  pivot_longer(cols = c("0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80"),
               names_to = "Levers",
               values_to = "Nombre")



donnees_long_regroupement <- donnees_long_regroupement %>%
  select(individu, Levers, Nombre,categorie)
print(n=30,donnees_long_regroupement)

resume_stats_grp <- donnees_long_regroupement %>%
  group_by(Levers) %>%
  summarise(Moyenne = mean(Nombre,na.rm = TRUE),
            EcartType = sd(Nombre,na.rm = TRUE)/sqrt(87))
print(resume_stats_grp)


diagramme_regroupement <- ggplot(donnees_long_regroupement, aes(x = Levers, y = Nombre, group = individu)) +
  geom_line(aes(linetype = "solid"), size = 1, color = "blue") +
  geom_point(size = 3) +
  geom_point(data = resume_stats_grp, aes(x = Levers, y = Moyenne), color = "red", shape = 16, group = 1) +
  geom_errorbar(data = resume_stats_grp, aes(x = Levers, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), width = 0.5, color = "red", group = 1) +
  labs(title = "Time between lever and beam before and after the first complete sequence",
       x = "Levers",
       y = "Time mean between lever and beam") +
  
  theme_minimal()

print(diagramme_regroupement)





## regroupement par 10 levers avant et après séquence complètes, en faisant les moyennes par catégorie
donnees_long_regroupement <- data %>%
  pivot_longer(cols = c("0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80"),
               names_to = "Levers",
               values_to = "Nombre")



print(n = 30, donnees_long_regroupement)

resume_stats_grp <- donnees_long_regroupement %>%
  group_by(Levers,categorie) %>%
  summarise(Moyenne = mean(Nombre, na.rm = TRUE),
            EcartType = sd(Nombre, na.rm = TRUE) / sqrt(86))
print(n=50,resume_stats_grp)



diagramme_regroupement <- ggplot() +
  geom_line(data = resume_stats_grp, aes(x = Levers, y = Moyenne, group = categorie, color = categorie), linetype = "solid", size = 1) +
  geom_point(data = resume_stats_grp, aes(x = Levers, y = Moyenne, color = categorie), size = 3) +
  geom_errorbar(data = resume_stats_grp, aes(x = Levers, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType, color = categorie), width = 0.2) +
  labs(title = "Time between lever and beam before and after the first complete sequence",
       x = "Levers",
       y = "Time mean between lever and beam") +
  scale_color_manual(values = c("s" = "blue", "w" = "black", "i" = "red", "t" = "orange", "fa"="green", "fs"="yellow", "ma"="purple","ms"="pink")) +
  theme_minimal()

print(diagramme_regroupement)


## boxplot regroupement par 10 levers avant et après séquence complètes par catégorie


ggplot(donnees_long_regroupement, aes(x = Levers, y = Nombre, fill=categorie)) +
  geom_boxplot() +
  labs(title = "Moyennes des temps entre lever et beam avant la première séquence complète par catégorie",
       x = "Levers",
       y = "Nombre") +
  theme_minimal()











### tests influence heure et catégorie pour nombre et temps moyen avant et après first sequence complète

#model<- aov(Nombre~Temps*Category + Error(Individu/(Temps * Category)), data=donnees_long3)
#summary(model)
donnees_long3$Category <- factor(donnees_long3$Category)
head(donnees_long3)


## test différences d'appuis leviers avant et après 1 ère séquence complète
model_sc<- aov(Nombre~Temps*Category , data=donnees_long3)
summary(model_sc)

posthoc <- glht(model_sc, linfct = mcp( Category = "Tukey"))
summary(posthoc)


posthoc_bonferroni <- glht(model_sc, linfct = mcp(Category = "B"))
summary(posthoc_bonferroni)

### tests influence heure et catégorie pour nombre et temps moyen avant et après first sequence  complète par catégorie

donnees_long2$Category <- factor(donnees_long2$Category)
donnees_long2$cage <- factor(donnees_long2$cage)

head(donnees_long3)


## test différences d'appuis leviers avant et après 1 ère séquence complète
model_sc<- aov(Nombre~Temps*Category , data=donnees_long3)
summary(model_sc)


## test moyenne de temps entre lever et beam avant et après sequence par tranche de 10
head(donnees_long_regroupement)
unique(donnees_long_regroupement$catégorie)

donnees_long_regroupement$categorie<- factor(donnees_long_regroupement$categorie)
donnees_long_regroupement$Levers<- factor(donnees_long_regroupement$Levers)

model_groupe<-aov(Nombre~Levers* categorie , data=donnees_long_regroupement)
summary(model_groupe)
posthoc_groupe <- glht(model_groupe, linfct = mcp( Levers = "Tukey"))
summary(posthoc_groupe)

posthoc_tukey <- TukeyHSD(model_groupe, "Levers")
print(posthoc_tukey)
## graphes heure de la première séquence complète
#boxplot

ggplot(data, aes(x = Category, y = heure, fill = Category)) +
  geom_boxplot() +
  labs(title = "Boxplot time first sequence",
       x = "Catégorie",
       y = "Valeur") +
  theme_minimal()


#avec barres d'erreur heure première séquence

donnees_first_frame <- data %>%
  select(moment,catégorie,individu)
print(n=30,donnees_first_frame)

resume_stats2 <- donnees_first_frame %>%
  group_by(catégorie) %>%
  summarise(Moyenne = mean(moment,na.rm = TRUE),
            EcartType = sd(moment,na.rm = TRUE)/sqrt(90))
print(resume_stats2)
str(resume_stats2)
resume_stats2$catégorie <- factor(resume_stats2$catégorie)

couleurs <- c(s = "blue", i = "red", w = "black", t = "orange", ma= "purple", ms= "pink", fa= "green", fs="yellow")

diagramme_first_frame <- ggplot(donnees_first_frame, aes(x = catégorie, y = moment ,color = catégorie)) +
  geom_line(aes(linetype = "solid"), size = 1 ) +
  geom_point(size = 3) +
  geom_point(data = resume_stats2, aes(x = catégorie, y = Moyenne), color = "black", shape = 16, size = 3, group=1) +
  geom_errorbar(data = resume_stats2, aes(x = catégorie, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), width = 0.2, color = "black", group=1) +
  labs(title = "mouse at the lever 6 seconds before beam day2",
       x = "Strategy",
       y = "mouse at the lever ") +
  scale_fill_manual(values = couleurs) +  
  scale_color_manual(values = couleurs) +
  theme_minimal()

print(diagramme_first_frame)

#### test influence catégorie sur heure première séquence complète


model_first_frame<- aov(moment~catégorie, data=data)
summary(model_first_frame)
comparaisons <- TukeyHSD(model_first_frame)
print(comparaisons)

test_kruskal <- kruskal.test(moment ~ catégorie*individu, data = data)
print(test_kruskal)


#### test influence cage sur heure première séquence complète par catégorie

donnees_first_frame <- data %>%
  select(individu, heure,Category, cage)
print(n=30,donnees_first_frame)

donnees_first_frame$cage <- as.factor(donnees_first_frame$cage)

first_frame_filtre <- donnees_first_frame[donnees_first_frame$Category == "s", ]
model_first_frame_filtre<- aov(heure~cage, data=first_frame_filtre)
summary(model_first_frame_filtre)



posthoc_model_first_frame_filtre <- glht(model_first_frame_filtre, linfct = mcp(cage = "Tukey"))
summary(posthoc_model_first_frame_filtre)



###################

for (categorie in categories){
  colonnes_selectionnees<- colnames(data)[grepl(categorie, as.character(data[1,]))]
  donnees_filtrees <- select(data, séquence, colonnes_selectionnees)
  donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -séquence)
  donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
  
  donnees_liste[[categorie]] <- donnees_long
  
  graphique_agregate <- ggplot()+
    geom_point(data = donnees_liste[[categorie]], aes(x = séquence, y = Valeur, color = categorie), size = 2, alpha = 0.6) +
    labs(title = sprintf("séquences (%s)",categorie),
         x = "sequence",
         y = "Value",
         color = "Variable") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size=0.5, linetype = "dashed"))+
    scale_color_manual(values = c("blue", "green", "red"),
                     labels = c("s", "w", "i"))
  graphique_liste[[paste( categorie)]] <- graphique_agregate
  
}
grid.arrange(grobs = graphique_liste, ncol = 2)



#### first frame 

# 
# 
# moyennes <- data %>%
#   group_by(catégorie) %>%
#   summarise(moyenne = mean(moment))
# 
# # Calculer l'écart-type par catégorie
# ecart_types <- data %>%
#   group_by(catégorie) %>%
#   summarise(ecart_type = sd(moment)/87)
# 
# 
# 
# bar_plot <- ggplot(data, aes(x = catégorie, y = moyenne)) +
#   geom_bar(stat = "identity", fill = "blue", alpha = 0.7) +
#   geom_errorbar(aes(ymin = moyenne - ecart_type, ymax = moyenne + ecart_type), width = 0.4, color = "red", position = position_dodge(0.9)) +
#   labs(title = "Moyenne et Écart-type par Catégorie", x = "Catégorie", y = "Moyenne") +
#   theme_minimal()
# 
# # Afficher le graphique à barres
# print(bar_plot)
# 
# 
# 
# data$moment <- as.numeric(data$moment)
# 
# 
# moyennes <- data %>%
#   group_by(catégorie) %>%
#   summarise(moyenne = mean(moment,na.rm = TRUE))
# 
# # Calculer l'écart-type par catégorie
# ecart_types <- data %>%
#   group_by(catégorie) %>%
#   summarise(ecart_type = sd(moment,na.rm = TRUE)/87)
# 
# # Créer un graphique à barres avec la moyenne par catégorie
# bar_plot <- ggplot(data, aes(x = catégorie, y = moment)) +
#   geom_bar(stat = "identity", fill = "blue", alpha = 0.7) +
#   geom_errorbar(aes(ymin = moyenne - ecart_types$ecart_type, ymax = moyennes$moyenne + ecart_types$ecart_type), width = 0.4, color = "red", position = position_dodge(0.9)) +
#   labs(title = "Moyenne et Écart-type par Catégorie", x = "Catégorie", y = "Moyenne") +
#   theme_minimal()
# 
# # Afficher le graphique à barres
# print(bar_plot)



### boxplot heure de la première séquence complète

box_plot <- ggplot(data, aes(x = catégorie, y = moment, fill = catégorie)) +
  geom_boxplot() +
  labs(title = "Boxplot par Catégorie", x = "Catégorie", y = "Valeur") +
  theme_minimal()

# Afficher le boxplot
print(box_plot)


########################## graphe par groupe avec nombre de levers avant et après la première séquence complète
sheet_name2 <- "moyennes"
data2 <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/time_between_sequence12.xlsx", sheet=sheet_name2)
diagramme <- ggplot(data2, aes(x = Individu, y = Number_before, group = Individu)) +
  geom_line(aes(color = "Temps 1"), size = 1) +
  geom_point(aes(color = "Temps 1"), size = 3) +
  geom_line(aes(y = Number_after, color = "Temps 2"), size = 1, linetype = "dashed") +
  geom_point(aes(y = Number_after, color = "Temps 2"), size = 3) +
  labs(title = "Number of levers before and after the first  complete sequence",
       x = "Individu",
       y = "numebr of levers") +
  scale_color_manual(values = c("Temps 1" = "blue", "Temps 2" = "red")) +
  theme_minimal()

print(diagramme)

############## graphe avec points reliés; nombre de leviers avant la première sequence et entre les deux premières, en filtrant la catégorie
## avec "time_before_sequence" et "time_between_sequences_12"

donnees_long2 <- data2 %>%
  pivot_longer(cols = c(Number_before,Number_after),
               names_to = "Temps",
               values_to = "Nombre") %>%
  filter(Category == "s")
#filter(Category=="i") 

donnees_long2 <- donnees_long2 %>%
  select(Individu, Temps, Nombre)
print(n=30,donnees_long2)

resume_stats <- donnees_long2 %>%
  group_by(Temps) %>%
  summarise(Moyenne = mean(Nombre),
            EcartType = sd(Nombre)/sqrt(22))
print(resume_stats)
resume_stats <- left_join(resume_stats, donnees_long2 %>% distinct(Individu, Temps), by = "Temps")

diagramme2 <- ggplot(donnees_long2, aes(x = Temps, y = Nombre, group=Individu ,color = Temps)) +
  geom_line(aes(linetype = "solid"), size = 1, color="blue") +
  geom_point(size = 3,color="blue") +
  geom_point(data = resume_stats, aes(x = Temps, y = Moyenne), color = "red", shape = 16, size = 3) +
  geom_errorbar(data = resume_stats, aes(x = Temps, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), width = 0.2, color = "red") +
  labs(title = "Number of levers before and after the first  complete sequence for scroungers mice",
       x = "Time",
       y = "Number of levers") +
  theme_minimal()

print(diagramme2)

####### graphe avec points reliés; nombre de leviers avant la première sequence et entre les deux premières avec tous les individus

donnees_long3 <- data2 %>%
  pivot_longer(cols = c(Number_before,Number_after),
               names_to = "Temps",
               values_to = "Nombre") 

donnees_long3 <- donnees_long3 %>%
  select(Individu, Temps, Nombre,Category)
print(n=30,donnees_long3)

resume_stats2 <- donnees_long3 %>%
  group_by(Temps) %>%
  summarise(Moyenne = mean(Nombre,na.rm = TRUE),
            EcartType = sd(Nombre,na.rm = TRUE)/sqrt(48))
print(resume_stats2)


diagramme2 <- ggplot(donnees_long3, aes(x = Temps, y = Nombre, group=Individu ,color = Temps)) +
  geom_line(aes(linetype = "solid"), size = 1, color="blue") +
  geom_point(size = 3, color="black") +
  geom_point(data = resume_stats2, aes(x = Temps, y = Moyenne), color = "red", shape = 16, size = 3, group=1) +
  geom_errorbar(data = resume_stats2, aes(x = Temps, y = Moyenne, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), width = 0.2, color = "red", group=1) +
  labs(title = "Number of lever and beam before and after the first  complete sequence",
       x = "Time",
       y = "Number of lever and beam") +
  theme_minimal()

print(diagramme2)







print(data2)
ggplot(data2, aes(x = Category, y = Number_before, fill = Category)) +
  geom_boxplot() +
  labs(title = "Moyennes des temps entre lever et beam avant la première séquence complète par catégorie",
       x = "Catégorie",
       y = "Valeur") +
  theme_minimal()

ggplot(data2, aes(x = Category, y = Time_before, fill = Category)) +
  geom_boxplot() +
  labs(title = "Boxplot avec nombre de leverpress avant la première séquence complète par catégorie",
       x = "Catégorie",
       y = "Valeur") +
  theme_minimal()









data2_long <- data2 %>%
  pivot_longer(cols = c("Time_before", "Time_after"), names_to = "Variable", values_to = "Value")

#  boxplot pour les temps avant la séquence complète entre beam et lever
ggplot(data2_long, aes(x = Category, y = Value, fill = Category)) +
  geom_boxplot() +
  facet_grid(. ~ Variable, scales = "free_y", space = "free_y") +
  labs(title = "Moyennes des temps entre lever et beam avant et après la première séquence complète par catégorie",
       x = "Catégorie",
       y = "Valeur") +
  theme_minimal()

data2_long <- data2 %>%
  pivot_longer(cols = c("Number_before", "Number_after"), names_to = "Variable", values_to = "Value")

#  boxplot pour le nombre d'essai avant la première séquence complète
ggplot(data2_long, aes(x = Category, y = Value, fill = Category)) +
  geom_boxplot() +
  facet_grid(. ~ Variable, scales = "free_y", space = "free_y") +
  labs(title = "Nombre de levers suivis d'un beam avant et après la première séquence complète par catégorie",
       x = "Catégorie",
       y = "Valeur") +
  theme_minimal()

