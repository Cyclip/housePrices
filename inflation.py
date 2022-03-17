# Index year: 2010
from email.mime import base
import logging
import pandas as pd
from const import *


logger = logging.getLogger(__name__ + "wee")
logger.setLevel(LOGGING_LEVEL)


def loadInflation():
    """Load inflation dataset"""
    df = pd.read_csv(FILENAME, nrows=222, chunksize=1, skiprows=7)
    years = {}

    for row in df:
        year, index = row.values[0]
        years[year] = index
        logger.debug(f"Loaded inflation index {year}: {index}")
    
    return years


def adjustVal(val, year):
    """Adjust a nominal value for inflation

    Args:
        val (float): Money to adjust
        year (int): Year to adjust from

    Returns:
        float: Real (adjusted) value
    """
    baseYearLevel = inflationData[INDEX_YEAR]
    currentYearLevel = inflationData[year]

    adjusted = val / (currentYearLevel/baseYearLevel)
    
    logger.debug(f"Adjusted {val} ({year}) => {adjusted} ({INDEX_YEAR})")

    return adjusted


inflationData = loadInflation()
logger.info("Loaded inflation data")