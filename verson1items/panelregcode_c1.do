//panelreg.csv , hotdf.csv , coldf.csv , eastdf.csv , westdf.csv, richdf.csv, poordf.csv

import delimited "G:\SME\Paper_1\panelreg_c1.csv", clear
xtset kreise_code year
gen t=year-1999
gen t2=t^2

gen tasxtasd1= tas*tasd1
gen precxprecd1 =prec*precd1
gen precxprecd1l1 = prec*precd1l1
gen tasxtasd1l1 = tas*tasd1l1

// BHM regression equation (1)
reghdfe lngvarealpwd1 tas tas2 prec prec2 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)


// KW regression equation (2)
reghdfe lngvarealpwd1 tasd1 tasd1l1 tasxtasd1 tasxtasd1l1 tas tas2 precd1 precd1l1 precxprecd1 precxprecd1l1 prec prec2 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)

// Combining the KW with lagged precipitation and the extremes estimates equation (3)

reghdfe lngvarealpwd1 tas tas2 tasd1 tasxtasd1 precd1 precd1l1 precxprecd1 precxprecd1l1 prec prec2 hotdayd hotdaydl1 colddayd colddaydl1 precpd precpdl1 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)

// Temperature and temperature shocks, precipitation shocks, base and lags, and extremes and lags, without county trends

reghdfe lngvarealpwd1 tas tas2 tasd1 tasxtasd1 precd1 precd1l1 precxprecd1 precxprecd1l1 prec prec2 hotdayd hotdaydl1 colddayd colddaydl1 precpd precpdl1  , absorb(kreise_code year) vce(cluster kreise_code)



// KW without lagged temperatures but with lagged precipitation 
reghdfe lngvarealpwd1 lncappwd1 tas tas2 tasd1 tasxtasd1 precd1 precd1l1 precxprecd1 precxprecd1l1 prec prec2 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)

// KW without any lagged terms

reghdfe lngvarealpwd1 lncappwd1 tas tas2 tasd1 tasxtasd1 prec prec2 precd1 precxprecd1 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)

// Regression with extremes - hotdays, colddays and precipitation concentration

reghdfe lngvarealpwd1 cappwlnd1 hotdayd hotdaydl1 colddayd colddaydl1 precpd precpdl1 i.kreise_code#c.t i.kreise_code#c.t2 , absorb(kreise_code year) vce(cluster kreise_code)

reghdfe lngvarealpwlnd1 tas tas2 tasd1 tasxtasd1 precd1 precd1l1 precxprecd1 precxprecd1l1 prec prec2 hotdayd hotdaydl1 colddayd colddaydl1 precpd precpdl1  , absorb(kreise_code year) vce(cluster state)
//growth regression 

reghdfe lngvarealpwd1 tasd1 tas2d1 precd1 precpdd1 colddaydd1 hotdaydd1 ,absorb(kreise_code year) vce (cluster kreise_code)
