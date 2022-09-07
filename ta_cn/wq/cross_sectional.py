"""
Cross Sectional Operators
"""
import numpy as np

from .. import bn_wraps as bn
from ..utils import pd_to_np


def normalize(x, useStd=False, limit=0.0):
    """Calculates the mean value of all valid alpha values for a certain date, then subtracts that mean from each element."""
    if x.ndim == 2:
        t1 = np.nanmean(x, axis=1, keepdims=True)
    else:
        t1 = np.nanmean(x)

    if useStd:
        if x.ndim == 2:
            t2 = np.nanstd(x, axis=1, keepdims=True, ddof=1)
        else:
            # 这里用ddof=1才能与文档数值对应上
            t2 = np.nanstd(x, ddof=1)

        r = (x - t1) / t2
    else:
        r = (x - t1)

    if limit != 0:
        return np.clip(r, -limit, limit)
    else:
        return r


def one_side(x, side='long'):
    """Shifts all instruments up or down so that the Alpha becomes long-only or short-only
(if side = short), respectively."""
    # TODO: 这里不确定，需再研究
    # [-1, 0, 1]+1=[0, 1, 2]
    # max([-1, 0, 1], 0)=[0,0,1]
    if side == 'long':
        return np.maximum(x, 0)
    else:
        return np.minimum(x, 0)


def quantile(x, driver='gaussian', sigma=1.0):
    """Rank the raw vector, shift the ranked Alpha vector, apply distribution ( gaussian, cauchy, uniform ). If driver is uniform, it simply subtract each Alpha value with the mean of all Alpha values in the Alpha vector."""
    pass


def rank(x, rate=2):
    """Ranks the input among all the instruments and returns an equally distributed number between 0.0 and 1.0. For precise sort, use the rate as 0."""
    pct = True

    if x.ndim == 2:
        t1 = bn.nanrankdata(x, axis=1)
    else:
        t1 = bn.nanrankdata(x)

    if pct:
        if x.ndim == 2:
            t2 = np.nansum(~np.isnan(x), axis=1, keepdims=True)
        else:
            t2 = np.nansum(~np.isnan(x))

        return t1 / t2
    else:
        return t1


def rank_by_side(x, rate=2, scale=1):
    """Ranks positive and negative input separately and scale to book. For precise sorting use rate=0."""
    pass


def generalized_rank(open, m=1):
    """The idea is that difference between instrument values raised to the power of m is added to the rank of instrument with bigger value and subtracted from the rank of instrument with lesser value. More details in the notes at the end of page."""
    pass


def regression_neut(y, x):
    """Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable."""
    pass


def regression_proj(y, x):
    """Conducts the cross-sectional regression on the stocks with Y as target and X as the independent variable."""
    pass


def scale(x, scale=1, longscale=1, shortscale=1):
    """Scales input to booksize. We can also scale the long positions and short positions to separate scales by mentioning additional parameters to the operator."""
    if x.ndim == 2:
        b = np.nansum(abs(x), axis=1, keepdims=True)
    else:
        b = np.nansum(abs(x), keepdims=True)

    return x / b * scale


def scale_down(x, constant=0):
    """Scales all values in each day proportionately between 0 and 1 such that minimum value maps to 0 and maximum value maps to 1. Constant is the offset by which final result is subtracted."""
    if x.ndim == 2:
        m1, m2 = np.min(x, axis=1, keepdims=True), np.max(x, axis=1, keepdims=True)
    else:
        m1, m2 = np.min(x), np.max(x)

    return (x - m1) / (m2 - m1) - constant


def truncate(x, maxPercent=0.01):
    """Operator truncates all values of x to maxPercent. Here, maxPercent is in decimal notation."""
    if x.ndim == 2:
        t1 = np.nansum(x, axis=1, keepdims=True) * maxPercent
    else:
        t1 = np.nansum(x) * maxPercent

    return np.minimum(x, t1)


def vector_neut(x, y):
    """For given vectors x and y, it finds a new vector x* (output) such that x* is orthogonal to y."""
    pass


def vector_proj(x, y):
    """Returns vector projection of x onto y. Algebraic and geometric details can be found on wiki"""
    pass


def winsorize(x, std=4):
    """Winsorizes x to make sure that all values in x are between the lower and upper limits, which are specified as multiple of std. Details can be found on wiki"""
    x = pd_to_np(x, copy=False)
    if x.ndim == 2:
        _mean = bn.nanmean(x, axis=1)[:, None]
        _std = bn.nanstd(x, axis=1, ddof=0)[:, None] * std
    else:
        _mean = bn.nanmean(x)
        _std = bn.nanstd(x, ddof=0) * std

    return np.clip(x, _mean - _std, _mean + _std)


def zscore(x):
    """Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean"""
    x = pd_to_np(x, copy=False)
    if x.ndim == 2:
        _mean = bn.nanmean(x, axis=1)[:, None]
        _std = bn.nanstd(x, axis=1, ddof=0)[:, None]
    else:
        _mean = bn.nanmean(x)
        _std = bn.nanstd(x, ddof=0)

    return (x - _mean) / _std


def rank_gmean_amean_diff(input1, input2, input3, ):
    """Operator returns difference of geometric mean and arithmetic mean of cross sectional rank of inputs."""
    pass
