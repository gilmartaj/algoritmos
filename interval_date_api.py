from collections import deque
from datetime import date
from datetime import timedelta
import math

class Date(object):

    def __init__(self, day, month = date.today().month, year = date.today().year):
        if not self.isValidDate(day, month, year):
            raise Exception("Invalid date {d}/{d}/{d}.".format(day, month, year))
        self._day = day
        self._month = month
        self._year = year
                
    def __eq__(self, other_date):
        return other_date != None and self.day == other_date.day and self.month == other_date.month and self.year == other_date.year
        
    def __ge__(self, other_date):
        return self == other_date or self > other_date
        
    def __gt__(self, other_date):
        if self.year > other_date.year:
            return True
        elif self.year < other_date.year:
            return False
        elif self.month > other_date.month:
            return True
        elif self.month < other_date.month:
            return False
        elif self.day > other_date.day:
            return True
        return False
                
    def __le__(self, other_date):
        return self == other_date or self < other_date
        
    def __lt__(self, other_date):
        #if self == Date.NEGATIVE_INFINITY and other_date != Date.NAGATIVE_INFINITY
         #   return True
        #elif self != Date.NEGATIVE_INFINITY and other_date == Date.NAGATIVE_INFINITY
         #   return False
        if self.year < other_date.year:
            return True
        elif self.year > other_date.year:
            return False
        elif self.month < other_date.month:
            return True
        elif self.month > other_date.month:
            return False
        elif self.day < other_date.day:
            return True
        return False
        
    def __str__(self):
        if self == Date.NEGATIVE_INFINITY(): return "-infinito"
        elif self == Date.POSITIVE_INFINITY(): return "+infinito"
        return "{:02d}/{:02d}/{:d}".format(self.day, self.month, self.year)
        
    def copy(self):
        if self == Date.NEGATIVE_INFINITY():
            return Date.NEGATIVE_INFINITY()
        if self == Date.POSITIVE_INFINITY():
            return Date.POSITIVE_INFINITY()
        return Date(self.day, self.month, self.year)
    
    def fromPythonDate(python_date):
        return Date(python_date.day, python_date.month, python_date.year)
        
    def fromString(date_string, is_initial = False):
        date_string = date_string.lower()
        if date_string == "-infinito" or date_string == "" and is_initial:
            return Date.NEGATIVE_INFINITY()
        elif date_string == "+infinito" or date_string == "" and not is_initial:
            return Date.POSITIVE_INFINITY()
        elements = list(map(lambda e: int(e), date_string.split('/')))
        if len(elements) == 1:
            return Date(elements[0])
        elif len(elements) == 2:
            return Date(elements[0], elements[1])
        return Date(elements[0], elements[1], elements[2])
            
    def isValidDate(self, day, month, year):
        if day < 1 or day > 31 or month < 1 or month > 12:
            return False
        
        leap_year = year % 4 == 0 and (not year % 100 == 0 or year % 400 == 0)
        months_with_30_days = (4, 6, 9, 11)
        
        if (month in months_with_30_days and day > 30) or (month == 2 and day > 28 + int(leap_year)):
            return False
        
        return True
        
    def NEGATIVE_INFINITY():
        date = Date(1,1,1)
        date._day = -math.inf
        date._month = -math.inf
        date._year = -math.inf
        return date
         
    def POSITIVE_INFINITY():
        date = Date(1,1,1)
        date._day = math.inf
        date._month = math.inf
        date._year = math.inf
        return date
        
    @property
    def day(self):
         return self._day
         
    @property
    def month(self):
         return self._month
         
    @property
    def year(self):
         return self._year
        
