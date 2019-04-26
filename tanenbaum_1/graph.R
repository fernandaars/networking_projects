library(ggplot2)

values <- read.csv(file="/home/fernandaars/networking_projects/tanenbaum_1/redes.csv")

labels <- values[1]
labels = as.matrix(labels)
time <- values[3]
time = as.matrix(time)
distance <- values[4]
distance <- as.matrix(distance)
print(values)

graph <- ggplot(values, aes(x = distance, y = time), group=1) +
  geom_bar(stat="identity")+
  scale_x_discrete(limits=c("7.457,87","9.343,77","9.875,30", "12.507,79", "13.838,79")) +
  geom_text(aes(label=labels), position=position_dodge(width=0.9), vjust=-0.25)

print(graph + labs(title= "One-Way Transit Time Over The Internet",
                   y="Time of Response Measured by Ping (s)", x = "Distance (Km)"))

