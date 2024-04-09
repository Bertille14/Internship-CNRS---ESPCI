library(readxl)
library(ggplot2)
library(dplyr)
library(tidyr)
library(gridExtra) 
library(readr) 
library(dunn.test)
library(lsmeans)
install.packages("dplyr")


sheet_name <- "jour1"
sheet_name2 <- "alone"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx", sheet= sheet_name2)
data2 <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_unfollowed_lever_first_day.xlsx", sheet= sheet_name2)
data_lever<- read_excel("C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx",sheet = sheet_name2)


data$catégorie <- as.factor(data$catégorie)
str(data)
str(data$catégorie)




categories<-c("i","s","t","w","fa","fs","ma","ms")

### graphe qui fonctionne pour les beams, sequences etc 
#utiliser sheet alone 

sheet_name2 <- "alone"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx", sheet= sheet_name2)

categories<-c("i","s","t","w","fa","fs","ma","ms")
graphique_liste<-list()
for (jour in jours) {
  donnees_liste <- list()
  
  for (categorie in categories) {
    colonnes_condition_s <- colnames(data)[grepl(categorie, as.character(data[1,]))]
    colonnes_condition_jour <- colnames(data)[grepl(jour, as.character(data[2,]))]
    colonnes_selectionnees <- intersect(colonnes_condition_s, colonnes_condition_jour)
    
    donnees_filtrees <- select(data, Hour, colonnes_selectionnees)
    print(donnees_filtrees)
    donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Hour)
    donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
    
    donnees_agregate <- donnees_long %>%
      group_by(Hour) %>%
      summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(130))
    print(donnees_agregate)
    donnees_liste[[categorie]] <- donnees_agregate
  }
  
  graphique_agregate <- ggplot() +
    geom_line(data = donnees_liste[["s"]], aes(x = Hour, y = Moyenne, group = 1, color = "scroungers"), size = 1) +
    geom_ribbon(data = donnees_liste[["s"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "blue", alpha=0.2) +
    geom_line(data = donnees_liste[["w"]], aes(x = Hour, y = Moyenne, group = 1, color = "workers"), size = 1) +
    geom_ribbon(data = donnees_liste[["w"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "black", alpha=0.2) +
    geom_line(data = donnees_liste[["i"]], aes(x = Hour, y = Moyenne, group = 1, color = "independents"), size = 1) +
    geom_ribbon(data = donnees_liste[["i"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "red", alpha=0.2) +
    geom_line(data = donnees_liste[["t"]], aes(x = Hour, y = Moyenne, group = 1, color = "storers"), size = 1) +
    geom_ribbon(data = donnees_liste[["t"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "orange", alpha=0.2) +
    geom_line(data = donnees_liste[["fa"]], aes(x = Hour, y = Moyenne, group = 1, color = "females achievers"), size = 1) +
    geom_ribbon(data = donnees_liste[["fa"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "green", alpha=0.2) +
    geom_line(data = donnees_liste[["ma"]], aes(x = Hour, y = Moyenne, group = 1, color = "males achievers"), size = 1) +
    geom_ribbon(data = donnees_liste[["ma"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "purple", alpha=0.2) +
    geom_line(data = donnees_liste[["ms"]], aes(x = Hour, y = Moyenne, group = 1, color = "males storers"), size = 1) +
    geom_ribbon(data = donnees_liste[["ms"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "pink", alpha=0.5) +
    geom_line(data = donnees_liste[["fs"]], aes(x = Hour, y = Moyenne, group = 1, color = "females storers"), size = 1) +
    geom_ribbon(data = donnees_liste[["fs"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "yellow", alpha=0.2) +
    labs(title = sprintf("Number sequences (%s)", jour),
         x = "Time (hour)",
         y = " sequences  ",
         color = "strategy") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
    scale_color_manual(values = c("scroungers" = "blue", "workers" = "black", "independents" = "red", "storers" = "orange", "females achievers"="green", "males achievers"="purple", "males storers"="pink", "females storers"="yellow"),
                       labels = c("scroungers" = "Scroungers", "workers" = "Workers", "independents" = "Independents", "storers" = "Storers", "females achievers"="Females achievers", "males achievers"="Males achievers", "males storers"="Males storers", "females storers"="Females storers")) +
    scale_fill_manual(values = c("blue", "black", "red", "orange", "green", "purple", "pink", "yellow"))
  
  graphique_liste[[jour]] <- graphique_agregate
}

grid.arrange(grobs = graphique_liste, ncol = 1)

## graphe qui fonctionne pour seulement triades 
graphique_liste2<- list()
jours<- c("jour1","jour2")
categories<- c("w","i","s","t")

sheet_name2 <- "Sheet1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx", sheet= sheet_name2)

for (jour in jours) {
  donnees_liste <- list()
  
  for (categorie in categories) {
    colonnes_condition_s <- colnames(data)[grepl(categorie, as.character(data[2,]))]
    colonnes_condition_jour <- colnames(data)[grepl(jour, as.character(data[3,]))]
    colonnes_selectionnees <- intersect(colonnes_condition_s, colonnes_condition_jour)
    
    donnees_filtrees <- select(data, Hour, colonnes_selectionnees)
    print(donnees_filtrees)
    donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Hour)
    donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
    
    donnees_agregate <- donnees_long %>%
      group_by(Hour) %>%
      summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(84))
    print(donnees_agregate)
    donnees_liste[[categorie]] <- donnees_agregate
  }
  
  graphique_agregate2 <- ggplot() +
    geom_line(data = donnees_liste[["s"]], aes(x = Hour, y = Moyenne, group = 1, color = "scroungers"), size = 1) +
    geom_ribbon(data = donnees_liste[["s"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "blue", alpha=0.2) +
    geom_line(data = donnees_liste[["w"]], aes(x = Hour, y = Moyenne, group = 1, color = "workers"), size = 1) +
    geom_ribbon(data = donnees_liste[["w"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "black", alpha=0.2) +
    geom_line(data = donnees_liste[["i"]], aes(x = Hour, y = Moyenne, group = 1, color = "independents"), size = 1) +
    geom_ribbon(data = donnees_liste[["i"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "red", alpha=0.2) +
    geom_line(data = donnees_liste[["t"]], aes(x = Hour, y = Moyenne, group = 1, color = "storers"), size = 1) +
    geom_ribbon(data = donnees_liste[["t"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                color = NA, group = 1, fill = "orange", alpha=0.2) +
    labs(title = sprintf("mouse at the lever 6 seconds before beam (%s)", jour),
         x = "Time (hour)",
         y = " mouse at the lever  ",
         color = "strategy") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
    scale_color_manual(values = c("scroungers" = "blue", "workers" = "black", "independents" = "red", "storers" = "orange"),
                       labels = c("scroungers" = "Scroungers", "workers" = "Workers", "independents" = "Independents", "storers" = "Storers")) +
    scale_fill_manual(values = c("blue", "black", "red", "orange", "green", "purple", "pink", "yellow"))
  
  graphique_liste2[[jour]] <- graphique_agregate2
}

grid.arrange(grobs = graphique_liste2, ncol = 1)





####tout sur un graphe différent##############################################################################################

sheet_name2 <- "Sheet1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx", sheet= sheet_name2)


graphique_liste <- list()
categories <- c("s","w","i","t")
jours <- c("jour1", "jour2")
for (jour in jours){
  for (categorie in categories){
    
    
    colonnes_condition_s <- colnames(data)[grepl(categorie, as.character(data[2, ]))]
    colonnes_condition_jour1 <- colnames(data)[grepl(jour, as.character(data[3, ]))]
    colonnes_selectionnees<- intersect(colonnes_condition_s,colonnes_condition_jour1)
    
    print(colonnes_selectionnees)
    
    donnees_filtrees <- select(data, Hour, colonnes_selectionnees)
    donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Hour)
    print(donnees_long)
    donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur),na.rm=TRUE)
    
    
    donnees_agregate <- donnees_long %>%
      group_by(Hour) %>%
      summarize(Moyenne = mean(Valeur,na.rm = TRUE), EcartType = sd(Valeur,na.rm = TRUE)/sqrt(48))
    
    graphique_agregate <- ggplot(donnees_agregate, aes(x = Hour, y = Moyenne, color = "Moyenne")) +
      geom_line(size = 1) +
      geom_ribbon(aes(ymin = Moyenne - EcartType, ymax = Moyenne + EcartType), alpha = 0.2, fill = "blue", color = NA) +
      labs(title = sprintf("sequences par heure (%s, %s)", categorie, jour),
           x = "Hour",
           y = "Moyenne +/- Ecart-Type sequences ",
           color = "Variable") +
      theme_minimal() +
      theme(panel.grid = element_blank(),
            panel.grid.major = element_line(color = "gray", size=0.5, linetype = "dashed"))
    graphique_liste[[paste( categorie, jour)]] <- graphique_agregate
  }
}


grid.arrange(grobs = graphique_liste, ncol = 2)


### graphe des levers  par heure sur les deux premiers jours

sheet_name2 <- "Sheet1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_lever_first_day.xlsx", sheet= sheet_name2)

graphique_liste1 <- list()
print(graphique_liste1)
for (jour in jours){
  colonnes_jour<- colnames(data)[grepl(jour, as.character(data[3,]))]
  donnees_jour<- select(data, Hour, colonnes_jour)
  donnees_long <- gather(donnees_jour, key = "Variable", value = "Valeur", -Hour)
  donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
  
  donnees_lever <- donnees_long %>%
    group_by(Hour) %>%
    summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(48))
  
  graphique_lever <- ggplot() +
    geom_line(data = donnees_lever, aes(x = Hour, y = Moyenne, color ="mean_lever"), size = 1) +
    geom_ribbon(data = donnees_lever, aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "red", color = NA) +
    labs(title = sprintf("Lever per hour (%s)", jour),
         x = "Hour",
         y = "Mean +/- standard deviation lever",
         color = "") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed"))
  graphique_liste1[[jour]] <- graphique_lever
}
grid.arrange(grobs = graphique_liste1, ncol = 2)


# graphe unfollowed levers 

sheet_name2="Sheet1"
data2 <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/number_unfollowed_lever_first_day.xlsx", sheet= sheet_name2)

categories <- c("s", "w", "i")
jours <- c("jour1", "jour2")

for (jour in jours) {
  donnees_liste <- list()
  
  for (categorie in categories) {
    colonnes_condition_s <- colnames(data2)[grepl(categorie, as.character(data2[1,]))]
    colonnes_condition_jour <- colnames(data2)[grepl(jour, as.character(data2[2,]))]
    colonnes_selectionnees <- intersect(colonnes_condition_s, colonnes_condition_jour)
    
    donnees_filtrees <- select(data2, Hour, colonnes_selectionnees)
    donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Hour)
    donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
    
    donnees_agregate <- donnees_long %>%
      group_by(Hour) %>%
      summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(48))
    print(donnees_agregate)
    
    donnees_liste[[categorie]] <- donnees_agregate
  }
  
  graphique_agregate <- ggplot() +
    geom_line(data = donnees_liste[["s"]], aes(x = Hour, y = Moyenne, color ="blue"), size = 1) +
    geom_ribbon(data = donnees_liste[["s"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "blue", color = NA) +
    geom_line(data = donnees_liste[["w"]], aes(x = Hour, y = Moyenne, color ="green"), size = 1) +
    geom_ribbon(data = donnees_liste[["w"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "green", color = NA) +
    geom_line(data = donnees_liste[["i"]], aes(x = Hour, y = Moyenne, color ="red"), size = 1) +
    geom_ribbon(data = donnees_liste[["i"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "red", color = NA) +
    labs(title = sprintf("Unfollowed lever per hour (%s)", jour),
         x = "Hour",
         y = "Moyenne +/- Ecart-Type ",
         color = "Variable") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
    scale_color_manual(values = c("blue", "green", "red"),
                       labels = c("s", "w", "i"))
  graphique_liste[[jour]] <- graphique_agregate
}

grid.arrange(grobs = graphique_liste, ncol = 2)


# graphe accumulation entre beams ou levers

sheet_name2="graphe"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/accumulation_between_beams.xlsx", sheet= sheet_name2)


categories <- c("m", "f", "ma", "fa")
graphique_liste <- list()

jours <- c("jour4")

for (jour in jours) {
  for (categorie in categories) {
    colonnes_condition_s <- colnames(data)[grepl(categorie, as.character(data[,]))]
    colonnes_condition_jour <- colnames(data)[grepl(jour, as.character(data[2,]))]
    colonnes_selectionnees <- intersect(colonnes_condition_s, colonnes_condition_jour)
    print(colonnes_selectionnees)
    
    donnees_filtrees <- select(data, Lever, colonnes_selectionnees)
    donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Lever)
    donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
    
    donnees_agregate <- donnees_long %>%
      group_by(Lever) %>%
      summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(67))
    print(donnees_agregate)
    donnees_liste[[categorie]] <- donnees_agregate
  }
  
  graphique_agregate <- ggplot() +
    geom_line(data = donnees_liste[["m"]], aes(x = Lever, y = Moyenne), color ="blue", size = 1) +
    geom_ribbon(data = donnees_liste[["m"]], aes(x = Lever, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "blue", color = NA) +
    geom_line(data = donnees_liste[["f"]], aes(x = Lever, y = Moyenne), color ="black", size = 1) +
    geom_ribbon(data = donnees_liste[["f"]], aes(x = Lever, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "black", color = NA) +
    geom_line(data = donnees_liste[["ma"]], aes(x = Lever, y = Moyenne), color ="red", size = 1) +
    geom_ribbon(data = donnees_liste[["ma"]], aes(x = Lever, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "red", color = NA) +
    geom_line(data = donnees_liste[["fa"]], aes(x = Lever, y = Moyenne ),color ="orange", size = 1) +
    geom_ribbon(data = donnees_liste[["fa"]], aes(x = Lever, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                alpha = 0.2, fill = "orange", color = NA) +
    labs(title = sprintf("temps entre lever et beam entre deux séquences complètes (%s)", jour),
         x = "Lever",
         y = "Moyenne +/- Ecart-Type",
         color = "Variable") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
    scale_color_manual(values = c("blue", "green", "red","orange"),
                       labels = c("m", "f", "ma","fa"))
  graphique_liste[[paste("Graph_", jour, sep = "")]]<- graphique_agregate
}


grid.arrange(grobs = graphique_liste, ncol = 1)





##### graphe mouse position when a lever is done ###########################################################################################
sheet_name2="Sheet1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/position_apres_lever_beam.xlsx", sheet= sheet_name2)


graphique_liste<- list()
categories <- c("s","i","w","t")
graphique_agregate<-ggplot()

donnees_liste <- list()

for (categorie in categories) {
  colonnes_condition_lever <- colnames(data)[grepl("w", as.character(data[1,]))]
  colonnes_condition_position_other_mouse <- colnames(data)[grepl(categorie, as.character(data[2,]))]
  
  colonnes_selected <- intersect(colonnes_condition_lever, colonnes_condition_position_other_mouse)
  
  
  
  donnees_filtrees <- select(data, Hour, colonnes_selected)
  print(donnees_filtrees)
  donnees_long <- pivot_longer(donnees_filtrees, cols = -Hour, names_to = "Variable", values_to = "Valeur")
  donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
  donnees_long$Hour <- as.numeric(as.character(donnees_long$Hour), na.rm = TRUE)
  print(donnees_long)
  
  donnees_agregate <- donnees_long %>%
    group_by(Hour) %>%
    summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(174))
  print(donnees_agregate)
  
  donnees_liste[[categorie]] <- donnees_agregate
  print(donnees_liste[[categorie]])
}



for (categorie in categories) {
  if (length(donnees_liste[[categorie]]) > 0) {
    graphique_agregate <- graphique_agregate +
      geom_line(data = donnees_liste[[categorie]], aes(x = Hour, y = Moyenne, linetype= categorie, color=categorie, group = 1), size = 1,
                group = 1, color = ifelse(categorie == "s", "blue", ifelse(categorie == "i", "red", ifelse(categorie == "t", "orange", ifelse(categorie == "w", "black", "green")))))+
      geom_ribbon(data = donnees_liste[[categorie]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                  color = NA, group = 1, fill = ifelse(categorie == "s", "blue", ifelse(categorie == "i", "red", ifelse(categorie == "t", "orange", ifelse(categorie == "w", "black", "green")))))
  }
}

graphique_agregate <- graphique_agregate +
  labs(title = "position ",
       x = "Time (hour)",
       y = "Number of levers",
       color = "Catégorie") +
  theme_minimal() +
  theme(panel.grid = element_blank(),
        panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
  scale_color_manual(values = c("s" = "blue", "w" = "black", "i" = "red", "t" = "orange"))+
  scale_linetype_manual(values = c("s" = "solid", "w" = "solid", "i" = "solid", "fi" = "solid", "t" = "solid"))

print(graphique_agregate)



### graphes stolen levers

sheet_name2="Sheet1"
data <- read_excel( "C:/Users/LMT3-B7bis/Desktop/bm stage/stolen_levers.xlsx", sheet= sheet_name2)
colonnes_selected <- intersect(colonnes_condition_s, colonnes_condition_jour)

graphique_liste<- list()
categories <- c("s","i","w","t")
graphique_agregate<-ggplot()

donnees_liste <- list()
  
for (categorie in categories) {
  colonnes_condition_voleuse <- colnames(data)[grepl(categorie, as.character(data[2,]))]
  ## mettre as.character(data[3,]) pour avoir la souris qui se fait voler
  #colonnes_condition_volée <- colnames(data)[grepl(categorie, as.character(data[2,]))]
  
  
  
  
  donnees_filtrees <- select(data, Hour, colonnes_condition_voleuse)
  print(donnees_filtrees)
  donnees_long <- pivot_longer(donnees_filtrees, cols = -Hour, names_to = "Variable", values_to = "Valeur")
  donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
  donnees_long$Hour <- as.numeric(as.character(donnees_long$Hour), na.rm = TRUE)
  print(donnees_long)
  
  donnees_agregate <- donnees_long %>%
    group_by(Hour) %>%
    summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(174))
  print(donnees_agregate)
  
  donnees_liste[[categorie]] <- donnees_agregate
  print(donnees_liste[[categorie]])
}



for (categorie in categories) {
  if (length(donnees_liste[[categorie]]) > 0) {
    graphique_agregate <- graphique_agregate +
      geom_line(data = donnees_liste[[categorie]], aes(x = Hour, y = Moyenne, linetype= categorie, color=categorie, group = 1), size = 1,
       group = 1, color = ifelse(categorie == "s", "blue", ifelse(categorie == "i", "red", ifelse(categorie == "t", "orange", ifelse(categorie == "w", "black", "green")))))+
      geom_ribbon(data = donnees_liste[[categorie]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
                  color = NA, group = 1, fill = ifelse(categorie == "s", "blue", ifelse(categorie == "i", "red", ifelse(categorie == "t", "orange", ifelse(categorie == "w", "black", "green")))))
  }
}

graphique_agregate <- graphique_agregate +
  labs(title = "Number of levers that were stolen by another mouse ",
       x = "Time (hour)",
       y = "Number of levers",
       color = "Catégorie") +
  theme_minimal() +
  theme(panel.grid = element_blank(),
        panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
  scale_color_manual(values = c("s" = "blue", "w" = "black", "i" = "red", "t" = "orange"))+
  scale_linetype_manual(values = c("s" = "solid", "w" = "solid", "i" = "solid", "fi" = "solid", "t" = "solid"))

print(graphique_agregate)

categorie<- list()










## essais 
categories <- c("s","i","w","t")
data$Hour <- as.numeric(data$Hour)
donnees_liste <- list()

# Loop through each category
for (categorie in categories) {
  
  # Get column names for the stolen and thief categories
  colonnes_condition_lever <- colnames(data_lever)[grepl(categorie, as.character(data[1,]))]
  colonnes_condition_volée <- colnames(data)[grepl(categorie, as.character(data[2,]))]
  
  # Select relevant columns and pivot the data
  donnees_filtrees_lever <- select(data_lever, Hour, colonnes_condition_lever)
  donnees_filtrees_stolen <- select(data, Hour, colonnes_condition_volée)
  print(donnees_filtrees_lever)
  
  # Count occurrences of stealing and being stolen
  donnees_agregate_lever <- donnees_filtrees_lever %>%
    group_by(Hour) %>%
    summarize(leverCount = sum(!is.na(.), na.rm = TRUE))
  print(donnees_agregate_lever)
  
  donnees_agregate_stolen <- donnees_filtrees_stolen %>%
    group_by(Hour) %>%
    summarize(StolenCount = sum(!is.na(.), na.rm = TRUE))
  
  # Merge the two counts and calculate the ratio
  donnees_agregate <- merge(donnees_agregate_lever, donnees_agregate_stolen, by = "Hour", all = TRUE)
  donnees_agregate$Ratio <- donnees_agregate$StolenCount / donnees_agregate$LeverCount
  
  # Store the results in the list
  donnees_liste[[categorie]] <- donnees_agregate
  print(donnees_agregate)
}

# Plotting
graphique_agregate2 <- ggplot()

for (categorie in categories) {
  if (length(donnees_liste[[categorie]]) > 0) {
    graphique_agregate2 <- graphique_agregate2 +
      geom_line(data = donnees_liste[[categorie]], aes(x = Hour, y = Ratio, linetype = categorie, color = categorie, group = 1), size = 1) +
      geom_ribbon(data = donnees_liste[[categorie]], aes(x = Hour, ymin = Ratio - 0.05, ymax = Ratio + 0.05),
                  color = NA, alpha = 0.2, group = 1, fill = ifelse(categorie == "s", "blue", ifelse(categorie == "i", "red", ifelse(categorie == "fi", "orange", ifelse(categorie == "t", "purple", "green")))))
  }
}

graphique_agregate2 <- graphique_agregate2 +
  labs(title = "Ratio of stealing to being stolen per hour",
       x = "Hour",
       y = "Ratio",
       color = "Catégorie") +
  theme_minimal() +
  theme(panel.grid = element_blank(),
        panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
  scale_color_manual(values = c("s" = "blue", "i" = "red", "fi" = "orange", "t" = "purple", "w" = "green")) +
  scale_linetype_manual(values = c("s" = "solid", "i" = "solid", "fi" = "solid", "t" = "solid", "w" = "solid"))

print(graphique_agregate2)



### graphe pour chaque catégorie

plots_list <- list()

for (categorie in categories) {
  if (length(donnees_liste[[categorie]]) > 0) {
    plot <- ggplot(donnees_liste[[categorie]], aes(x = Hour, y = Ratio, linetype = categorie, color = categorie)) +
      geom_line(size = 1) +
      geom_ribbon(aes(ymin = Ratio - 0.05, ymax = Ratio + 0.05), color = NA, alpha = 0.2) +
      labs(title = paste("Ratio of stealing to being stolen per hour -", categorie),
           x = "Hour",
           y = "Ratio",
           color = "Catégorie") +
      theme_minimal() +
      theme(panel.grid = element_blank(),
            panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
      scale_color_manual(values = c("s" = "blue", "i" = "red", "fi" = "orange", "t" = "purple", "w" = "green")) +
      scale_linetype_manual(values = c("s" = "solid", "i" = "solid", "fi" = "solid", "t" = "solid", "w" = "solid"))
    
    plots_list[[categorie]] <- plot
  }
}

# Display the plots
for (i in seq_along(plots_list)) {
  print(plots_list[[i]])
}




# tout sur le même graphe

# 
# 
# 
# graphique_liste<- list()
# categories <- c("s", "w", "i","t")
# jours <- c("jour1", "jour2")
# 
# for (jour in jours) {
#   donnees_liste <- list()
#   
#   for (categorie in categories) {
#     colonnes_condition_s <- colnames(data)[grepl(categorie, as.character(data[2,]))]
#     colonnes_condition_jour <- colnames(data)[grepl(jour, as.character(data[3,]))]
#     colonnes_selectionnees <- intersect(colonnes_condition_s, colonnes_condition_jour)
#     
#     donnees_filtrees <- select(data, Hour, colonnes_selectionnees)
#     donnees_long <- gather(donnees_filtrees, key = "Variable", value = "Valeur", -Hour)
#     donnees_long$Valeur <- as.numeric(as.character(donnees_long$Valeur), na.rm = TRUE)
#     
#     donnees_agregate <- donnees_long %>%
#       group_by(Hour) %>%
#       summarize(Moyenne = mean(Valeur, na.rm = TRUE), EcartType = sd(Valeur, na.rm = TRUE)/sqrt(48))
#     print(donnees_agregate)
#     
#     
#     donnees_liste[[categorie]] <- donnees_agregate
#   }
#   
#   graphique_agregate <- ggplot() +
#     geom_line(data = donnees_liste[["s"]], aes(x = Hour, y = Moyenne), color ="blue",group=1, size = 1,show.legend = TRUE) +
#     geom_ribbon(data = donnees_liste[["s"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
#                 alpha = 0.2, color = NA, group=1, fill="blue") +
#     geom_line(data = donnees_liste[["w"]], aes(x = Hour, y = Moyenne), color ="green", group=1, size = 1) +
#     geom_ribbon(data = donnees_liste[["w"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
#                 alpha = 0.2,  color = NA, group=1, fill="green") +
#     geom_line(data = donnees_liste[["i"]], aes(x = Hour, y = Moyenne), color ="red", group=1, size = 1) +
#     geom_ribbon(data = donnees_liste[["i"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
#                 alpha = 0.2, color = NA,group=1, fill="red") +
#     geom_line(data = donnees_liste[["fi"]], aes(x = Hour, y = Moyenne), color ="yellow", group=1, size = 1) +
#     geom_ribbon(data = donnees_liste[["fi"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
#                 alpha = 0.2,  color = NA, group=1, fill="yellow") +
#     geom_line(data = donnees_liste[["t"]], aes(x = Hour, y = Moyenne), color ="purple", group=1, size = 1) +
#     geom_ribbon(data = donnees_liste[["t"]], aes(x = Hour, ymin = Moyenne - EcartType, ymax = Moyenne + EcartType),
#                 alpha = 0.2, color = NA, group=1, fill="purple") +
#     labs(title = sprintf("levers per hour (%s)", jour),
#          x = "Hour",
#          y = "Mean +/- standard deviation ",
#          color = "categorie") +
#     theme_minimal() +
#     theme(panel.grid = element_blank(),
#           panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dashed")) +
#     scale_color_manual(values = c("blue", "green", "red","yellow","purple"),
#                        labels = c("scroungers", "workers", "independents","independent females","stockers"))
#   graphique_liste[[jour]]<- graphique_agregate
# }
# 
# grid.arrange(grobs = graphique_liste, ncol = 1)
# 
# graphique_tot<- c(graphique_liste1,graphique_liste)
# graphique_tot <- grid.arrange(graphique_liste1[[1]], graphique_liste[[1]],
#                               graphique_liste1[[2]], graphique_liste[[2]],
#                               ncol = 1)
