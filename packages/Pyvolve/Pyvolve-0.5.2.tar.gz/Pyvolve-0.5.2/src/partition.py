#! /usr/bin/env python

##############################################################################
##  pyvolve: Python platform for simulating evolutionary sequences.
##
##  Written by Stephanie J. Spielman (stephanie.spielman@gmail.com) 
##############################################################################

'''
    This module defines the Partition() class, which indicates a particular evolutionary unit. 
'''

from model import * 



class Partition():

    def __init__(self, **kwargs):
        '''
            Required keyword arguments:
                
                1. **size**, integer giving the root length of this partition
                2. **models**, either a single Model object (for cases of branch homogeneity), or a list of Model objects (for cases of branch heterogeneity)
        
            Examples:
                .. code-block:: python

                   >>> # Define a temporally homogeneous partition
                   >>> my_partition = Partition(models = my_model, size = 500) 
                   
                   >>> # Define a temporally heterogeneous partition, in which three models (model1, model2, and rootmodel) are used during sequence evolution, and rootmodel is the model at the root of the tree
                   >>> my_other_partition = Partition(models = [model1, model2, rootmodel], size = 134, root_model_name = rootmodel.name)       
                
        '''
                
                
        self.size              = kwargs.get('size', None)   # List of integers representing partition length. If there is no rate heterogeneity, then the list is length 1. Else, list is length k, where k is the number of rate categories.
        if self.size == None:
                self.size = []
        self.models            = kwargs.get('models', None)  # List of models associated with this partition. When length 1 (or not provided as a list) temporally homogeneous.
        self.root_model_name   = kwargs.get('root_model_name', None)  # NAME of Model beginning evolution at root of tree. Used under *branch heterogeneity*, and should be None or False if process is temporally homogeneous. If there is branch heterogeneity, this string *MUST* correspond to one of the Model() object's names.
        self.shuffle           = False # Shuffle sites after evolving?
        self._root_model       = None  # The actual root model object.

        self._partition_sanity()
        self._divvy_partition_size()



    def _partition_sanity(self):
        ''' 
            Sanity checks that Partition has been properly setup.
        '''
        
        # Ensure that self.models is a list
        if type(self.models) is not list:
            self.models = [self.models]

        # Assign _root_model
        if self.branch_het():
            for m in self.models:
                if m.name == self.root_model_name:
                    self._root_model = m
        else:
            self._root_model = self.models[0] 
        assert(self._root_model != None), "\n Root model not properly assigned in your partition. Make sure that you specified a root model name if you have branch heterogeneity! Do so with the argument root_model_name."
 
        # Ensure branch-site is ok - number of rate categories has to be the same across branches.
        if self.site_het():
            self.shuffle = True
            for model in self.models:
                assert( len(model.rate_probs) == len(self._root_model.rate_probs) ), "For branch-site models, the number of rate categories must remain constant over the tree in a given partition."


    def _divvy_partition_size(self):
        '''
            Turn size attribute into a list of different rate-heterogeneity size chunks (based on rate_probs to model object).
            If no rate heterogeneity, will simply be a list of length 1 containing full size.
        '''
        full = int( self.size )
        remaining = full
        new_size = []
        for i in range(self._root_model.num_classes() - 1):
            section = int( self._root_model.rate_probs[i] * full )
            new_size.append( section )
            remaining -= section
        new_size.append(remaining)  
                                     
        assert( sum(new_size) ==  full ), "\n\nImproperly divvied up rate heterogeneity."
        self.size = new_size

    
    def branch_het(self):
        ''' 
            Return True if the partition uses branch heterogeneity, and False if homogeneous.
        '''
        if isinstance(self.models, Model) or len(self.models) == 1:
            return False
        elif len(self.models) > 1:
            return True
        else:
            raise AssertionError("\n\nPartition has no associated models.")

    def site_het(self):
        ''' 
            Return True if the partition uses site/rate heterogeneity, and False if homogeneous.
        '''
        if self.models[0].num_classes() > 1:
            return True
        else:
            return False
    
    
    def is_codon_model(self):
        '''
            Return True if the partition is evolving with dN/dS heterogeneity, and False otherwise.
        '''
        return self.models[0].is_codon_model()

