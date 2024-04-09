library(readxl)
library(ggplot2)
library(dplyr)
library(tidyr)
library(gridExtra) 
library(readr) 
library(dunn.test)
library(lsmeans)
library(MASS)
library(lme4)

sheet_name <- "jour1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_sequences_first_day.xlsx", sheet= sheet_name)
data$catégorie <- as.factor(data$catégorie)
print(data$catégorie)
print(data)
significant_hours <- c() 

### test influence heure et catégorie sur nombre séquences
donnees_long <- data %>%
  gather(key = "Heure", value = "Mesure", -individu, -catégorie)
head(donnees_long)
print(donnees_long)
print(donnees_long$Mesure)
donnees <- donnees_long %>%
  mutate(individu = as.character(individu),
         catégorie = as.character(catégorie),
         Heure = as.character(Heure),
         Mesure = as.numeric(Mesure))
print(donnees, n=100)

modele <- aov( Mesure ~ Heure* catégorie , data= donnees)
summary(modele)

comparaisons <- TukeyHSD(modele)
print(comparaisons)

donnees<-c()


##test à une heure précise
kruskal.test(heure15 ~ catégorie, data = data)
dunn_res <- dunn.test(data$heure15, data$catégorie, method = "bonferroni")
print(dunn_res)




## test heures où les différences sont significatives
length(heure_col_vector)
length(data$catégorie)
 for (heure in c(1:24)) {
  heure_col <- paste0("heure", heure)
  
  # Sélectionner les données de l'heure en cours
  heure_col_vector <- as.numeric(data[[heure_col]])
  
  # Effectuer le test de Kruskal-Wallis
  kruskal_res <- kruskal.test(heure_col_vector ~ data$catégorie)
  
  # Si le test est significatif
  if (kruskal_res$p.value < 0.05) {
    # Effectuer le test de Dunn avec ajustement de Bonferroni
    significant_hours <- c(significant_hours, heure_col)
    dunn_res <- dunn.test(heure_col_vector, data$catégorie, method = "bonferroni")
    
    # Afficher les résultats
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
}

print(significant_hours)

## heures où les heures sont significatives deux à deux
significant_hours_fii <- c()
significant_hours_fis <- c()
significant_hours_is <- c()
significant_hours_fit <- c()
significant_hours_it <- c() 
significant_hours_st <- c()
significant_hours_fiw <- c()
significant_hours_iw <- c()
significant_hours_sw <- c()
significant_hours_tw <- c()

for (heure in c(1:24)) {
  heure_col <- paste0("heure", heure)
  
  heure_col_vector <- as.numeric(data[[heure_col]])
  
  
  dunn_res <- dunn.test(heure_col_vector, data$catégorie, method = "bonferroni")
  if (dunn_res$P.adjusted[1] < 0.05){
    significant_hours_fii <- c(significant_hours_fii, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
    
  }
  if (dunn_res$P.adjusted[2] < 0.05){
    significant_hours_fis <- c(significant_hours_fis, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
    
  }
  if (dunn_res$P.adjusted[3] < 0.05){
    significant_hours_is <- c(significant_hours_is, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[4] < 0.05){
    significant_hours_fit <- c(significant_hours_fit, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[5] < 0.05){
    significant_hours_it <- c(significant_hours_it, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[6] < 0.05){
    significant_hours_st <- c(significant_hours_st, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[7] < 0.05){
    significant_hours_fiw <- c(significant_hours_fiw, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[8] < 0.05){
    significant_hours_iw <- c(significant_hours_iw, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[9] < 0.05){
    significant_hours_sw <- c(significant_hours_sw, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
  if (dunn_res$P.adjusted[10] < 0.05){
    significant_hours_tw <- c(significant_hours_tw, heure_col)
    print(paste("Résultats pour", heure_col))
    print(kruskal_res)
    print(dunn_res)
  }
}
print(significant_hours_fii)
print(significant_hours_fis)
print(significant_hours_is) 
print(significant_hours_fit)
print(significant_hours_it) 
print(significant_hours_st)
print(significant_hours_fiw)
print(significant_hours_iw)
print(significant_hours_sw)
print(significant_hours_tw)





### test influence catégorie sur stolen levers

donnees_long_stolen <- data %>%
  gather(key = "Heure", value = "Mesure", -individu, -voleuse, -volée)
head(donnees_long_stolen)
print(donnees_long_stolen)

donnees_stolen <- donnees_long_stolen %>%
  mutate(individu = as.character(individu),
         catégorie = as.character(volée),
         Heure = as.character(Heure),
         Mesure = as.numeric(Mesure))

modele_stolen <- aov( Mesure ~ Heure* volée , data= donnees_stolen)
summary(modele_stolen)

comparaisons <- TukeyHSD(modele_stolen)

# Affichez les résultats
print(comparaisons)



####### test influence heure et cage pour une catégorie donnée sur nombre séquences

donnees_long_categorie <- data %>%
  gather(key = "Heure", value = "Mesure", -individu, -catégorie, -cage)
head(donnees_long_categorie)

donnees_categorie <- donnees_long_categorie %>%
  mutate(individu = as.character(individu),
         catégorie = as.character(catégorie),
         Heure = as.character(Heure),
         Mesure = as.numeric(Mesure),
         cage=as.factor(cage))
         

donnees_categorie_filtre <- donnees_categorie[donnees_categorie$catégorie == "i", ]
model_cage<- aov(Mesure~Heure*cage, data=donnees_categorie_filtre)
summary(model_cage)


posthoc_tukey_categorie_s <- glht(model_cage, linfct = mcp(cage = "Tukey"))
summary(posthoc_tukey_categorie_s)








