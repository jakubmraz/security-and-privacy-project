library(readxl)
library(sdcMicro)

# Read the Excel file
data <- read_excel("D:\\Documents\\Documents\\Uni\\Security_Privacy\\final_project\\phase1\\private_dataD.xlsx")

# Specify key variables and sensitive variables
keyVars <- c("sex",	"evote",	"dob",	"zip",	"education",	"citizenship",	"marital_status")
pramVars <- c("party")


# Apply sdcMicro to your data
sdc_obj <- createSdcObj(dat = data, keyVars = keyVars, pramVars = pramVars)

# Calculate risk metrics
risk <- dRisk(sdc_obj)
print(risk)
