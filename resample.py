#python3
"""
"""

#imports

#+ standard libraries

import os

from typing import Union, Tuple, Optional, Sequence, Any

import collections.abc as c_abc

from bisect import bisect_left

#data types

TReal = Union[int, float]
TRealNone = Union[int, float, None]
TRealPair = Tuple[TReal, TReal]
TCoord = Sequence[TReal]
TData = Sequence[TCoord]

#functions

#+ private helper functions

def _CheckDataPoints(Data: Any) -> None:
    """
    Checks that the passed argument is a sequence of nested sequences of 2 real
    number elements each, with, at least, two such sub-sequences; raises an
    exception otherwise.
    
    Signature:
        type A -> None
    
    Raises:
        Exception: passed argument is not a sequence of nested sequences of 2
            real number elements each
    
    Version 1.0.0.0
    """
    if not isinstance(Data, c_abc.Sequence):
        raise Exception #TODO - beter handling required
    elif len(Data) < 2:
        raise Exception #TODO - beter handling required
    for Index, Item in enumerate(Data):
        if not isinstance(Item, c_abc.Sequence):
            raise Exception #TODO - beter handling required
        elif len(Item) != 2:
            raise Exception #TODO - beter handling required
        x, y = Item
        if not isinstance(x, (int, float)):
            raise Exception #TODO - beter handling required
        elif not isinstance(y, (int, float)):
            raise Exception #TODO - beter handling required

def _CheckStartStop(Start: Any, Stop: Any) -> None:
    """
    Checks that the both passed arguments are real numbers and the second is
    larger than the first; otherwise an exception is raised.
    
    Signature:
        type A, type B -> None
    
    Raises:
        Exception: any or the arguments is not a real number, OR the second
            argument is less than or equal to the firsts
    
    Version 1.0.0.0
    """
    if not isinstance(Start, (int, float)):
        raise Exception #TODO - beter handling required
    elif not isinstance(Stop, (int, float)):
        raise Exception #TODO - beter handling required
    elif Stop <= Start:
        raise Exception #TODO - beter handling required

def _CheckStep(Step: Any) -> None:
    """
    Checks that the passed value is a positive real number; raises an exception
    otherwise.
    
    Signature:
        type A -> None
    
    Raises:
        Exception: passed argument is not a real number, OR not positive
    
    Version 1.0.0.0
    """
    if not isinstance(Step, (int, float)):
        raise Exception #TODO - beter handling required
    elif Step <= 0:
        raise Exception #TODO - beter handling required

#+ public helper functions

