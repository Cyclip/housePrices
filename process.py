from numpy import cumprod
import pandas as pd
import logging
import pickle
import os
import datetime

import inflation
from const import *


logger = logging.getLogger(__name__ + "wee")
logger.setLevel(LOGGING_LEVEL)


def getAvg(l):
    return sum(l) / len(l)


def getHousePrices(filename, limiting=False):
    """Retrieve house prices from file

    Args:
        filename (string): CSV path
        limiting (bool/int, optional): Limit rows. Defaults to False.

    Returns:
        Dataframe: Dataframe containing historical price data
    """
    logger.info(f"Loading house prices from {filename}")

    # check if cached
    if os.path.isfile(HOUSE_PRICES_CACHE):
        logger.warning("Using cached result")
        return pickle.load(open(HOUSE_PRICES_CACHE, "rb"))
    
    if limiting == False:
        df = pd.read_csv(filename, chunksize=1)
    else:
        logger.warn(f"Limiting to {limiting} rows")
        df = pd.read_csv(filename, nrows=limiting, chunksize=1)

    currentYear = None
    prices = []
    data = {
        X_VAL: [],
        Y_VAL: [],
    }

    for chunk in df:
        date = datetime.datetime.strptime(
            chunk['Date'].values[0],
            "%Y-%m-%d"
        )

        price = float(chunk['Average_Price'].values[0])
        logger.debug(f"Read chunk {date.year}: £{price}")

        if currentYear != date.year:
            if currentYear == None:
                currentYear = date.year
            else:
                avg = inflation.adjustVal(getAvg(prices), currentYear)
                
                data[X_VAL].append(currentYear)
                data[Y_VAL].append(avg)

                prices = []
                currentYear = date.year

                logger.info(f"Compiled {currentYear} data, real average {avg}")
        
        prices.append(price)

    return pd.DataFrame.from_dict(
        data,
    )


def getSalaries(filename):
    """Process the salaries csv file

    Args:
        filename (string): Path of .csv salaries file
    """
    df = pd.read_csv(filename, chunksize=1)

    data = {
        X_VAL: [],
        Y_VAL: [],
    }

    for chunk in df:
        year = int(chunk['Year'].values[0])
        salary = inflation.adjustVal(int(chunk['Amount'].values[0]), year)
        logger.debug(f"Reading salary {year}: £{salary}")

        data[X_VAL].append(year)
        data[Y_VAL].append(salary)
    
    return pd.DataFrame.from_dict(data)


def cache(obj, fn):
    logger.info(f"Caching to {fn}")
    pickle.dump(obj, open(fn, 'wb'))


def getPercChange(df):
    logger.info("Getting percentage change of dataframe")

    data = {
        PERC_X_VAL: [],
        PERC_Y_VAL: [],
    }

    df.reset_index()
    previousYearVal = None

    for index, row in df.iterrows():
        currentYearVal = row[Y_VAL]

        if previousYearVal is None:
            # data[PERC_X_VAL].append(row[X_VAL])
            # data[PERC_Y_VAL].append(0)

            previousYearVal = currentYearVal
            continue

        # get perc change
        percChange = ((currentYearVal - previousYearVal) / previousYearVal) * 100
        data[PERC_X_VAL].append(row[X_VAL])
        data[PERC_Y_VAL].append(percChange)

        previousYearVal = currentYearVal
        logger.debug(f"Recent addition: {round(percChange, 2)}% ({row[X_VAL]})")
    
    return pd.DataFrame.from_dict(data)