library(shiny)
library(dplyr)
library(ggplot2)

df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")

dfq1 <- subset(df, Year == 2010)




shinyServer(function(input, output) {
  SelectedData <- reactive({
    dfSlice <- dfq1 %>%
      filter(ICD.Chapter==input$cause) %>%
      arrange(desc(Crude.Rate))
    })
  output$plot1 <- renderPlot({
    dfSlice <- dfq1 %>%
      filter(ICD.Chapter == input$cause)
    ggplot(SelectedData, aes(x=Year, y= State, color='red')) + 
      geom_bar()
  })
})
  

## Keep getting error message:incorrect length (0), expecting: 835
  