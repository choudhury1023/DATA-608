
df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")


# Subset 2010 data
dfq1 <- df %>%
  filter(Year == 2010) %>%
  select(State, Crude.Rate, ICD.Chapter) %>%
  arrange(Crude.Rate)


fluidPage(
  headerPanel('Cause of Mortality'),
  sidebarPanel(
    selectInput('ICD.Chapter', 'Cause', unique(dfq1$ICD.Chapter), selected='Neoplasms')
  ),
  mainPanel(
    plotOutput('plot1')
  )
)

