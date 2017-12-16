#defining Table 2.1
table21 <- data.frame(child = 1:7, 
                y0 = c(10, 15, 20, 20,10,15,15), 
                y1 = c(15, 15, 30,15,20,15,30 ))

table21$treatment <- table21$y0 - table21$y1