class SimpleDateInterval(object):
    def __init__(self, start_date = None, end_date = None):
        if start_date == None and end_date != None or start_date != None and end_date == None:
            raise Exception(f"Invalid Interval [{start_date}, {end_date}]")
        if start_date and end_date and start_date > end_date:
            raise Exception("Start date is greather than end date")
        self._start_date = start_date
        self._end_date = end_date
                      
    def __and__(self, other_date_interval):
        return self.intersection(other_date_interval)
           
    def __eq__(self, other_date_interval):
        return other_date_interval != None and self.start_date == other_date_interval.start_date and self.end_date == other_date_interval.end_date
             
    def __invert__(self):
        return self.complement()
        
    def __len__(self):
        if self.isNullDateInterval(): return 0
        if self.start_date == Date.NEGATIVE_INFINITY() or self.end_date == Date.POSITIVE_INFINITY(): return math.inf
        return (date(self.end_date.year, self.end_date.month, self.end_date.day) - date(self.start_date.year, self.start_date.month, self.start_date.day)).days + 1
             
    def __or__(self, other_date_interval):
        return self.union(other_date_interval)
        
    def __str__(self):
        if self.isNullDateInterval():
            return "[]"
        return f"[{self.start_date}, {self.end_date}]"
        
    def __sub__(self, other_date_interval):
        return self.subtraction(other_date_interval)
         
    def areStuckIntervals(date_interval1, date_interval2):
        first_date_interval = SimpleDateInterval.first(date_interval1, date_interval2)
        second_date_interval = date_interval1 if first_date_interval == date_interval2 else date_interval2
        if first_date_interval.intersection(second_date_interval).isNullDateInterval():
            auxiliar_python_date = date(first_date_interval.end_date.year, first_date_interval.end_date.month, first_date_interval.end_date.day)
            auxiliar_python_date += timedelta(days = 1)
            if(Date(auxiliar_python_date.day, auxiliar_python_date.month, auxiliar_python_date.year) == second_date_interval.start_date): 
                return True
        return False
         
    def complement(self):
        complement_intervals = []
        if self.isNullDateInterval():
            return SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY())
        if self.start_date != Date.NEGATIVE_INFINITY():
            auxiliar_date = date(self.start_date.year, self.start_date.month, self.start_date.day) - timedelta(days = 1)
            complement_intervals.append(SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.fromPythonDate(auxiliar_date)))
        if self.end_date != Date.POSITIVE_INFINITY():
            auxiliar_date = date(self.end_date.year, self.end_date.month, self.end_date.day) + timedelta(days = 1)
            complement_intervals.append(SimpleDateInterval(Date.fromPythonDate(auxiliar_date), Date.POSITIVE_INFINITY()))
        if len(complement_intervals) > 1:
             return MultipleDateInterval(complement_intervals)
        elif len(complement_intervals) == 1:
            return complement_intervals[0]
        return SimpleDateInterval(None, None)
              
    def contains(self, other_date_interval):
        return self.start_date <= other_date_interval.start_date and self.end_date >= other_date_interval.end_date
        
    def copy(self):
        return SimpleDateInterval(self.start_date.copy() if type(self.start_date) == Date else self.start_date, self.end_date.copy() if type(self.end_date) == Date else self.end_date)
        
    def first(date_interval1, date_interval2):
        return date_interval1 if date_interval1.start_date < date_interval2.start_date else date_interval2
                
    def hasIntersection(self, other_date_interval):
        if self.isNullDateInterval() or other_date_interval.isNullDateInterval():
            return False
        first_date_interval = SimpleDateInterval.first(self, other_date_interval)
        second_date_interval = self if first_date_interval == other_date_interval else other_date_interval
        if second_date_interval.start_date <= first_date_interval.end_date:
            return True
        return False
        
    def intersection(self, other_date_interval):
        if self.isNullDateInterval() or other_date_interval.isNullDateInterval():
            return SimpleDateInterval(None, None)
        if type(other_date_interval) is SimpleDateInterval:
            first_date_interval = SimpleDateInterval.first(self, other_date_interval)
            second_date_interval = self if first_date_interval == other_date_interval else other_date_interval
            if second_date_interval.start_date > first_date_interval.end_date:
                return SimpleDateInterval(None, None)
            if first_date_interval.end_date < second_date_interval.end_date:
                return SimpleDateInterval(second_date_interval.start_date, first_date_interval.end_date)
            return SimpleDateInterval(second_date_interval.start_date, second_date_interval.end_date)
        elif type(other_date_interval) is MultipleDateInterval:
            intersections = []
            for sdi in other_date_interval.simpleIntervals:
                intersection = self & sdi
                if not intersection.isNullDateInterval():
                    intersections.append(intersection)
            if len(intersections) == 0:
                return SimpleDateInterval(None, None)
            if len(intersections) == 1:
                return intersections[0]
            interval = MultipleDateInterval(intersections)
            if len(interval.simple_date_intervals) == 1:
                interval.simple_date_intervals[0]
            return interval
        
    def isNullDateInterval(self):
        return self.start_date == None
         
    def subtraction(self, other_date_interval):
        return self.intersection(other_date_interval.complement())
         
    def union(self, other_date_interval):
        if self.isNullDateInterval():
            return other_date_interval.copy()
        elif other_date_interval.isNullDateInterval():
            return self.copy()
        if type(other_date_interval) == MultipleDateInterval:
            return other_date_interval.union(self)
            
        first_date_interval = SimpleDateInterval.first(self, other_date_interval)
        second_date_interval = self if first_date_interval == other_date_interval else other_date_interval
        if self.isNullDateInterval():
            return SimpleDateInterval(other_date_interval.start_date, other_date_interval.end_date)
        elif other_date_interval.isNullDateInterval():
            return SimpleDateInterval(self.start_date, self.end_date)
        elif self.intersection(other_date_interval).isNullDateInterval():
            auxiliar_python_date = date(first_date_interval.end_date.year, first_date_interval.end_date.month, first_date_interval.end_date.day)
            auxiliar_python_date += timedelta(days = 1)
            if(Date(auxiliar_python_date.day, auxiliar_python_date.month, auxiliar_python_date.year) != second_date_interval.start_date):
                return MultipleDateInterval([first_date_interval, second_date_interval])
        return SimpleDateInterval(first_date_interval.start_date, second_date_interval.end_date if second_date_interval.end_date > first_date_interval.end_date else first_date_interval.end_date)
            
        #start_date = self.start_date if self.start_date < other_date_interval.start_date else other_date_interval.start_date
        #end_date = self.end_date if self.end_date > other_date_interval.end_date else other_date_interval.end_date
        #return SimpleDateInterval(start_date, end_date)
       
    @property  
    def end_date(self):
         return self._end_date
       
    @property
    def start_date(self):
         return self._start_date
         
