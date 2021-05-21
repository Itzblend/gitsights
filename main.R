library(tidyverse)
library(treemap)

data <- read.csv('csv/commits.csv')

edit_counts <- data.frame(table(data$filename))
colnames(edit_counts) <- c('filename', 'count')

edit_counts
treemap(edit_counts,
        index="filename",
        vSize="count",
        type="index"
)
