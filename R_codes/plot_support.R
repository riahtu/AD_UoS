
library(reshape2)
library(ggplot2)


CO <- c(3.39,0.73,2.57,4.57,0.68,2.23)  
FHMM<- c(3.72,0.55,0.61,4.79,0.58,2.30) 
LBM <- c(1.74,0.40,0.52,2.63,0.93,1.02)
Appliance <- c(1,2,3,4,5,6)
Approach <- rep('Noisy',6)
Result_type <- rep('ANE',6)
Home <- rep(10,6)

df_10_ane_noisy <- data.frame(Home,Appliance,Approach,Result_type,CO,FHMM,LBM)

setwd('/Volumes/MacintoshHD2/Users/haroonr/Dropbox/Writings/UoS/plots/')
plot_ane(df_10_ane_noisy,'df_10_ane_noisy.pdf')

plot_ane <- function(dframe,savename) {
keep <- c('Appliance','CO','FHMM','LBM')
temp <- dframe[keep]
df_melt=  reshape2::melt(temp,id.vars= c('Appliance'))
g <- ggplot(df_melt,aes(Appliance,value)) + geom_bar(aes(fill=variable),position="dodge",stat="identity",width = 0.4 )
g <- g +  labs(x = "Appliance ", y='ANE', fill="")  + scale_fill_brewer(palette="Set1")
g <- g + theme(axis.text = element_text(color="Black",size = 7),legend.text = element_text(size = 7))+ scale_x_continuous(breaks = seq(1, 6, by = 1)) + opts(legend.key=unit(1))
g <- g + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
               panel.background = element_blank(), axis.line = element_line(colour = "grey"))
#g
ggsave(savename, width = 3, height = 1.5, units = "in")
}