class MultipleDateInterval(object):
    def __init__(self, intervals):
        self.simple_date_intervals = []
                
        for interval in intervals:
            if interval.isNullDateInterval():
                continue
            inserido = False
            for i in range(0, len(self.simple_date_intervals)):
                if interval.end_date < self.simple_date_intervals[i].start_date:
                    self.simple_date_intervals.insert(i, interval)
                    inserido = True
                    break
                elif interval.hasIntersection(self.simple_date_intervals[i]) or SimpleDateInterval.areStuckIntervals(interval, self.simple_date_intervals[i]):
                    self.simple_date_intervals[i] = self.simple_date_intervals[i] | interval
                    inserido = True
                    break
            if not inserido:
                self.simple_date_intervals.append(interval)
            revise = True
            while revise:
                revise = False
                for i in reversed(range(1, len(self.simple_date_intervals))):
                    if self.simple_date_intervals[i].hasIntersection(self.simple_date_intervals[i-1])|SimpleDateInterval.areStuckIntervals(self.simple_date_intervals[i], self.simple_date_intervals[i-1]):
                        self.simple_date_intervals[i-1] = self.simple_date_intervals[i].union(self.simple_date_intervals[i-1])
                        del self.simple_date_intervals[i]
                        revise = True
                        break


    def __and__(self, other_date_interval):
        return self.intersection(other_date_interval)
        
    def __eq__(self, other_date_interval):
        #return bool(self.simple_date_intervals & other_date_interval.simple_date_intervals)
        return type(other_date_interval) == MultipleDateInterval and self.simple_date_intervals == other_date_interval.simple_date_intervals
        
    def __invert__(self):
        return self.complement()
        
    def __len__(self):
        sum = 0
        for interval in self.simpleIntervals:
            sum += len(interval)
        return sum
        
    def __or__(self, other_date_interval):
        return self.union(other_date_interval)
        
    def __str__(self):
        string = "{ "
        if self.isNullDateInterval():
            return "{ Intervalo nulo }"
        for interval in self.simple_date_intervals:
            string += str(interval) + " | "
        return string[0:-2] + "}"
        
    def __sub__(self, other_date_interval):
        return self.subtraction(other_date_interval)
            
    def complement(self):
        complement_intervals = []
        if self.isNullDateInterval():
            return SimpleDateInterval(Date.NAGATIVE_INFINITY(), Date.POSITIVE_INFINITY())
        if len(self.simpleIntervals) == 1:
            return self.simpleIntervals[0].complement()
        
        if(self.simpleIntervals[0].start_date != Date.NEGATIVE_INFINITY()):
            end_date = Date.fromPythonDate(date(self.simpleIntervals[0].start_date.year, self.simpleIntervals[0].start_date.month, self.simpleIntervals[0].start_date.day) - timedelta(days = 1))
            complement_intervals.append(SimpleDateInterval(Date.NEGATIVE_INFINITY(), end_date))
            
        for i in range(1, len(self.simpleIntervals)):
            start_date = Date.fromPythonDate(date(self.simpleIntervals[i-1].end_date.year, self.simpleIntervals[i-1].end_date.month, self.simpleIntervals[i-1].end_date.day) + timedelta(days = 1))
            end_date = Date.fromPythonDate(date(self.simpleIntervals[i].start_date.year, self.simpleIntervals[i].start_date.month, self.simpleIntervals[i].start_date.day) - timedelta(days = 1))
            complement_intervals.append(SimpleDateInterval(start_date, end_date))
            
        if(self.simpleIntervals[-1].end_date != Date.POSITIVE_INFINITY()):
            start_date = Date.fromPythonDate(date(self.simpleIntervals[-1].end_date.year, self.simpleIntervals[-1].end_date.month, self.simpleIntervals[-1].end_date.day) + timedelta(days = 1))
            complement_intervals.append(SimpleDateInterval(start_date, Date.POSITIVE_INFINITY()))
            
        if len(complement_intervals) == 1:
            return complement_intervals[0]
        else:
            return MultipleDateInterval(complement_intervals)
            
            
        if self.start_date != Date.NEGATIVE_INFINITY():
            auxiliar_date = date(self.start_date.year, self.start_date.month, self.start_date.day) - timedelta(days = 1)
            complement_intervals.append(SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.fromPythonDate(auxiliar_date)))
        if self.end_date != Date.POSITIVE_INFINITY():
            auxiliar_date = date(self.end_date.year, self.end_date.month, self.end_date.day) + timedelta(days = 1)
            complement_intervals.append(SimpleDateInterval(Date.fromPythonDate(auxiliar_date), Date.POSITIVE_INFINITY()))
        return MultipleDateInterval(complement_intervals) if len(complement_intervals) > 0 else SimpleDateInterval(None, None)
          
    def copy(self):
        return MultipleDateInterval(self.simpleIntervals)
          
    def intersection(self, other_date_interval):
        intersections = []        
        if type(other_date_interval) == MultipleDateInterval:
            for interval1 in self.simple_date_intervals:
                for interval2 in other_date_interval.simple_date_intervals:
                    intersection = interval1.intersection(interval2)
                    if not intersection.isNullDateInterval():
                        intersections.append(intersection)
        elif type(other_date_interval) == SimpleDateInterval:
            return other_date_interval.intersection(self)
        if len(intersections) == 0:
            return SimpleDateInterval(None, None)
        if len(intersections) == 1:
            return intersections[0]
        interval = MultipleDateInterval(intersections)
        if len(interval.simple_date_intervals) == 1:
            interval.simple_date_intervals[0]
        return interval
        
    def isNullDateInterval(self):
        return len(self.simple_date_intervals) == 0
        
    def subtraction(self, other_date_interval):
        return self.intersection(other_date_interval.complement())
    
    def union(self, other_date_interval):
        if self.isNullDateInterval():
            return other_date_interval
        if other_date_interval.isNullDateInterval():
            return MultipleDateInterval(self.simple_date_intervals)
        intervals = []
        intervals.extend(self.simple_date_intervals)
        if type(other_date_interval) == SimpleDateInterval:
            intervals.append(other_date_interval)
        else:
            intervals.extend(other_date_interval.simple_date_intervals)
        interval = MultipleDateInterval(intervals)
        if len(interval.simple_date_intervals) == 1:
            return interval.simple_date_intervals[0]
        return interval
        
    @property         
    def simpleIntervals(self):
        return tuple(self.simple_date_intervals)

