# Submitter: brizam(Martin del Campo, Briza)
# Partner  : devorek(DeVore, Kristen)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # set the class attribute below to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  

    def check(self,param,annot,value,check_history=''):
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        def mult_type_check(original):
            if not isinstance(value, original):
                raise AssertionError('type of '+str(value)+' '+'is not '+str(original))
            else:
                if len(annot) != 1:
                    if len(annot) != len(value):
                        raise AssertionError('len of '+str(annot)+' '+ 'is not the same as len of '+str(value))
                    else:
                        for value_one, value_two in zip(annot,value):
                            self.check(param, value_one, value_two, check_history)
                else:
                    for thing in value:
                        self.check(param, annot[0], thing, check_history)
                        
                        
        def diction_check(variable):
            if not isinstance(value,dict):
                raise AssertionError('type of '+str(value)+' '+'is not '+str(dict))
            
            else:
                if len(annot) == 1:
                    for value_one, value_two in annot.items():
                      pass
                    for item_one, item_two in value.items():
                        self.check(param, value_one, item_one, check_history)
                        self.check(param, value_two, item_two, check_history)
                else:
                    raise AssertionError('type of '+str(annot)+' '+'is not dict')
       
        
        def set_final(original):
            if not isinstance(value, original):
                raise AssertionError('type of '+str(value)+' '+'is not '+str(original))
            
            else:
                if len(annot) == 1:
                    for value_one in annot:
                        pass
                    for value_two in value:
                        self.check(param, value_one, value_two, check_history +str(original) + ' : ' + str(value_one) + ' was checked') #+new + 'values of the set have been checked' + str(value_one) + '\n')
                else:
                    raise AssertionError('type of '+str(annot)+' '+'is not set')
        
        
        def lambda_final(variable):
            if len(annot.__code__.co_varnames) != 1:
                raise AssertionError('type of '+str(annot.__code__.co_varnames)+' '+'is not correct')       
            else:
                try:
                    variable = annot(value)
                except:
                    raise AssertionError('type of '+str(annot.__code__.co_varnames)+' '+'is not correct')    
                else:
                    if variable:
                        pass
                    else:
                        raise AssertionError('type of '+str(annot.__code__.co_varnames)+' '+'is not correct')
        
        
        def str_final(variable):
            try:
                variable = eval(annot,self._variable)
            except:
                raise AssertionError('type of '+str(value)+' '+'is not str')
            else:
                if variable:
                    pass
                else:
                    raise AssertionError('type of '+str(value)+' '+'is not str')
            
          

        # Decode your annotation next; then check against argument        
        if annot == None:
            pass
        
        elif isinstance(annot,type): 
            if not isinstance(value, annot):
                raise AssertionError('type of '+str(value)+' '+'is not '+str(annot))
        elif isinstance(annot, list):
            mult_type_check(list)
        elif isinstance(annot, frozenset):
            set_final(frozenset)
        elif isinstance(annot, dict):
            diction_check(dict)
        elif isinstance(annot, set):
            set_final(set)
        elif isinstance(annot, tuple):
            mult_type_check(tuple)
        elif isinstance(annot, str): 
            str_final(str)
        elif inspect.isfunction(annot):
            lambda_final(annot)
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except:
                raise AssertionError('Error with either '+str(value)+' '+'or '+str(annot))

 
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict: the order parameters appear in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name  not in  bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        
        #    If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if self.checking_on == False and Check_Annotation.checking_on == False:
            return self._f(*args, **kargs)
       
        try:
           
            # Check the annotation for every parameter (if there is one)
            self._variable = param_arg_bindings()
            for parameter,value in param_arg_bindings().items():
                if parameter in self._f.__annotations__:
                    self.check(parameter,self._f.__annotations__[parameter],self._variable[parameter])#value)
                

              
            # Compute/remember the value of the decorated function
            val_of_dec_funct = self._f(*args, **kargs)
            
            # If 'return' is in the annotation, check it
            if 'return' in self._f.__annotations__:
               self.check(parameter,self._f.__annotations__['return'],val_of_dec_funct)  
            # Return the decorated answer
            return val_of_dec_funct
#     
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:

         #   print(80*'-')
         #   for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
         #       print(l.rstrip())
         #   print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
  #  def f(x:int): pass
    #f = Check_Annotation(f)
   # f(3)
   # f('a')
           
    import driver
    driver.driver()
