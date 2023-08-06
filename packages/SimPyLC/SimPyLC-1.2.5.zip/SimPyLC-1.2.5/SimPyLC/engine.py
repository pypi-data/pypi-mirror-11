# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

from datetime import *
from time import *
from threading import *
from traceback import *
import __builtin__

from base import _evaluate
from gui import *
from graphics import *
from scene import *
from chart import *
		
class _Functor:
	def __init__  (self, state):
		self._state = _evaluate (state)
		
	def __call__ (self):
		return self._state
		
	def __lt__ (self, other):
		return _Functor (self () < _evaluate (other))
	
	def __le__ (self, other):
		return _Functor (self () <= _evaluate (other))
	
	def __gt__ (self, other):
		return _Functor (self () > _evaluate (other))
	
	def __ge__ (self, other):
		return _Functor (self () >= _evaluate (other))
	
	def __eq__ (self, other):
		return _Functor (self () == _evaluate (other))
	
	def __ne__ (self, other):
		return _Functor (self () != _evaluate (other))
		
	def __neg__ (self):
		return _Functor (-self ())
		
	def __add__ (self, other):
		return _Functor (self () + _evaluate (other))
	
	def __sub__ (self, other):
		return _Functor (self () - _evaluate (other))
	
	def __mul__ (self, other):
		return _Functor (self () * _evaluate (other))
	
	def __div__ (self, other):
		return _Functor (float (self ()) / _evaluate (other))
		
	def __mod__ (self, other):
		return _Functor (self () % _evaluate (other))
		
	def __nonzero__ (self):
		return not not self ()
		
	def __bool__ (self):
		return nonzero (self)
		
class _Element:
	def __init__ (self):
		self.color = None
		if not Module._current is None:
			self._setPosition ()
			Module._current._pages [self._pageIndex] ._elements.append (self)

	def _setPosition (self):
		self._pageIndex, self._rowIndex, self._columnIndex = Module._pageIndex, Module._rowIndex, Module._columnIndex 
		Module._current._maxNrOfRows = max (Module._current._maxNrOfRows, self._rowIndex + 2)  # Leave room for page caption
		Module._current._maxNrOfColumns = max (Module._current._maxNrOfColumns, self._columnIndex + 1)
			
	def _isA (self, ClassName):			
		return isinstance (self, eval (ClassName))
		
class _Caption (_Element):
	def __init__ (self, text):
		_Element.__init__ (self)
		self._text = text
		
	def __call__ (self):
		return self._text
	
class _GroupCaption (_Caption):
	def __init__ (self, text, top = False):
		self._top = top
		_Caption.__init__ (self, text)

	def _setPosition (self):
		if self._top:
			Module._columnIndex += 1
			Module._rowIndex = 0
		else:
			Module._rowIndex += 1
		_Caption._setPosition (self)
		
class _PageCaption (_Caption):
	def __init__ (self, text):
		_Caption.__init__ (self, text)
		
	def _setPosition (self):
		Module._pageIndex += 1
		Module._current._pages.append (_Page ())
		Module._columnIndex = -1
		Module._rowIndex = -1
		_Caption._setPosition (self)
		
	def __call__ (self):
		return 'page {0}: {1}'.format (self._pageIndex + 1, self._text)

class _Circuit (_Element, _Functor):
	def __init__ (self, state):
		_Element.__init__ (self)
		_Functor .__init__ (self, state)
		self._forced = False
		
	def _write (self, value):
		self._state = value
		
	def _force (self):
		self._forced = True
		
	def _release (self):
		self._forced = False
		
	def _setPosition (self):
		if Module._pageIndex == -1:  # No _Captions, so just one long list of _Circuits
			Module._current._defaultFormat = True
			Module._pageIndex = 0
			Module._current._pages.append (_Page ())
			Module._columnIndex = 0
			Module._rowIndex = -1  # Use position of missing _PageCaption for first _Circuit
			
		Module._rowIndex += 1
		_Element._setPosition (self)
	
class _Follower (_Circuit):
	def __init__ (self, value):
		_Circuit.__init__ (self, value)
		
	def _follow (self, trueValue, condition = True, falseValue = None):
		if self._forced:
			return
		if _evaluate (condition):
			self._state = _evaluate (trueValue)
		else:
			if not falseValue is None:
				self._state = _evaluate (falseValue)		
				
class Marker (_Follower):
	def __init__ (self, value = False):
		_Follower.__init__ (self, value)
		
	def mark (self, trueValue, condition = True, falseValue = None):
		_Follower._follow (self, trueValue, condition, falseValue)
		
class Runner (Marker):
	def __init__ (self, value = True):
		Marker.__init__ (self, value)
		World.runner = self
		
class Oneshot (_Circuit):
	def __init__ (self, condition = False):
		_Circuit.__init__ (self, condition)
		self._oldCondition = condition
		
	def trigger (self, condition):
		if self._forced:
			return			
		self._state =  _evaluate (condition) and not self._oldCondition
		self._oldCondition = condition