class IntervalCalculator:
    
    def calculateExpression(expression):
        postfix_expression = IntervalCalculator._infixToPostfix(IntervalCalculator._splitElements(expression))
        
        for i in range(0, len(postfix_expression)):
            if len(postfix_expression[i]) > 1:
                postfix_expression[i] = IntervalCalculator._stringToInterval(postfix_expression[i])
        return IntervalCalculator._evaluateExpression(postfix_expression)
    
    def _evaluateExpression(elements):
        operandStack = deque()
        for element in elements:
            if type(element) == SimpleDateInterval or type(element) == MultipleDateInterval:
                operandStack.append(element)
            else:
                result = None
                operand2 = operandStack.pop()
                if element == '!':
                    result = ~operand2 ###
                else:
                    operand1 = operandStack.pop()
                    if element == '&':
                        result = operand1.intersection(operand2)
                    elif element == '|':
                        result = operand1 | (operand2)
                    elif element == '-':
                        result = operand1 - (operand2)
                operandStack.append(result)
        return operandStack.pop()
    
    def _infixToPostfix(elements):
        operator_precedency = {'(': 0, '|': 1, '-':2, '!': 3, '&': 4}
        queue = deque()
        postfix_list = []
        for e in elements:
            if len(e) > 1:
                postfix_list.append(e)
            elif e == '(':
                queue.append(e)
            elif e == ')':
                top = queue.pop()
                while top != '(':
                    postfix_list.append(top)
                    top = queue.pop()
            else:
                while len(queue) > 0 and operator_precedency[queue[-1]] >= operator_precedency[e] and not (queue[-1] == '&' and e == '!'):
                    postfix_list.append(queue.pop())
                queue.append(e)
        
        while len(queue)> 0:
            postfix_list.append(queue.pop())
        
        return postfix_list

    def _splitElements(expressao):
        expressao = expressao.replace(" ", "")
        elements = []
        auxiliary = None
        type = None
        for i, c in enumerate(expressao):
            if c in ["(", "["] and not expressao[i+1] in ["(", "["]:
                auxiliary = c
                type = "interval"
            elif c in [")", "]"] and type == "interval":
                elements.append(auxiliary + c)
                auxiliary = None
                type = None
            elif type == "interval":
                auxiliary += c
            else: # if c in ["!", "-", "&", "|"]:
                elements.append(c)
        return elements
        
    def _stringToInterval(interval_string):
        interval_string = interval_string.replace(" ", "")
        if len(interval_string) < 3:
            return SimpleDateInterval(None, None)
        date1 = Date.fromString(interval_string[1:-1].split(",")[0], True)
        if  interval_string[0] == "(" and not date1 == Date.NEGATIVE_INFINITY() and not date1 == Date.POSITIVE_INFINITY():
            auxiliary_date = date(date1.year, date1.month, date1.day) + timedelta(days = 1)
            date1 = Date(auxiliary_date.day, auxiliary_date.month, auxiliary_date.year)
        date2 = Date.fromString(interval_string[1:-1].split(",")[1], False)
        if  interval_string[-1] == ")" and not date2 == Date.NEGATIVE_INFINITY() and not date2 == Date.POSITIVE_INFINITY():
            auxiliary_date = date(date2.year, date2.month, date2.day) - timedelta(days = 1)
            date2 = Date(auxiliary_date.day, auxiliary_date.month, auxiliary_date.year)
        return SimpleDateInterval(date1, date2)
  