def GetBoundaries(Previous: TRealNone, Current: TReal,
                                                Next: TRealNone) -> TRealPair:
    """
    Calculates the lower and upper boundaries of an unterval around the current
    data point (x2) based on the values of the previous (x1) and the next (x3)
    data points using the following convention:
        * x1 = None, x2 < x3 - as x2 +- (x3 - x2)/2
        * x3 = None, x1 < x2 - as x2 +- (x2 - x1)/2
        * x1 < x2 < x3 - as (x2 + x1) / 2 and (x2 + x3) /2
    
    Other cases result in an exception.
    
    Signature:
        int OR float OR None, int OR float, int OR float OR None
            -> tuple(int OR float, int OR float)
    
    Args:
        Previous: int OR float OR None; the previous data point
        Current: int OR float; the current data point
        Next: int OR float OR None; the next data point, both Previous and Next
            cannot be None simultaneously
    
    Returns:
        tuple(int OR float, int OR float): two real numbers tuple as the lower
            and upper boundaries of the interval
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    if not isinstance(Current, (int, float)):
        raise Exception #TODO - beter handling required
    if not ((Previous is None) or isinstance(Previous, (int, float))):
        raise Exception #TODO - beter handling required
    if not ((Next is None) or isinstance(Next, (int, float))):
        raise Exception #TODO - beter handling required
    if (Previous is None) and (Next is None):
        raise Exception #TODO - beter handling required
    if Previous is None:
        if Next <= Current:
            raise Exception #TODO - beter handling required
        DeltaP = 0.5 * (Next - Current)
        DeltaN = - DeltaP
    elif Next is None:
        if Current <= Previous:
            raise Exception #TODO - beter handling required
        DeltaP = 0.5 * (Current - Previous)
        DeltaN = - DeltaP
    else:
        if Next <= Current:
            raise Exception #TODO - beter handling required
        elif Current <= Previous:
            raise Exception #TODO - beter handling required
        DeltaP = 0.5 * (Next - Current)
        DeltaN = 0.5 * (Previous - Current)
    Result = (Current + DeltaN, Current + DeltaP)
    return Result

def GenerateXPoints(Start: TReal, *, Stop: TRealNone = None,
                            Step: TRealNone = None,
                            NPoints: Optional[int] = None) -> Tuple[TReal, ...]:
    """
    Generates a tuple of real numbers forming an equidistance intervals. The
    following calling signatures are supported:
        * starting point, (maximal) ending point and step length - the last
            returned point may be less than the passed ending point, but not
            more than 1 interval apart; however, at least, 2 points are
        * starting point, ending point and number of points
        * starting point, interval length and number of points
    
    Other cases result in an exception.
    
    Signature:
        int OR float, *, int OR float, int OR float -> tuple(int OR float)
    
    Args:
        Start: int OR float; the starting point
        Stop: (keyword) int OR float OR None; the ending point, defaults to None
        Step: (keyword) int > 0 OR float > 0 OR None; the interval length,
            defaults to None
        NPoints: (keyword) int > 1 OR None; the number of points, defaults to
            None
    
    Returns:
        tuple(int OR float): a sequence of the data points forming an
            equidistance intervals
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    if not isinstance(Start, (int, float)):
        raise Exception #TODO - beter handling required
    if not (Stop is None):
        if not isinstance(Stop, (int, float)):
            raise Exception #TODO - beter handling required
        elif Stop <= Start:
            raise Exception #TODO - beter handling required
        if (Step is None) and (NPoints is None):
            raise Exception #TODO - beter handling required
        elif ((not (Step is None)) and (not (NPoints is None))):
            raise Exception #TODO - beter handling required
        elif Step is None: #NPoints is not None
            if not isinstance(NPoints, int):
                raise Exception #TODO - beter handling required
            elif NPoints <= 1:
                raise Exception #TODO - beter handling required
            _Step = (Stop - Start) / (NPoints - 1)
            Result = tuple(Start + Index * _Step for Index in range(NPoints))
        else: #NPoints is None but Step is not None
            _CheckStep(Step)
            _NSteps = int((Stop - Start) / Step) + 1
            if _NSteps == 1:
                _NSteps = 2
            Result = tuple(Start + Index * Step for Index in range(_NSteps))
    elif not (Step is None): #Stop is None but Step is not None
        _CheckStep(Step)
        if NPoints is None: #only Step is not None
            raise Exception #TODO - beter handling required
        elif NPoints <= 1:
            raise Exception #TODO - beter handling require
        Result = tuple(Start + Index * Step for Index in range(NPoints))
    else: #Stop is None and Step is None
        raise Exception #TODO - beter handling required
    return Result

#+ main work functions

