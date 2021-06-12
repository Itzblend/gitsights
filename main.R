library(tidyverse)
library(treemap)

data <- read.csv('csv/commits.csv')


edit_counts <- data.frame(table(data$filename, data$repository))
colnames(edit_counts) <- c('filename', 'repository', 'count')

edit_counts[with(edit_counts, order(-count)),] %>% 
  top_n(n=20) %>% 
  treemap(index="filename",
          vSize="count",
          type="index"
  )
  
edit_counts %>%
  filter(repository == 'dotties' & count != 0) %>% 
  top_n(n=20)
  treemap(index="filename",
          vSize="count",
          type="index"
)

sum(data[data$filename == 'app/index.html' & data$repository == 'dotties',"additions"]) - sum(data[data$filename == 'app/index.html' & data$repository == 'dotties',"deletions"])


temp = data[data$filename == 'app/index.html',]
temp$truechange <- temp$additions - temp$deletions
temp <- distinct(temp, .keep_all = TRUE)
sum(temp$truechange)



# By each commit, get lines of code
data %>% 
  filter(filename == 'docker-compose.yml' & repository == 'dotties' & commiter != 'GitHub') %>% 
  distinct(sha, .keep_all = TRUE) %>% 
  arrange(commit_date) %>% 
  select(additions, deletions, changes) %>% 
  cumsum() %>% 
  mutate(filesize = additions - deletions)

