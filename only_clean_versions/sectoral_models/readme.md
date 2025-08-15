The sectoral GVA and Employment Statistics are presented in tables gvapw_{A or BE or F or GI}.csv . 
These can be used to compare the ardeco tables, I downloaded the data used here on 15 August 2025.

The panel data regressions are done using the file all_sectors_ardeco.csv .

The panel regression output is shown in pyresults_tab.xlsx under different tabs for GDP-percapita and for sectoral regressions.

The Burke results matched, as we had earlier discussed, however, I do not like using tas and tas^2 because the linear correlation
between these two regressors (as with prec and prec^2) are nearly 1. This is not correct, I have checked within county correlation 
and ofcourse cross-sectional correlations, and it is not advisable to use this. The reason for this high correlation is that we
have a very small range of temperatures so the tas and tas^2 pretty much move together. The second-degree effects are instead expressed 
tas X D_tas (temperature X delta temperature) as the correlation between these terms are much more manageable at around 0.6.

