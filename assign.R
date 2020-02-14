# import dplyr
# import readxl library to read excel files
# df data frame is created to read files

library(readxl)
library(dplyr)

#To read SaleData
df <- read_excel('SaleData.xlsx')


df<- read.csv(text = gsub("\\\\,", "-", readLines("imdb.csv")))

#To read diamond data set
df<- read.csv('diamonds.csv')


# Q1 Find least sales amount for each item

Q1 <- function(df){
  d1 <- filter(group_by(df,Item),Sale_amt == min(Sale_amt))
  return(d1)
  
}

# Q2 compute total sales at each year X region

Q2 <- function(df){
  d1 <- df %>% group_by(Year=format(OrderDate,"%Y"),Region) %>% summarise(Total_sales = sum(Sale_amt))
  return(d1)
  
}

# Q3 append column with no of days difference from present date to each order date

Q3 <- function(df){
  c <- Sys.Date()
  df$days_diff <- as.Date(as.character(c), format = "%Y-%m-%d") - as.Date(as.character(df$OrderDate), format = "%Y-%m-%d")
  return(df)
  
}

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.

Q4 <- function(df){
  df <- df %>% group_by(Manager) %>% summarise(salesman = toString(unique(SalesMan)))
  return(df)
  
}

# Q5 For all regions find number of salesman and number of units

Q5 <- function(df){
  d2 <- df %>% group_by(Region) %>% summarise(total_sales = sum(Sale_amt),salesman_count = n()) 
  return(d2)
  
}

# Q6 Find total sales as percentage for each manager

Q6 <- function(df){
  d2 <- df %>% group_by(Manager) %>% summarise(total_sales = sum(Sale_amt)) 
  tot_sales <- sum(df$Sale_amt)
  d2$sales_percentage <- (d2$total_sales/tot_sales)*100
  return(d2)
}

df <- read.csv(text = gsub("\\\\,", "-", readLines("imdb.csv")))

# Q7 get imdb rating for fifth movie of dataframe

Q7 <- function(df){
  
  return(df[5,'imdbRating'])
}


# Q8 return titles of movies with shortest and longest run time

Q8 <- function(df){
  
  d1 <- df %>% filter(!is.na(duration)) %>% filter(type == 'video.movie') %>% arrange(duration)
  m1 <- tail(d1,1)[1,'title']
  m2 <- head(d1,1)[1,'title']
  return(paste("longest duration movie",m1,"shortest duration movie",m2))
}

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)

Q9 <- function(df){
  d1 <- arrange(df,year,desc(imdbRating))
  return(d1)
}

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes

Q10 <- function(df){
  df$duration <- as.numeric(df$duration)
  d1 <- subset(df, duration >= 60 & duration <= 180)
  return(d1)
}

# Q11 count the duplicate rows of diamonds DataFrame.

Q11 <- function(df){
  c <- count(df[duplicated(df),])
  return(c)
}

df<- read.csv('diamonds.csv')


# Q12 droping those rows where any value in a row is missing in carat and cut columns

Q12 <- function(df){
  df <- na.omit(df,cols=c("carot","cut"))
  return(df)
}

# Q13 subset only numeric columns

Q12 <- function(df){
  df <- select_if(df,is.numeric)
  return(df)
}

# Q14 compute volume as (x*y*z) when depth > 60 else 8

Q14 <- function(df){
  
  for (i in 1:nrow(df)) {
    if(df$depth[i] > 60)
    {
      df$volume[i] <- df$x[i] * df$y[i] * (as.numeric(df$z[i]))
    }
    else
    {
      df$volume[i] <- 8
    }
    
  }
  return(df)
}

# Q15 impute missing price values with mean

Q15 <- function(df){
  df$price[which(is.na(df$price))] <- mean(df$price,na.rm = TRUE)
  return(df)
}