class Latch (_Circuit):
	def __init__ (self, condition = False):
		_Circuit.__init__ (self, condition)

	def latch (self, condition):
		if self._forced:
			return
		if _evaluate (condition):
			self._state = True

	def unlatch (self, condition):
		if self._forced:
			return
		if _evaluate (condition):
			self._state = False
					
class Register (_Follower):
	def __init__ (self, value = 0):
		_Follower.__init__ (self, value)

	def set (self, trueValue, condition = True, falseValue = None):
		_Follower._follow (self, trueValue, condition, falseValue)

class Timer (_Circuit):
	def __init__ (self):
		_Circuit.__init__ (self, self._stateFromValue (0))
		self._value = 0  # Seconds as float
		
	def _stateFromValue (self, value):  # State is time when timer semantic value was 0
		return World.time () - value
	
	def _valueFromState (self, state):  # Value is timer semantic value for a certain state (stored time)
		return World.time () - state

	def reset (self, condition):
		if self._forced:
			return
		if _evaluate (condition):
			self._state = self._stateFromValue (0)
		
	def _force (self):
		self._forced = True
		self._value = self._valueFromState (self._state)
		
	def _release (self):
		self._forced = False
		self._state = self._stateFromValue (self._value)
		
	def __call__ (self):
		if self._forced:
			return self._value
		else:
			return self._valueFromState (self._state)
			
	def _write (self, value):
		if self._forced:
			self._value = value
		else:
			self._state = self._stateFromValue (value)
	
class _Page:
	def __init__ (self):
		self._elements = []
	
class Module:
	_current = None  # Place elements outside any module
	_id = -1
	
	def _getId (self):
		Module._id += 1
		return str (Module._id) 

	def __init__ (self, name = None):
		Module._current = self  # Place elements in this module
		self._name = name if name else self.__class__.__name__.lower ()
		Module._pageIndex = -1
		self._pages = []
		self._maxNrOfRows = 0
		self._maxNrOfColumns = 0
		self._defaultFormat = False
		
	def input (self, world):
		pass
		
	def sweep (self):
		pass
		
	def output (self, world):
		pass
		
	def group (self, text = '', top = False):
		setattr (self, Module._getId (self), _GroupCaption ('', top))
		setattr (self, Module._getId (self), _GroupCaption (text))
			
	def page (self, text = ''):
		setattr (self, Module._getId (self), _PageCaption (text))		
						
	def _setPublicElementNames (self):
		for var in vars (self):
			if not var.startswith ('_'):
				getattr (self, var) ._name = var
				
import inspect
				
class World (Thread):
	time = Register (0)  # Early because needed in Timer constructors
	startDateTime = datetime.now ()
	runner = True	# May be replaced by a Runner
	
	def __init__ (self, *parameters):
		Thread.__init__ (self)
		
		Module._current = None  # Place further elements outside any module
		self._modules = []
		self._scenes = []
		self._charts = []
		
		for parameter in parameters:
			if isinstance (parameter, Module):
				self._modules.append (parameter)
			elif isinstance (parameter, Scene):
				self._scenes.append (parameter)
			elif isinstance (parameter, Chart):
				self._charts.append (parameter)
				
		World._instance = self
		
		for module in self._modules:
			setattr (self, module._name, module)
			module._setPublicElementNames ()
			
		for chart in self._charts:
			chart.define (self)
				
		World.first = Marker (True)
		World.sleep = Register (0.02)
		World.period = Timer ()
		
		World.elapsed = Register (0)
		World.offset = Register (0)
						
		self.daemon = True
		self.start ()

		Graphics (self)
		Gui (self)	# Main thread, so this thread, so last
	
	def run (self):	# Module constructors called here, placing elements inside modules
		self._cycle ()		
		
	def _cycle (self):
		while True:
			World.elapsed.set ((datetime.now () - World.startDateTime) .total_seconds ())
						
			if World.runner:
				World.time.set (World.elapsed () - World.offset ())
				
				for module in self._modules:
					module.input (World._instance)
					module.sweep ()
					module.output (World._instance)
					
				for chart in self._charts:
					chart.adapt ()
					
				World.first.mark (False)
			else:
				World.offset.set(World.elapsed () - World.time ())

			World.period.reset (True)
			sleep (World.sleep ())
				
def abs (anObject):
	return __builtin__.abs (_evaluate (anObject))
	
def max (object0, object1):
	return __builtin__.max (_evaluate (object0), _evaluate (object1))

def min (object0, object1):
	return __builtin__.min (_evaluate (object0), _evaluate (object1))

def pow (object0, object1):
	return math.pow (_evaluate (object0), _evaluate (object1))

def sqrt (anObject):
	return math.sqrt (_evaluate (anObject))

def exp (anObject):
	return math.exp (_evalate (anObject))
	
def log (anObject):
	return math.log (_evalate (anObject))
	
def log10 (anObject):
	return math.log10 (_evalate (anObject))
	
def sin (anObject):
	return math.sin (_evaluate (anObject))
	
def cos (anObject):
	return math.cos (_evaluate (anObject))
	
def tan (anObject):
	return math.tan (_evaluate (anObject))

def limit (anObject, limit0, limit1 = None):
	if limit1 is None:
		limit1 = limit0
		limit0 = -limit0
	return min (max (anObject, limit0), limit1)
	