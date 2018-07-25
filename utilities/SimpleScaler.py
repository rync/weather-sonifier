def simple_scaler(initMin, initMax, destMin, destMax, value):
    # Very simple, stupid scaling function.
    # It's worth replacing this at some point to account for more nuanced scaling.
    if (initMin != initMax) and (destMin != destMax):
        initRange = initMax - initMin
        destRange = destMax - destMin
        return ((value - initMin) * destRange) / initRange + destMin
    else:
        print('Scaling failed:\nInitial Range: Min ({}) to Max({})\nDestination Range: Min ({}) to Max ({})'.format(initMin, initMax, destMin, destMax))
        return None