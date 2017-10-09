
df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv", header = TRUE, stringsAsFactors = FALSE)

fluidPage(
  headerPanel('Housing Price Explorer'),
  sidebarPanel(
    selectInput('cuses', 'ICD.Chapter', unique(df$ICD.Chapter), selected='Neoplasms'),
    selectInput('state', 'State', unique(df$State), selected='NY')
   ),
  mainPanel(
    plotOutput('plot2')
   )
)