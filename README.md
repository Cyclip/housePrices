# house prices
 Graph perc. change in house price vs perc. change in median annual salary (adjusted for inflation)

Inflation index year 2010 = 100

## Process
- Load inflation data
  - Used to adjust nominal values
  - `val / (currentYearLevel/baseYearLevel)`
- Load salaries dataset
  - Adjust each salary for inflation
- Load house prices dataset
  - Calculate the average across a year
  - Adjust average for inflation
- Find annual percentage change for:
  - Salary dataframe
  - House prices dataframe
- Plot both :D

## Sources
- [World bank](https://databank.worldbank.org/reports.aspx?source=2&type=metadata&series=FP.CPI.TOTL.ZG#) (inflation)
- [Statista](https://www.statista.com/statistics/1002964/average-full-time-annual-earnings-in-the-uk/) (average annual earnings)
- [UK Govt](https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-december-2021) (house prices)