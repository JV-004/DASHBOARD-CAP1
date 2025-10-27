# ------ ESTATÍSTICAS ------  
plantio <- read.csv("phase1/plantio.csv")

# Mostrar dados  
print("=== DADOS DE PLANTIO ===")  
print(plantio)  

# Cálculos  
media <- mean(plantio$area)  
desvio <- sd(plantio$area)  

print(paste("Média das áreas:", round(media, 2), "m²"))  
print(paste("Desvio padrão:", round(desvio, 2), "m²"))  

# ------ CLIMA ------  
library(httr)  

# Configurar API  
url <- "https://api.open-meteo.com/v1/forecast"  
parametros <- list(  
  latitude = -23.55,  
  longitude = -46.64,  
  hourly = "temperature_2m"  
)  

# Requisição  
resposta <- GET(url, query = parametros)  

if (status_code(resposta) == 200) {  
  dados_clima <- content(resposta)  
  temperatura <- dados_clima$hourly$temperature_2m[1]  
  print(paste("Temperatura atual em São Paulo:", temperatura, "°C"))  
} else {  
  print("Erro ao acessar a API do clima!")  
}