def ResampleIntegral(Data: TData, Start: TReal, Stop: TReal,
                                                        Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the instanteneous,
    point-values of a function at the given points. The actual function is
    approximated by step-wise one, and the definite integrals of it are
    calculated within the bounds of each of the target bins, which are then
    normalized to the width / length of a bin. Thus, the returned, re-sampled
    values are estimators of the actual, point-values of this function at the
    different x-points.
    
    The source bins boundaries are calculated as mid-points between 3
    consecutive positions, except for the left and right edges, where the
    boundaries are symmetric and calculated from 2 adjacent points.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorted in ascending order of X values
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    TargetBinIndex = 0
    TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
    TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    SourceIndex = 0
    Prev = None
    Curr = Data[SourceIndex][0]
    Next = Data[SourceIndex + 1][0]
    SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    DataLen = len(Data)
    TargetLen = len(TargetBins)
    Values = list()
    #skipping source points to the left of the target range
    while SourceBinRight <= TargetBinLeft and SourceIndex < DataLen:
        SourceIndex += 1
        if SourceIndex < DataLen:
            Prev = Data[SourceIndex - 1][0]
            Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    #filling left part of the target range with zeroes if not in source range
    while TargetBinRight <= SourceBinLeft and TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
        if TargetBinIndex < TargetLen:
            TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
            TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    #actual re-sampling
    TargetValue = 0
    while TargetBinIndex < TargetLen and SourceIndex < DataLen:
        SourceValue = Data[SourceIndex][1]
        if SourceIndex > 0:
            Prev = Data[SourceIndex - 1][0]
        else:
            Prev = None
        Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
        if SourceBinLeft >= TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = SourceBinRight - SourceBinLeft
            TargetValue += Delta * SourceValue
            SourceIndex += 1
        elif SourceBinLeft < TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = SourceBinRight - TargetBinLeft
            TargetValue += Delta * SourceValue
            SourceIndex += 1
        elif SourceBinLeft >= TargetBinLeft and SourceBinRight > TargetBinRight:
            Delta = TargetBinRight - SourceBinLeft
            TargetValue += Delta * SourceValue
            Values.append(TargetValue / Step)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
        else:
            Values.append(SourceValue)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    if SourceIndex == DataLen and TargetValue != 0 and TargetBinIndex<TargetLen:
        Values.append(TargetValue / Step)
        TargetBinIndex += 1
        TargetValue = 0
    #filling right part of the target range with zeroes if not in source range
    while TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
    #forming the re-sampled data
    Result = tuple((Position, Values[Index])
                                for Index, Position in enumerate(TargetBins))
    return Result

def ResampleIntegralLeft(Data: TData, Start: TReal, Stop: TReal,
                                                        Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the instanteneous,
    point-values of a function at the given points. The actual function is
    approximated by step-wise one, and the definite integrals of it are
    calculated within the bounds of each of the target bins, which are then
    normalized to the width / length of a bin. Thus, the returned, re-sampled
    values are estimators of the actual, point-values of this function at the
    different x-points.
    
    The source bins boundaries are calculated calculated from 2 adjacent points:
    the current and the previous, except for the left-most bin, when the current
    and next points are used instead. In any case, the boundaries are symmetric
    with respect to the 'center' values of the source bins.
    
    This method is implemented for the backward compatibility with some legacy
    calculations.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorted in ascending order of X values
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    TargetBinIndex = 0
    TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
    TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    SourceIndex = 0
    Prev = None
    Curr = Data[SourceIndex][0]
    Next = Data[SourceIndex + 1][0]
    SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    DataLen = len(Data)
    TargetLen = len(TargetBins)
    Values = list()
    #skipping source points to the left of the target range
    while SourceBinRight <= TargetBinLeft and SourceIndex < DataLen:
        SourceIndex += 1
        if SourceIndex < DataLen:
            Prev = Data[SourceIndex - 1][0]
            Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    #filling left part of the target range with zeroes if not in source range
    while TargetBinRight <= SourceBinLeft and TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
        if TargetBinIndex < TargetLen:
            TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
            TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    #actual re-sampling
    TargetValue = 0
    while TargetBinIndex < TargetLen and SourceIndex < DataLen:
        SourceValue = Data[SourceIndex][1]
        if SourceIndex > 0:
            Prev = Data[SourceIndex - 1][0]
        else:
            Prev = None
        Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
        if Prev is None:
            SourceStep = Next - Curr
        else:
            SourceStep = Curr - Prev
        if SourceBinLeft >= TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = SourceStep
            TargetValue += Delta * SourceValue
            SourceIndex += 1
        elif SourceBinLeft < TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = Curr + 0.5 * SourceStep - TargetBinLeft
            TargetValue += Delta * SourceValue
            SourceIndex += 1
        elif SourceBinLeft >= TargetBinLeft and SourceBinRight > TargetBinRight:
            Delta = TargetBinRight - Curr + 0.5 * SourceStep
            TargetValue += Delta * SourceValue
            Values.append(TargetValue / Step)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
        else:
            Values.append(SourceValue)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    if SourceIndex == DataLen and TargetValue != 0 and TargetBinIndex<TargetLen:
        Values.append(TargetValue / Step)
        TargetBinIndex += 1
        TargetValue = 0
    #filling right part of the target range with zeroes if not in source range
    while TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
    #forming the re-sampled data
    Result = tuple((Position, Values[Index])
                                for Index, Position in enumerate(TargetBins))
    return Result

def ResampleWeightedMean(Data: TData, Start: TReal, Stop: TReal,
                                                        Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the instanteneous,
    point-values of a function at the given points. The re-sampled instateneous,
    point-values are calculated as weighted mean of the values of the source
    bins overlapping with the respective target bin, where the weight is defined
    as the ratio of the length of the overlap to the total length of a source
    bin.
    
    The source bins boundaries are calculated as mid-points between 3
    consecutive positions, except for the left and right edges, where the
    boundaries are symmetric and calculated from 2 adjacent points.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorted in ascending order of X values
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    TargetBinIndex = 0
    TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
    TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    SourceIndex = 0
    Prev = None
    Curr = Data[SourceIndex][0]
    Next = Data[SourceIndex + 1][0]
    SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    DataLen = len(Data)
    TargetLen = len(TargetBins)
    Values = list()
    #skipping source points to the left of the target range
    while SourceBinRight <= TargetBinLeft and SourceIndex < DataLen:
        SourceIndex += 1
        if SourceIndex < DataLen:
            Prev = Data[SourceIndex - 1][0]
            Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    #filling left part of the target range with zeroes if not in source range
    while TargetBinRight <= SourceBinLeft and TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
        if TargetBinIndex < TargetLen:
            TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
            TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    #actual re-sampling
    TargetValue = 0
    AllWeights = 0
    while TargetBinIndex < TargetLen and SourceIndex < DataLen:
        SourceValue = Data[SourceIndex][1]
        if SourceIndex > 0:
            Prev = Data[SourceIndex - 1][0]
        else:
            Prev = None
        Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
        SourceStep = SourceBinRight - SourceBinLeft
        if SourceBinLeft >= TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = SourceStep
            TargetValue += SourceValue
            AllWeights += 1
            SourceIndex += 1
        elif SourceBinLeft < TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = Curr + 0.5 * SourceStep - TargetBinLeft
            Weight = Delta / SourceStep
            TargetValue += Weight * SourceValue
            AllWeights += Weight
            SourceIndex += 1
        elif SourceBinLeft >= TargetBinLeft and SourceBinRight > TargetBinRight:
            Delta = TargetBinRight - Curr + 0.5 * SourceStep
            Weight = Delta / SourceStep
            TargetValue += Weight * SourceValue
            AllWeights += Weight
            Values.append(TargetValue / AllWeights)
            TargetBinIndex += 1
            TargetValue = 0
            AllWeights = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
        else:
            Values.append(SourceValue)
            TargetBinIndex += 1
            TargetValue = 0
            AllWeights = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    if SourceIndex == DataLen and TargetValue != 0 and TargetBinIndex<TargetLen:
        Values.append(TargetValue / AllWeights)
        TargetBinIndex += 1
        TargetValue = 0
        AllWeights = 0
    #filling right part of the target range with zeroes if not in source range
    while TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
    #forming the re-sampled data
    Result = tuple((Position, Values[Index])
                                for Index, Position in enumerate(TargetBins))
    return Result

def ResampleSum(Data: TData, Start: TReal, Stop: TReal, Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the integrals of a
    function within the source bins intervals. The re-sampled values are
    calculated as weighted sum of the values of the source bins overlapping with
    the respective target bin, where the weight is defined as the ratio of the
    length of the overlap to the total length of a source bin. Thus, the new
    values are the integrals of the function within the target bins intervals.
    
    The source bins boundaries are calculated as mid-points between 3
    consecutive positions, except for the left and right edges, where the
    boundaries are symmetric and calculated from 2 adjacent points.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorted in ascending order of X values
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    TargetBinIndex = 0
    TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
    TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    SourceIndex = 0
    Prev = None
    Curr = Data[SourceIndex][0]
    Next = Data[SourceIndex + 1][0]
    SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    DataLen = len(Data)
    TargetLen = len(TargetBins)
    Values = list()
    #skipping source points to the left of the target range
    while SourceBinRight <= TargetBinLeft and SourceIndex < DataLen:
        SourceIndex += 1
        if SourceIndex < DataLen:
            Prev = Data[SourceIndex - 1][0]
            Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
    #filling left part of the target range with zeroes if not in source range
    while TargetBinRight <= SourceBinLeft and TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
        if TargetBinIndex < TargetLen:
            TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
            TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    #actual re-sampling
    TargetValue = 0
    while TargetBinIndex < TargetLen and SourceIndex < DataLen:
        SourceValue = Data[SourceIndex][1]
        if SourceIndex > 0:
            Prev = Data[SourceIndex - 1][0]
        else:
            Prev = None
        Curr = Data[SourceIndex][0]
        if SourceIndex < (DataLen - 1):
            Next = Data[SourceIndex + 1][0]
        else:
            Next = None
        SourceBinLeft, SourceBinRight = GetBoundaries(Prev, Curr, Next)
        SourceStep = SourceBinRight - SourceBinLeft
        if SourceBinLeft >= TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = SourceStep
            TargetValue += SourceValue
            SourceIndex += 1
        elif SourceBinLeft < TargetBinLeft and SourceBinRight <= TargetBinRight:
            Delta = Curr + 0.5 * SourceStep - TargetBinLeft
            Weight = Delta / SourceStep
            TargetValue += Weight * SourceValue
            SourceIndex += 1
        elif SourceBinLeft >= TargetBinLeft and SourceBinRight > TargetBinRight:
            Delta = TargetBinRight - Curr + 0.5 * SourceStep
            Weight = Delta / SourceStep
            TargetValue += Weight * SourceValue
            Values.append(TargetValue)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
        else:
            Values.append(SourceValue * Step / SourceStep)
            TargetBinIndex += 1
            TargetValue = 0
            if TargetBinIndex < TargetLen:
                TargetBinLeft = TargetBins[TargetBinIndex] - 0.5 * Step
                TargetBinRight = TargetBins[TargetBinIndex] + 0.5 * Step
    if SourceIndex == DataLen and TargetValue != 0 and TargetBinIndex<TargetLen:
        Values.append(TargetValue)
        TargetBinIndex += 1
        TargetValue = 0
    #filling right part of the target range with zeroes if not in source range
    while TargetBinIndex < TargetLen:
        Values.append(0)
        TargetBinIndex += 1
    #forming the re-sampled data
    Result = tuple((Position, Values[Index])
                                for Index, Position in enumerate(TargetBins))
    return Result

def ResampleMean(Data: TData, Start: TReal, Stop: TReal, Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the instanteneous,
    point-values of a function at the given points. The re-sampled instateneous,
    point-values are calculated as arithmetic mean of the values at the central
    positions falling within the respective target bin. Makes sense only if the
    target intervals are broader than the source ones.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorting by X values is not required
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs, sorted by X values in ascending order
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    TargetLen = len(TargetBins)
    RealStop = TargetBins[-1]
    Sums = list(0 for _ in range(TargetLen))
    Counts = list(0 for _ in range(TargetLen))
    for Position, Value in Data:
        if Position < Start - 0.5 * Step or Position > RealStop + 0.5 * Step:
            continue
        Index = bisect_left(TargetBins, Position - 0.5 * Step)
        Sums[Index] += Value
        Counts[Index] += 1
    Temp = list()
    for Index, Position in enumerate(TargetBins):
        Count = Counts[Index]
        Value = Sums[Index]
        if Count != 0:
            Temp.append((Position, Value / Count))
        else:
            Temp.append((Position, 0))
    Result = tuple(Temp)
    return Result

def ResampleInterpolation(Data: TData, Start: TReal, Stop: TReal,
                                                        Step: TReal) -> TData:
    """
    Re-samples f(x) data from an arbitrary varying lengths intervals onto an
    equidistant mesh. The f(x) values are supposed to be the instanteneous,
    point-values of a function at the given points. The re-sampled instateneous,
    point-values are calculated using linear interpolation between two closest
    positions in the source data.
    
    Signature:
        seq(seq(int OR float, int OR float)), int OR float, int OR float,
            int > 0 OR float > 0 -> tuple(tuple(int OR float, int OR float))
    
    Args:
        Data: seq(seq(int OR float, int OR float)); the input data as (X, Y)
            pairs, sorted by X values in ascending order
        Start: int OR float; exact center of the left-most target bin
        Stop: int OR float; desired (approximate) center of the right-most
            target bin
        Step: int > 0 OR float > 0; the exact length of a target bin
    
    Returns:
        tuple(tuple(int OR float, int OR float)): the resampled data as (X, Y)
            pairs, sorted by X values in ascending order
    
    Raises:
        Exception: type or value or any argument is not acceptable
    
    Version 1.0.0.0
    """
    _CheckDataPoints(Data)
    _CheckStartStop(Start, Stop)
    _CheckStep(Step)
    TargetBins = GenerateXPoints(Start, Stop = Stop, Step = Step)
    SourceLen = len(Data)
    IndexSource = 0
    SourceX = Data[0][0]
    SourceY = Data[0][1]
    Values = list()
    for TargetX in TargetBins:
        if TargetX == SourceX:
            Values.append(SourceY)
        elif TargetX < SourceX:
            if IndexSource == 0:
                Values.append(0)
            else: #IndexSource > 0
                Slope = (SourceY - Data[IndexSource - 1][1]) / (
                                            SourceX - Data[IndexSource - 1][0])
                Value = SourceY + Slope * (TargetX - SourceX)
                Values.append(Value)
        else: # TargetX > SourceX
            if IndexSource >= SourceLen:
                Values.append(0)
            else:
                while IndexSource < SourceLen and TargetX > SourceX:
                    IndexSource += 1
                    if IndexSource >= SourceLen:
                        Values.append(0)
                        break
                    else:
                        SourceX = Data[IndexSource][0]
                        SourceY = Data[IndexSource][1]
                        if TargetX == SourceX:
                            Values.append(SourceY)
                            break
                        elif TargetX < SourceX:
                            Slope = (SourceY - Data[IndexSource - 1][1]) / (
                                            SourceX - Data[IndexSource - 1][0])
                            Value = SourceY + Slope * (TargetX - SourceX)
                            Values.append(Value)
                            break
                else: #while exited (source length) whitout finding a point
                    Values.append(0)
    Result = tuple(zip(TargetBins, Values))
    return Result
