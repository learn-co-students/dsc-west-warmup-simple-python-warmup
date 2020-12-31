import os
import glob
import types

import pickle as pkl

import numpy as np
import pandas as pd
import math

import sklearn.neighbors
import sklearn

from IPython.display import Markdown, display

from dataclasses import dataclass, field




class Test():
    """
        Provides a way for students to check their objects against 
        objects created in solution cells

        How to use this class
        ---------------------

        In a solution cell: 

        once you have an object you would like students to replicate,
        call Test().save(object, object_nickname) to pkl the object
        in a class-defined directory

            This will: 
                - check to see if there's a directory at the level of the book called test_obj, 
                and create it if there's not.  (The directory name can be altered 
                with the attribute Test().dir)

                - check to see if there's a file at the path f"test_obj/{object_nickname+'.pkl'}"
                If there is, it is deleted.  (This allows for writing Test().save once and 
                re-saving the object every time the cell is run)

                - pkl the object and save it at the path f"test_obj/{object_nickname+'.pkl'}"

        In a student-facing cell: 

        call Test().run_test(student_object, object_nickname) and have students run the cell
        to check whether their object matches the pkl'd object

            This will: 
                - import the pkl'd object at the path f"test_obj/{object_nickname+'.pkl'}"

                - run an assert against the student-created object "student_object" and the pkl'd object

                - print "Hey, you did it.  Good job" if an AssertError is not thrown, "try again" if one is

                - the variable name of the first parameter is not bound by anything and need not be
                the original name of the object that was pkl'd.  It's up to the instructor whether
                to
                    - tell students to create an object with a specific name, and pre-populate
                    Test.run_test() with that name as the first parameter

                    - not specify a name for students to assign student_object, but rely on
                    the student to place their object as the first parameter for Test.run_test()


        Type-specific assert methods
        ----------------------------

        Some types need additional methods to be asserted.  

        Examples include numpy arrays, pandas series and dataframes.  

        These type-specific methods are run if an object of that type is the first
        parameter for Test().run_test

        A dictionary containing these type-specific assert methods is stored in Test().obj_tests_dict 
        with the type as the key.

        There is a Test().obj_tests_dict_kwargs attribute which contains parameters to pass to 
        type-specific assertion methods.  

        For example: the dataframe assertion method has a "check_like" parameter which ignores the sort order
        and will assert True if identical frames sorted differently are compared.  This class 
        sets "check_like" to True by default.


        Is this robust for students with Windows filepaths?
        ---------------------------------------------------
        Should be!
    """
    
    def __init__(self, directory='test_obj'):
                
        self.directory=directory
        
        self.obj_tests_dict = {
                np.ndarray: np.testing.assert_array_equal,
                pd.core.series.Series: pd.testing.assert_series_equal,
                pd.core.frame.DataFrame: pd.testing.assert_frame_equal,
                pd.core.indexes.base.Index: pd.testing.assert_index_equal,
                types.MethodType: lambda x, y: x.__code__.co_code == y.__code__.co_code,
                sklearn.neighbors._classification.KNeighborsClassifier: self.parse_model,
                sklearn.neighbors._regression.KNeighborsRegressor: self.parse_model,
                sklearn.linear_model.LinearRegression: self.parse_model,
                sklearn.tree._classes.DecisionTreeRegressor: self.parse_model,
                sklearn.tree._classes.DecisionTreeClassifier: self.parse_model,
                sklearn.ensemble._forest.RandomForestClassifier: self.parse_model,
                sklearn.ensemble._forest.RandomForestRegressor: self.parse_model
        }

        self.obj_tests_dict_kwargs = {
            np.ndarray: {},
            pd.core.series.Series: {},
            pd.core.frame.DataFrame: {'check_like': True},
            pd.core.indexes.base.Index: 
                {'check_names': False,
                 'check_exact': False,
                 'check_less_precise': True
                },
            types.MethodType: {},
            sklearn.neighbors._classification.KNeighborsClassifier: 
                None,
            sklearn.neighbors._regression.KNeighborsRegressor:
                None,
            sklearn.linear_model.LinearRegression: None,
            sklearn.tree._classes.DecisionTreeRegressor: None,
            sklearn.tree._classes.DecisionTreeClassifier: None,
            sklearn.ensemble._forest.RandomForestClassifier: None,
            sklearn.ensemble._forest.RandomForestRegressor: None
            
        }
        
        self.assert_dict = {
            'float': math.isclose
        }

        return        
    
    def parse_model(self, model_1, model_2, *args):
        '''
        compare .__dict__ values of two given models
        
        will compare list of values if given in *args
        
        if none given, will compare all key/item pairs in model.__dict__'s
        '''
        model_1_dict = dict(model_1.__dict__)
        model_2_dict = dict(model_2.__dict__)
        
        tree_removal = ['_tree', 'tree_']
        
        tree_values = []
        
        if 'tree_' in model_1_dict.keys() or 'tree_' in model_2_dict.keys():
            tree_values = [arg for arg in args if arg in dir(model_1_dict['tree_'])]
            tree_removal = ['_tree']
            args = [arg for arg in args if arg not in tree_values]
        
        #if values to test were passed, only include those to test
        if args:
            for index, arg in enumerate(args):
                    assert arg in model_1_dict.keys(), f"looks like your model object doesn't have {arg} values?"
                    assert arg in model_2_dict.keys(), f"looks like your model object doesn't have {arg} values?"                    
           
            model_1_dict_new = {key:val for key, val in model_1_dict.items() if key in args and key not in tree_removal}
            model_2_dict_new = {key:val for key, val in model_2_dict.items() if key in args and key not in tree_removal} 
        
        #if not given values to test, remove tree_ and _tree from both model dicts 
        else:
            model_1_dict_new = {key:val for key, val in model_1_dict.items() if key not in tree_removal} 
            model_2_dict_new = {key:val for key, val in model_2_dict.items() if key not in tree_removal} 
        
        #assert values
        if args:
            for key in model_1_dict_new:
                print(f"testing {key} values")
                if key == 'tree_':
                    continue
                self.run_assert(
                    model_1_dict_new[key],
                    model_2_dict_new[key],
                    flag = f"the first failed test compared {key} values"
                    )
                print(f"{key} values passed")
                print()
        
        #assert underyling tree values if they were passed
        if 'tree_values':
            for value in tree_values:
                print(f"testing {value} values in the underlying tree")
                model_1_dict_new = dict(model_1.__dict__)
                model_2_dict_new = dict(model_2.__dict__)
                self.run_assert(
                    getattr(model_1_dict_new['_tree'], value),
                    getattr(model_2_dict_new['_tree'], value),
                    flag = f"the first failed test compared {value} values in the underlying tree"
                )
                print(f"{value} in underlying tree passed")
                
        #reset value in kwargs dict:
        self.update_obj_tests_dict_kwargs(type(model_1), {})
        
        return 
    
    
    def test_dir(self):
        '''
        check if test_obj dir is there; if not, create it
        '''

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

        return

    def get_file_name(self, glob_listing):
        '''
        gets str of one file name in test_obj dir w/o .pkl extension

        Parameters:
            glob_listing: single returned object from glob

        Output:
            str of file name w/o .pkl extension
        '''

        #get filename
        directory, file_name = os.path.split(glob_listing)
        
        # remove .pkl
        listing, file_extension = os.path.splitext(file_name)
        return listing

    def save_ind(self, object, object_name):
        '''
        saves object to test_obj dir w/ object_name.pkl

        Parameters:
            object: object to pkl
            object_name: pkl file name
        '''
        
        with open(os.path.join(self.directory, f'{object_name}.pkl'), 'wb') as f:
            pkl.dump(object, f)

        return

    def save(self, object, object_name):
        '''
        parse test_obj dir to see if object_name.pkl prev saved
        if so, delete it

        save object under f'test_obj/{object_name}.pkl'

        Parameters:
            object: object to save as pkl file
            object_name: name to save pkl object as under f'test_obj/{object_name+".pkl"}'

        '''
        self.test_dir()

        files = glob.glob(
            os.path.join(
                self.directory, f'{object_name}.pkl'
            )
        )

        existing_files = [self.get_file_name(file) for file in files]

        if object_name+'.pkl' in existing_files:
            os.remove(
                os.path.join(
                    self.directory, f'{object_name}.pkl'
                )
            )

        self.save_ind(object, object_name)

        return

    def load_ind(self, object_name):
        '''
        loads and unpkls object from f"self.dir/{object_name+'.pkl'}"

        returns: unpkl'd object
        '''

        with open(os.path.join(self.directory, f'{object_name}.pkl'), 'rb') as f:
            obj = pkl.load(f)

        return obj

    def output(self, result=True):

        if result:
            display(Markdown('✅ **Hey, you did it.  Good job.**'))
        else:
            display(Markdown('❌ **Try Again**'))

    def update_obj_tests_dict_kwargs(self, obj_type, update_obj):
        '''
        updates self.obj_tests_dict_kwargs to pass parameters
        to specific assert statements
        
        Parameters
        __________
        
        obj_type: 
        type of object, acts as key to self.obj_tests_dict_kwargs
        
        update_obj:
        obj to replace self.obj_tests_dict_kwargs[obj_type]
        '''
        
        self.obj_tests_dict_kwargs[obj_type] = update_obj
            
        return
    
    def run_assert(self, obj1, obj2, *args, flag=None, asserts=None):
        
        assert type(obj1) == type(obj2), "objects not the same type?"
        
        kind = type(obj1) 

        #if the type of object has a specific type assert in obj_tests_dict:
        if kind in self.obj_tests_dict.keys():
            if args:
                self.update_obj_tests_dict_kwargs(kind, *args)
            
            #if there's a dictionary of kwargs in obj_tests_dict_kwargs:
            if type(self.obj_tests_dict_kwargs[kind]) == dict:
                self.obj_tests_dict[kind](
                    obj1, 
                    obj2, 
                    **self.obj_tests_dict_kwargs[kind]
                )
            
            #If there's another type of obj in obj_tests_dict_kwargs:
            elif type(self.obj_tests_dict_kwargs[kind]) != type(None):
                self.obj_tests_dict[kind](
                    obj1, 
                    obj2, 
                    *self.obj_tests_dict_kwargs[kind]
                )
                
            
            #if there are no kwargs:
            else:
                self.obj_tests_dict[kind](
                    obj1, 
                    obj2, 
                )
                

        else:
            
            if asserts==None:
                assert obj1 == obj2, flag
                 
            elif asserts=='float':
                assert self.assert_dict[asserts](obj1, obj2, abs_tol=.01)
        
    
    def run_test(self, obj, name, *args, flag=None, asserts=None):
        '''
        runs assert against obj and f"self.dir/{name+'.pkl'}"

        checks type of obj and, if type has assert method in self.obj_tests_dict, runs
        that assert method instead.  Any kwargs for that assert method in 
        obj_tests_dict_kwargs are also passed.
        '''
        test_obj = self.load_ind(name)

        self.run_assert(obj, test_obj, *args, flag=flag, asserts=asserts)