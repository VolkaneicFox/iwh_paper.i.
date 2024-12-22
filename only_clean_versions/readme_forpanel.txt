# README: Description of DataFrame Columns

## General Information

This dataset contains panel data with economic and climate variables for different regions in Germany. The columns are organized into economic indicators, log-transformed values, first differences, and climate variables. Below is a detailed description of each column:

## Column Descriptions

### Identifiers and Time Variables

- **year**: The year of observation.
- **DE_code**: Federal state (Bundesland) code for the region.
- **Kreise_Code**: Unique identifier for administrative districts (Kreise).

### Economic Indicators

- **capital_cons**: Total capital consumption or depreciation in the region.
- **total_employment**: Total number of employed persons in the region.
- **real_labour_prod_pw**: Real labor productivity per worker (adjusted for inflation).
- **real_gdppc**: Real Gross Domestic Product per capita (adjusted for inflation).

### Log-Transformed Variables

- **ln.capital_cons**: Natural logarithm of capital consumption.
- **ln.total_employment**: Natural logarithm of total employment.
- **ln.real_labour_prod_pw**: Natural logarithm of real labor productivity.
- **ln.real_gdppc**: Natural logarithm of real GDP per capita.

### First Differences of Log Variables

- **ln.capital_cons.d1**: First difference of the log of capital consumption.
- **ln.total_employment.d1**: First difference of the log of total employment.
- **ln.real_labour_prod_pw.d1**: First difference of the log of labor productivity.
- **ln.real_gdppc.d1**: First difference of the log of real GDP per capita.

### Annual Climate Variables

- **tas**: Mean annual surface air temperature (°C).
- **tas2**: Mean annual surface air temperature squared.
- **prec**: Total annual precipitation (mm).
- **prec2**: Total annual precipitation squared.

### Seasonal Temperature Extremes (F1 and F2)

#### Cold Days

- **autumn_colddays_f1**: Number of cold days in autumn (F1).
- **spring_colddays_f1**: Number of cold days in spring (F1).
- **summer_colddays_f1**: Number of cold days in summer (F1).
- **winter_colddays_f1**: Number of cold days in winter (F1).

#### Hot Days

- **autumn_hotdays_f1**: Number of hot days in autumn (F1).
- **spring_hotdays_f1**: Number of hot days in spring (F1).
- **summer_hotdays_f1**: Number of hot days in summer (F1).
- **winter_hotdays_f1**: Number of hot days in winter (F1).

#### Seasonal Means (Temperature)

- **autumn_seasonal_mean_tas_f1**: Mean temperature in autumn (F1).
- **spring_seasonal_mean_tas_f1**: Mean temperature in spring (F1).
- **summer_seasonal_mean_tas_f1**: Mean temperature in summer (F1).
- **winter_seasonal_mean_tas_f1**: Mean temperature in winter (F1).

### Annual Temperature Extremes

- **hotdays_f1**: Total number of hot days in a year (F1).
- **colddays_f1**: Total number of cold days in a year (F1).

### Precipitation Variables (Seasonal)

#### F1 Precipitation

- **autumn_season_prec_f1**: Total precipitation in autumn (F1).
- **spring_season_prec_f1**: Total precipitation in spring (F1).
- **summer_season_prec_f1**: Total precipitation in summer (F1).
- **winter_season_prec_f1**: Total precipitation in winter (F1).
- **prec_f1**: Total annual precipitation (F1).

### Extreme Wet Weeks

- **winter95_wetweeks**: 95th percentile wet weeks in winter.
- **winter99_wetweeks**: 99th percentile wet weeks in winter.
- **spring95_wetweeks**: 95th percentile wet weeks in spring.
- **spring99_wetweeks**: 99th percentile wet weeks in spring.
- **summer95_wetweeks**: 95th percentile wet weeks in summer.
- **summer99_wetweeks**: 99th percentile wet weeks in summer.
- **autumn95_wetweeks**: 95th percentile wet weeks in autumn.
- **autumn99_wetweeks**: 99th percentile wet weeks in autumn.

### Extreme Dry Weeks

- **winter05_dryweeks**: 5th percentile dry weeks in winter.
- **winter01_dryweeks**: 1st percentile dry weeks in winter.
- **spring05_dryweeks**: 5th percentile dry weeks in spring.
- **spring01_dryweeks**: 1st percentile dry weeks in spring.
- **summer05_dryweeks**: 5th percentile dry weeks in summer.
- **summer01_dryweeks**: 1st percentile dry weeks in summer.
- **autumn05_dryweeks**: 5th percentile dry weeks in autumn.
- **autumn01_dryweeks**: 1st percentile dry weeks in autumn.

### Annual Aggregates for Extremes

- **full95_wetweeks**: Total 95th percentile wet weeks across the year.
- **full99_wetweeks**: Total 99th percentile wet weeks across the year.
- **full05_dryweeks**: Total 5th percentile dry weeks across the year.
- **full01_dryweeks**: Total 1st percentile dry weeks across the year.

## NOTES
                                                          
- **F1** indicates all measures (where relevant) calculated against the fixed history period of 1950-1980.
- **F2** indicates all measures (where relevant) calculated against the rolling history method.                                                        
- Temperature variables are measured in degrees Celsius (°C).
- Precipitation variables are measured in millimeters (mm).
- Economic data are inflation-adjusted (real values).
- Log transformations and first differences are computed for economic variables to analyze growth rates and trends.
