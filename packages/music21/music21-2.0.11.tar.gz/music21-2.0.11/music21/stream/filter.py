
import inspect 
import unittest
from music21 import common
from music21.common import opFrac

#------------------------------------------------------------------------------

class StreamFilter(object):
    '''
    A filter is an object that when called returns True or False
    about whether an element in the stream matches the filter.
    
    A lambda expression: `lambda el, iterator: True if EXP else False` can also be
    used as a very simple filter. 
    
    Filters can also raise StopIteration if no other elements in this Stream
    can possibly fit.
    '''
    derivationStr = 'streamFilter'
    
    def __init__(self):
        pass # store streamIterator?


class ClassFilter(StreamFilter):
    '''
    >>> s = stream.Stream()
    >>> s.append(note.Note('C'))
    >>> s.append(note.Rest())
    >>> s.append(note.Note('D'))
    >>> sI = s.__iter__()
    >>> sI
    <music21.stream.iterator.StreamIterator object at 0x...>
    >>> for x in sI:
    ...     print(x)
    <music21.note.Note C>
    <music21.note.Rest rest>
    <music21.note.Note D>

    >>> sI.filters.append(stream.filter.ClassFilter('Note'))
    >>> sI.filters
    [<music21.stream.filter.ClassFilter object at 0x...>]
    >>> for x in sI:
    ...     print(x)
    <music21.note.Note C>
    <music21.note.Note D>
    
    ''' 
    derivationStr = 'getElementsByClass'

    def __init__(self, classList=()):
        super(ClassFilter, self).__init__()


        self._classListHasStrings = False
        self._classListHasTypes = False

        if not common.isListLike(classList):
            classList = (classList,)
            
        self.classList = classList
        for c in classList:
            if isinstance(c, str):
                self._classListHasStrings = True
            elif inspect.isclass(c):
                self._classListHasTypes = True

    def __call__(self, item, iterator):
        eClasses = item.classes 
        for className in self.classList:
            if self._classListHasStrings and className in eClasses:
                return True
            elif self._classListHasTypes and isinstance(item, className):
                return True
        return False


class ClassNotFilter(ClassFilter):
    '''
    Returns elements not of the class.

    >>> s = stream.Stream()
    >>> s.append(note.Note('C'))
    >>> s.append(note.Rest())
    >>> s.append(note.Note('D'))
    >>> sI = s.__iter__()

    >>> sI.filters.append(stream.filter.ClassNotFilter('Note'))
    >>> sI.filters
    [<music21.stream.filter.ClassNotFilter object at 0x...>]
    >>> for x in sI:
    ...     print(x)
    <music21.note.Rest rest>
    '''
    derivationStr = 'getElementsNotOfClass'

    def __call__(self, item, iterator):
        return not super(ClassNotFilter, self).__call__(item, iterator)


class GroupFilter(StreamFilter):
    '''
    Returns elements with a certain group.

    >>> n1 = note.Note("C")
    >>> n1.groups.append('trombone')
    >>> n2 = note.Note("D")
    >>> n2.groups.append('trombone')
    >>> n2.groups.append('tuba')
    >>> n3 = note.Note("E")
    >>> n3.groups.append('tuba')
    >>> s1 = stream.Stream()
    >>> s1.append(n1)
    >>> s1.append(n2)
    >>> s1.append(n3)
    >>> GF = stream.filter.GroupFilter
    
    >>> for thisNote in s1.__iter__().addFilter(GF("trombone")):
    ...     print(thisNote.name)
    C
    D
    >>> for thisNote in s1.__iter__().addFilter(GF("tuba")):
    ...     print(thisNote.name)
    D
    E

    '''
    derivationStr = 'getElementsByGroup'
    
    def __init__(self, groupFilterList):
        if not common.isListLike(groupFilterList):
            groupFilterList = [groupFilterList]
        self.groupFilterList = groupFilterList

    def __call__(self, item, iterator):
        eGroups = item.groups 
        for groupName in self.groupFilterList:
            if groupName in eGroups:
                return True
        return False

class OffsetFilter(StreamFilter):
    '''
    see iterator.getElementsByOffset()
    '''
    def __init__(self, offsetStart, offsetEnd=None,
                    includeEndBoundary=True, mustFinishInSpan=False,
                    mustBeginInSpan=True, includeElementsThatEndAtStart=True):
        self.offsetStart = opFrac(offsetStart)
        if offsetEnd is None:
            self.offsetEnd = offsetStart
            self.zeroLengthSearch = True
        else:
            self.offsetEnd = opFrac(offsetEnd)
            if offsetEnd > offsetStart:
                self.zeroLengthSearch = False
            else:
                self.zeroLengthSearch = True

        self.mustFinishInSpan = mustFinishInSpan
        self.mustBeginInSpan = mustBeginInSpan
        self.includeEndBoundary = includeEndBoundary
        self.includeElementsThatEndAtStart = includeElementsThatEndAtStart


    def __call__(self, e, iterator):
        dur = e.duration
        s = iterator.srcStream
        if s is e:
            return False
        offset = s.elementOffset(e)
        
        #offset = common.cleanupFloat(offset)

        if offset > self.offsetEnd:  # anything that ends after the span is definitely out
            if s.isSorted:
                # if sorted, optimize by breaking after exceeding offsetEnd
                # eventually we could do a binary search to speed up...
                raise StopIteration
            else:
                return False

        elementEnd = opFrac(offset + dur.quarterLength)
        if elementEnd < self.offsetStart:  # anything that finishes before the span ends is definitely out
            return False

        if dur.quarterLength == 0:
            elementIsZeroLength = True
        else:
            elementIsZeroLength = False


        # all the simple cases done! Now need to filter out those that are border cases depending on settings

        if self.zeroLengthSearch is True and elementIsZeroLength is True:
            # zero Length Searches -- include all zeroLengthElements
            return True


        if self.mustFinishInSpan is True:
            if elementEnd > self.offsetEnd:
                #environLocal.warn([elementEnd, offsetEnd, e])
                return False
            if self.includeEndBoundary is False:
                # we include the end boundary if the search is zeroLength -- otherwise nothing can be retrieved
                if elementEnd == self.offsetEnd:
                    return False

        if self.mustBeginInSpan is True:
            if offset < self.offsetStart:
                return False
            if self.includeEndBoundary is False:
                if offset >= self.offsetEnd:
                    # >= is unnecessary, should just be ==, but better safe than sorry
                    return False

        if self.mustBeginInSpan is False:
            if elementIsZeroLength is False:
                if elementEnd == self.offsetEnd and self.zeroLengthSearch is True:
                    return False
        if self.includeEndBoundary is False:
            if offset >= self.offsetEnd:
                return False

        if self.includeElementsThatEndAtStart is False and elementEnd == self.offsetStart:
            return False

        return True
    
    


class Test(unittest.TestCase):
    pass

if __name__ == '__main__':
    import music21
    music21.mainTest(Test)