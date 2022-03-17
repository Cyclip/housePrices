from const import *
import logging, sys

logger = logging.getLogger(__name__ + "wee")
logger.setLevel(LOGGING_LEVEL)

logging.basicConfig(
    format="[%(asctime)s] [%(module)s/%(funcName)s:%(lineno)d] %(levelname)s | %(message)s",
    stream=sys.stdout,
)

import csv
import sys
import seaborn
import matplotlib.pyplot as plt

import process


def main():
    # Get salaries historical data
    logger.info("Loading salaries")
    salaries = process.getSalaries(SALARIES)

    # Get house prices historical data
    logger.info("Loading house prices")
    housePrices = process.getHousePrices(HOUSEPRICES)

    # Cache house prices
    process.cache(housePrices, HOUSE_PRICES_CACHE)

    # Build percentage change datasets
    logger.info("Getting percentage change of salaries")
    salariesPC = process.getPercChange(salaries)
    
    logger.info("Getting percentage change of house prices")
    housePricesPC = process.getPercChange(housePrices)

    # Plot house prices
    logger.info("Plotting house price changes")
    housePricePlot = seaborn.lineplot(
        x=PERC_X_VAL,
        y=PERC_Y_VAL,
        data=housePricesPC,
    )

    # Plot salaries
    logger.info("Plotting salaries changes")
    salariesPlot = seaborn.lineplot(
        x=PERC_X_VAL,
        y=PERC_Y_VAL,
        data=salariesPC,
    )

    plt.legend(labels=["Average house price", "Median annual salary",])

    housePricePlot.axhline(0, color='gray')

    plt.show()


if __name__ == "__main__":
    seaborn.set_style("dark")
    seaborn.set_theme(style="darkgrid")
    main()
    pass