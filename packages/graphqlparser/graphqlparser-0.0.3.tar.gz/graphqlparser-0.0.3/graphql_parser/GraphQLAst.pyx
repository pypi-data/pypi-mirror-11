#/**
#* Copyright (c) 2015, Facebook, Inc.
#* All rights reserved.
#*
#* This source code is licensed under the BSD-style license found in the
#* LICENSE file in the root directory of this source tree. An additional grant
#* of patent rights can be found in the PATENTS file in the same directory.
#*/
## @generated

cimport cGraphQLAst

cdef class GraphQLAst:
    """Base class for all Ast pieces"""
    pass




cdef class GraphQLAstDocument(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstDocument *thing):
        node = GraphQLAstDocument()
        node._wrapped = thing
        return node



    def get_definitions_size(self):
        return int(cGraphQLAst.GraphQLAstDocument_get_definitions_size(self._wrapped))





cdef class GraphQLAstOperationDefinition(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstOperationDefinition *thing):
        node = GraphQLAstOperationDefinition()
        node._wrapped = thing
        return node



    def get_operation(self):
        val = cGraphQLAst.GraphQLAstOperationDefinition_get_operation(self._wrapped)
        if val is None:
            return None
        return (val)


    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstOperationDefinition_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_variable_definitions_size(self):
        return int(cGraphQLAst.GraphQLAstOperationDefinition_get_variable_definitions_size(self._wrapped))


    def get_directives_size(self):
        return int(cGraphQLAst.GraphQLAstOperationDefinition_get_directives_size(self._wrapped))


    def get_selection_set(self):
        cdef cGraphQLAst.GraphQLAstSelectionSet *next
        next = cGraphQLAst.GraphQLAstOperationDefinition_get_selection_set(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstSelectionSet.create(next)





cdef class GraphQLAstVariableDefinition(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstVariableDefinition *thing):
        node = GraphQLAstVariableDefinition()
        node._wrapped = thing
        return node



    def get_variable(self):
        cdef cGraphQLAst.GraphQLAstVariable *next
        next = cGraphQLAst.GraphQLAstVariableDefinition_get_variable(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstVariable.create(next)









cdef class GraphQLAstSelectionSet(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstSelectionSet *thing):
        node = GraphQLAstSelectionSet()
        node._wrapped = thing
        return node



    def get_selections_size(self):
        return int(cGraphQLAst.GraphQLAstSelectionSet_get_selections_size(self._wrapped))





cdef class GraphQLAstField(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstField *thing):
        node = GraphQLAstField()
        node._wrapped = thing
        return node



    def get_alias(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstField_get_alias(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstField_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_arguments_size(self):
        return int(cGraphQLAst.GraphQLAstField_get_arguments_size(self._wrapped))


    def get_directives_size(self):
        return int(cGraphQLAst.GraphQLAstField_get_directives_size(self._wrapped))


    def get_selection_set(self):
        cdef cGraphQLAst.GraphQLAstSelectionSet *next
        next = cGraphQLAst.GraphQLAstField_get_selection_set(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstSelectionSet.create(next)





cdef class GraphQLAstArgument(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstArgument *thing):
        node = GraphQLAstArgument()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstArgument_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)







cdef class GraphQLAstFragmentSpread(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFragmentSpread *thing):
        node = GraphQLAstFragmentSpread()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstFragmentSpread_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_directives_size(self):
        return int(cGraphQLAst.GraphQLAstFragmentSpread_get_directives_size(self._wrapped))





cdef class GraphQLAstInlineFragment(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstInlineFragment *thing):
        node = GraphQLAstInlineFragment()
        node._wrapped = thing
        return node



    def get_type_condition(self):
        cdef cGraphQLAst.GraphQLAstNamedType *next
        next = cGraphQLAst.GraphQLAstInlineFragment_get_type_condition(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstNamedType.create(next)


    def get_directives_size(self):
        return int(cGraphQLAst.GraphQLAstInlineFragment_get_directives_size(self._wrapped))


    def get_selection_set(self):
        cdef cGraphQLAst.GraphQLAstSelectionSet *next
        next = cGraphQLAst.GraphQLAstInlineFragment_get_selection_set(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstSelectionSet.create(next)





cdef class GraphQLAstFragmentDefinition(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFragmentDefinition *thing):
        node = GraphQLAstFragmentDefinition()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstFragmentDefinition_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_type_condition(self):
        cdef cGraphQLAst.GraphQLAstNamedType *next
        next = cGraphQLAst.GraphQLAstFragmentDefinition_get_type_condition(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstNamedType.create(next)


    def get_directives_size(self):
        return int(cGraphQLAst.GraphQLAstFragmentDefinition_get_directives_size(self._wrapped))


    def get_selection_set(self):
        cdef cGraphQLAst.GraphQLAstSelectionSet *next
        next = cGraphQLAst.GraphQLAstFragmentDefinition_get_selection_set(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstSelectionSet.create(next)





cdef class GraphQLAstVariable(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstVariable *thing):
        node = GraphQLAstVariable()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstVariable_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)





cdef class GraphQLAstIntValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstIntValue *thing):
        node = GraphQLAstIntValue()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstIntValue_get_value(self._wrapped)
        if val is None:
            return None
        return int(val)





cdef class GraphQLAstFloatValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFloatValue *thing):
        node = GraphQLAstFloatValue()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstFloatValue_get_value(self._wrapped)
        if val is None:
            return None
        return float(val)





cdef class GraphQLAstStringValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstStringValue *thing):
        node = GraphQLAstStringValue()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstStringValue_get_value(self._wrapped)
        if val is None:
            return None
        return (val)





cdef class GraphQLAstBooleanValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstBooleanValue *thing):
        node = GraphQLAstBooleanValue()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstBooleanValue_get_value(self._wrapped)
        if val is None:
            return None
        return bool(val)





cdef class GraphQLAstEnumValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstEnumValue *thing):
        node = GraphQLAstEnumValue()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstEnumValue_get_value(self._wrapped)
        if val is None:
            return None
        return (val)





cdef class GraphQLAstArrayValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstArrayValue *thing):
        node = GraphQLAstArrayValue()
        node._wrapped = thing
        return node



    def get_values_size(self):
        return int(cGraphQLAst.GraphQLAstArrayValue_get_values_size(self._wrapped))





cdef class GraphQLAstObjectValue(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstObjectValue *thing):
        node = GraphQLAstObjectValue()
        node._wrapped = thing
        return node



    def get_fields_size(self):
        return int(cGraphQLAst.GraphQLAstObjectValue_get_fields_size(self._wrapped))





cdef class GraphQLAstObjectField(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstObjectField *thing):
        node = GraphQLAstObjectField()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstObjectField_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)







cdef class GraphQLAstDirective(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstDirective *thing):
        node = GraphQLAstDirective()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstDirective_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)


    def get_arguments_size(self):
        return int(cGraphQLAst.GraphQLAstDirective_get_arguments_size(self._wrapped))





cdef class GraphQLAstNamedType(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstNamedType *thing):
        node = GraphQLAstNamedType()
        node._wrapped = thing
        return node



    def get_name(self):
        cdef cGraphQLAst.GraphQLAstName *next
        next = cGraphQLAst.GraphQLAstNamedType_get_name(self._wrapped)
        if next is NULL:
           return None
        return GraphQLAstName.create(next)





cdef class GraphQLAstListType(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstListType *thing):
        node = GraphQLAstListType()
        node._wrapped = thing
        return node








cdef class GraphQLAstNonNullType(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstNonNullType *thing):
        node = GraphQLAstNonNullType()
        node._wrapped = thing
        return node








cdef class GraphQLAstName(GraphQLAst):

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstName *thing):
        node = GraphQLAstName()
        node._wrapped = thing
        return node



    def get_value(self):
        val = cGraphQLAst.GraphQLAstName_get_value(self._wrapped)
        if val is None:
            return None
        return (val)



