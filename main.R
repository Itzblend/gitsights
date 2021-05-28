library(tidyverse)
library(treemap)

data <- read.csv('csv/commits.csv')

edit_counts <- data.frame(table(data$filename))
colnames(edit_counts) <- c('filename', 'count')

edit_counts[with(edit_counts, order(-count)),] %>% 
  top_n(n=20) %>% 
  treemap(index="filename",
          vSize="count",
          type="index"
  )
  
  
treemap(edit_counts,
        index="filename",
        vSize="count",
        type="index"
)