import unittest
       
class TestMethods(unittest.TestCase):
       
    def testDate(self):
        self.assertEqual(Date(1,2,2015), Date(1,2,2015))
        self.assertTrue(Date(1,2,2020) != Date(1,2,2021))
        self.assertTrue(Date(1).day == Date(1,2).day == Date(1,3,2066).day == 1)
        self.assertTrue(Date(1,5).month == Date(1,5,2010).month == 5)
        self.assertTrue(Date(13, 12, 2000).year == 2000)
        self.assertTrue(Date(10,1,2010) > Date(1,1,2010))
        self.assertTrue(Date(10,1,2010) >= Date(1,1,2010))
        self.assertTrue(Date(10,1,2009) < Date(1,1,2010))
        self.assertTrue(Date(10,1,2009) <= Date(1,1,2010))
        self.assertEqual(str(Date(1,2,2015)), "01/02/2015")
        self.assertEqual(Date.POSITIVE_INFINITY(), Date.POSITIVE_INFINITY())
        self.assertEqual(Date.NEGATIVE_INFINITY(), Date.NEGATIVE_INFINITY())
        self.assertTrue(Date.POSITIVE_INFINITY() > Date.NEGATIVE_INFINITY())
        self.assertTrue(Date.POSITIVE_INFINITY() >= Date.NEGATIVE_INFINITY())
        self.assertTrue(Date.NEGATIVE_INFINITY() < Date.POSITIVE_INFINITY())
        self.assertTrue(Date.NEGATIVE_INFINITY() <= Date.POSITIVE_INFINITY())
        self.assertTrue(Date.NEGATIVE_INFINITY() < Date(1))
        self.assertTrue(Date.NEGATIVE_INFINITY() <= Date(1))
        self.assertTrue(Date.POSITIVE_INFINITY() > Date(1))
        self.assertTrue(Date.POSITIVE_INFINITY() >= Date(1))
        
        with self.assertRaises(Exception): Date(-1)
        with self.assertRaises(Exception): Date(1, 13)
        with self.assertRaises(Exception): Date(0, 0, 0)
        with self.assertRaises(Exception): Date(29, 2, 2100)
        
    def testSimpleInterval(self):
        self.assertEqual(SimpleDateInterval().start_date, None)
        self.assertEqual(SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)).start_date, Date(1,5,2012))
        self.assertEqual(SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)).end_date, Date(2,6,2017))
        self.assertEqual(str(SimpleDateInterval(Date(1,5,2012), Date(2,6,2017))), "[01/05/2012, 02/06/2017]")
        self.assertEqual(SimpleDateInterval(Date(10,12,2020), Date(10,12,2020)), SimpleDateInterval(Date(10,12,2020), Date(10,12,2020)))
        self.assertEqual(SimpleDateInterval(), SimpleDateInterval())
        self.assertEqual(SimpleDateInterval(Date(10,12,2020), Date(11,12,2020)), SimpleDateInterval(Date(10,12,2020), Date(11,12,2020)))
        with self.assertRaises(Exception): SimpleDateInterval(Date(1,5,2012), Date(2,6,2011))
        with self.assertRaises(Exception): SimpleDateInterval(Date(1,5,2012))
        with self.assertRaises(Exception): SimpleDateInterval(None, Date(2,6,2011))
        
    def testSimpleIntervalOperations(self):
        si1 = SimpleDateInterval(Date(1,5,2012), Date(2,6,2017))
        si2 = SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))
        si3 = SimpleDateInterval(Date(24,10,2014), Date(11,11,2021))
        si4 = SimpleDateInterval(Date(1,5,2012), Date(10,8,2017))
        si5 = SimpleDateInterval(Date(10,10,2015), Date(25,11,2015))
        
        self.assertEqual(SimpleDateInterval(None, None) | SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()))
        self.assertEqual(si1 | si2, MultipleDateInterval([si1, si2]))
        self.assertEqual(si1 | si4, SimpleDateInterval(Date(1, 5, 2012), Date(10, 8, 2017)))
        self.assertEqual(si1 | si2 | si3, SimpleDateInterval(Date(1,5,2012), Date(7,6,2022)))
        
        self.assertEqual(SimpleDateInterval(None, None) & SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()), SimpleDateInterval(None, None))
        self.assertEqual(si1 & si2, SimpleDateInterval())
        self.assertEqual(si1 & si3, SimpleDateInterval(Date(24,10,2014), Date(2,6,2017)))
        self.assertEqual(si2 & si3, SimpleDateInterval(Date(31,12,2020), Date(11,11,2021)))
        
        self.assertEqual(~SimpleDateInterval(None, None), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()))
        self.assertEqual(~SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()), SimpleDateInterval())
        self.assertEqual(~si1, MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(30, 4, 2012)), SimpleDateInterval(Date(3, 6, 2017), Date.POSITIVE_INFINITY())]))
        self.assertEqual(~SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(1,1,2000)), SimpleDateInterval(Date(2,1,2000), Date.POSITIVE_INFINITY()))
        self.assertEqual(~SimpleDateInterval(Date(1,1,2000), Date.POSITIVE_INFINITY()), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(31,12,1999)))
        
        self.assertEqual(SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()) - SimpleDateInterval(None, None), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()))
        self.assertEqual(SimpleDateInterval(None, None) - SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()), SimpleDateInterval(None, None))
        self.assertEqual(si2 - si3, SimpleDateInterval(Date(12,11,2021), Date(7,6,2022)))
        self.assertEqual(si1 - si5, MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(9,10,2015)), SimpleDateInterval(Date(26,11,2015), Date(2,6,2017))]))
        self.assertEqual(SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()) - si1, MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(30,4,2012)), SimpleDateInterval(Date(3,6,2017), Date.POSITIVE_INFINITY())]))
        
    def testMultipleInterval(self):
        self.assertEqual(MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))]),
                            MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))]))
        self.assertEqual(MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))]),
                            MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))]))
                            
    def testMultipleIntervalOperations(self):
        mi1 = MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(10,5,2020), Date(20,6,2020))])
        mi2 = MultipleDateInterval([SimpleDateInterval(Date(10,4,2012), Date(12,6,2012)), SimpleDateInterval(Date(21,6,2020), Date(25,6,2020))])
        
        mi1_u_mi2 = MultipleDateInterval([SimpleDateInterval(Date(10,4,2012), Date(2,6,2017)), SimpleDateInterval(Date(10,5,2020), Date(25,6,2020))])
        
        self.assertEqual(mi1 | mi2, mi1_u_mi2)
        mi1_i_mi2 = SimpleDateInterval(Date(1,5,2012), Date(12,6,2012))
        self.assertEqual(mi1 & mi2, mi1_i_mi2)
        
        mi3 = MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,5,2012)), SimpleDateInterval(Date(30,7,2012), Date(22,11,2012)), SimpleDateInterval(Date(14,1,2018), Date(20,6,2018))])
        mi4 = MultipleDateInterval([SimpleDateInterval(Date(10,8,2012), Date(11,9,2012)), SimpleDateInterval(Date(30,7,2014), Date(25,11,2014)), SimpleDateInterval(Date(31,1,2018), Date(29,6,2018))])
        mi3_i_mi4 = MultipleDateInterval([SimpleDateInterval(Date(10,8,2012), Date(11,9,2012)), SimpleDateInterval(Date(31,1,2018), Date(20,6,2018))])
        self.assertEqual(mi3 & mi4, mi3_i_mi4)
        
        si1 = SimpleDateInterval(Date(30,11,2017), Date(27,2,2018))
        mi3_i_s11_i_mi4 = SimpleDateInterval(Date(31,1,2018), Date(27,2,2018))
        self.assertEqual(mi3 & si1 & mi4, mi3_i_s11_i_mi4)
        self.assertEqual(mi3 & mi4 & si1, mi3_i_s11_i_mi4)
        
        mi1_inv = MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(30,4,2012)), SimpleDateInterval(Date(3,6,2017), Date(9,5,2020)), SimpleDateInterval(Date(21,6,2020), Date.POSITIVE_INFINITY())])
        self.assertEqual(~mi1, mi1_inv)
        mi13_inv = MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(30,4,2012)), SimpleDateInterval(Date(3,5,2012), Date(29,7,2012)), SimpleDateInterval(Date(23,11,2012), Date(13,1,2018)), SimpleDateInterval(Date(21,6,2018), Date.POSITIVE_INFINITY())])
        mi5 = MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(2,6,2017)), SimpleDateInterval(Date(10,5,2020), Date.POSITIVE_INFINITY())])
        mi5_inv = SimpleDateInterval(Date(3,6,2017), Date(9,5,2020))
        self.assertEqual(~mi5, mi5_inv)
        
        mi2_sub_mi1 = MultipleDateInterval([SimpleDateInterval(Date(10,4,2012), Date(30,4,2012)), SimpleDateInterval(Date(21,6,2020), Date(25,6,2020))])
        self.assertEqual(mi2 - mi1, mi2_sub_mi1)
        mi1_sub_mi2 = MultipleDateInterval([SimpleDateInterval(Date(13,6,2012), Date(2,6,2017)), SimpleDateInterval(Date(10,5,2020), Date(20,6,2020))])
        self.assertEqual(mi1 - mi2, mi1_sub_mi2)
        self.assertEqual(mi5 - SimpleDateInterval(Date(10,4,2012), Date(30,4,2012)), MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(9,4,2012)), SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(10,5,2020), Date.POSITIVE_INFINITY())]))
        
    def testExpressionCalculate(self):
        self.assertEqual(IntervalCalculator.calculateExpression("[1, 10]"), SimpleDateInterval(Date(1), Date(10)))
        self.assertEqual(IntervalCalculator.calculateExpression("(1, 10)"), SimpleDateInterval(Date(2), Date(9)))
        self.assertEqual(IntervalCalculator.calculateExpression("(1, 10]"), SimpleDateInterval(Date(2), Date(10)))
        self.assertEqual(IntervalCalculator.calculateExpression("[1, 10)"), SimpleDateInterval(Date(1), Date(9)))
        self.assertEqual(IntervalCalculator.calculateExpression("(([1, 10]))"), SimpleDateInterval(Date(1), Date(10)))
        
        self.assertEqual(IntervalCalculator.calculateExpression("[]"), SimpleDateInterval(None, None))
        self.assertEqual(IntervalCalculator.calculateExpression("[,]"), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()))
        
        self.assertEqual(IntervalCalculator.calculateExpression("![1/10/2015, 10/10/2015]"), MultipleDateInterval([SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date(30,9,2015)), SimpleDateInterval(Date(11,10,2015), Date.POSITIVE_INFINITY())]))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/10/2015, 10/10/2015]|(25/10/2017, 09/09/2018)"), MultipleDateInterval([SimpleDateInterval(Date(1,10,2015), Date(10,10,2015)), SimpleDateInterval(Date(26,10,2017), Date(8,9,2018))]))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/10/2015, 10/10/2015]&(25/10/2017, 09/09/2018)"), SimpleDateInterval(None, None))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/10/2015, 10/10/2015] - (25/10/2017, 09/09/2018)"), SimpleDateInterval(Date(1,10,2015), Date(10,10,2015)))
        
        self.assertEqual(IntervalCalculator.calculateExpression("[1/5/2012,2/6/2017]|[31/12/2020,7/6/2022]"), MultipleDateInterval([SimpleDateInterval(Date(1,5,2012), Date(2,6,2017)), SimpleDateInterval(Date(31,12,2020), Date(7,6,2022))]))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/5/2012,2/6/2017]|[1/5/2012,10/8/2017]"), SimpleDateInterval(Date(1,5,2012), Date(10,8,2017)))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/5/2012,2/6/2017]|[31/12/2020,07/06/2022]|[24/10/2014,11/11/2021]"), SimpleDateInterval(Date(1,5,2012), Date(7,6,2022)))
        self.assertEqual(IntervalCalculator.calculateExpression("[]|[,]"), SimpleDateInterval(Date.NEGATIVE_INFINITY(), Date.POSITIVE_INFINITY()))
        
        self.assertEqual(IntervalCalculator.calculateExpression("()&[,]"), SimpleDateInterval(None, None))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/10/2015, 10/10/2015]&(25/10/2017, 09/09/2018)"), SimpleDateInterval(None, None))
        self.assertEqual(IntervalCalculator.calculateExpression("[1/5/2012, 2/6/2017]&[24/10/2014, 11/11/2021]"), SimpleDateInterval(Date(24,10,2014), Date(2,6,2017)))
        self.assertEqual(IntervalCalculator.calculateExpression("[31/12/2020, 7/6/2022]&[24/10/2014, 11/11/2021]"), SimpleDateInterval(Date(31,12,2020), Date(11,11,2021)))
        
        self.assertEqual(IntervalCalculator.calculateExpression("[31/12/2020, 7/6/2022]&[24/10/2014, 11/11/2021]|([12/3/2099, 13/2/2101]|[1/1/1988, 10/11/1995])|([31/05/1990,+infinito])"), SimpleDateInterval(Date(1,1,1988),Date.POSITIVE_INFINITY()))
        
        self.assertEqual(IntervalCalculator.calculateExpression("[1/10/2002, 10/12/2017]|[5/6/1987, 18/11/1996]|[1/10/2056, 10/12/2088]&[15/3/2077, 10/12/2082]&!([10/10/2033, +infinito]|[, 10/10/2020])-[12/07/2022, 19/10/2026]"),
                    MultipleDateInterval([SimpleDateInterval(Date(5,6,1987), Date(18,11,1996)), SimpleDateInterval(Date(1,10,2002), Date(10,12,2017))]))