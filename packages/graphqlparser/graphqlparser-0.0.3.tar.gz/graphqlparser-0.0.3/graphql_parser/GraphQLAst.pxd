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

    cdef cGraphQLAst.GraphQLAstDocument* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstDocument *thing)





cdef class GraphQLAstOperationDefinition(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstOperationDefinition* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstOperationDefinition *thing)





cdef class GraphQLAstVariableDefinition(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstVariableDefinition* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstVariableDefinition *thing)





cdef class GraphQLAstSelectionSet(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstSelectionSet* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstSelectionSet *thing)






cdef class GraphQLAstField(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstField* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstField *thing)





cdef class GraphQLAstArgument(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstArgument* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstArgument *thing)





cdef class GraphQLAstFragmentSpread(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstFragmentSpread* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFragmentSpread *thing)





cdef class GraphQLAstInlineFragment(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstInlineFragment* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstInlineFragment *thing)





cdef class GraphQLAstFragmentDefinition(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstFragmentDefinition* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFragmentDefinition *thing)






cdef class GraphQLAstVariable(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstVariable* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstVariable *thing)





cdef class GraphQLAstIntValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstIntValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstIntValue *thing)





cdef class GraphQLAstFloatValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstFloatValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstFloatValue *thing)





cdef class GraphQLAstStringValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstStringValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstStringValue *thing)





cdef class GraphQLAstBooleanValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstBooleanValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstBooleanValue *thing)





cdef class GraphQLAstEnumValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstEnumValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstEnumValue *thing)





cdef class GraphQLAstArrayValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstArrayValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstArrayValue *thing)





cdef class GraphQLAstObjectValue(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstObjectValue* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstObjectValue *thing)





cdef class GraphQLAstObjectField(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstObjectField* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstObjectField *thing)





cdef class GraphQLAstDirective(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstDirective* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstDirective *thing)






cdef class GraphQLAstNamedType(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstNamedType* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstNamedType *thing)





cdef class GraphQLAstListType(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstListType* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstListType *thing)





cdef class GraphQLAstNonNullType(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstNonNullType* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstNonNullType *thing)





cdef class GraphQLAstName(GraphQLAst):

    cdef cGraphQLAst.GraphQLAstName* _wrapped

    @staticmethod
    cdef create(cGraphQLAst.GraphQLAstName *thing)




