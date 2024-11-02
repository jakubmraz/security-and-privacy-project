library(readxl)
library(sdcMicro)

# Read the Excel file
data <- read_excel("D:\\Documents\\Documents\\Uni\\Security_Privacy\\final_project\\security-and-privacy-project\\even_more_private_dataD.xlsx")

# Specify key and PRAM variables
keyVars <- c("dob", "education", "citizenship", "zip", "marital_status", "sex")
pramVars <- c("party")

# Create the SDC object
sdc_obj <- createSdcObj(
  dat = data,
  keyVars = keyVars,
  pramVars = pramVars,
  numVars = NULL,
  ghostVars = NULL,
  weightVar = NULL,
  hhId = NULL,
  strataVar = NULL,
  sensibleVar = NULL
)

# Calculate risk metrics
risk <- dRisk(sdc_obj)
print(risk)
