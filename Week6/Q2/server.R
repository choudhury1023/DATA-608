library(shiny)
library(ggplot2)
library(dplyr)


df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv")




function(input, output, session) {
  selectedData <- reactive({
    dfSlice <- df %>% 
      filter(State%in%input$states, ICD.Chapter%in%input$causes)
    
  })
    output$plot2 <- renderPlot({
      NatAvg <- df %>% 
        filter(ICD.Chapter==input$causes) %>% 
        group_by(Year) %>% 
        summarise(WtAvg=(sum(as.numeric(Deaths))/sum(as.numeric(Population))*10^5))
    ggplot(selectedData, aes(x=Year, y=Crude.Rate, color='red')) + 
      geom_line() + 
      geom_line(aes(x=NatAvg$Year, y=Nat.Avg$WtAvg, color='green'),size=2)
    
  })
}

## Keep getting error message: incorrect length (0), expecting: 9961