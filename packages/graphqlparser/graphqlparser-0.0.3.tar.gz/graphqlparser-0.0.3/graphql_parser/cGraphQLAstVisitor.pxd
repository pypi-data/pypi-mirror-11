#/**
#* Copyright (c) 2015, Facebook, Inc.
#* All rights reserved.
#*
#* This source code is licensed under the BSD-style license found in the
#* LICENSE file in the root directory of this source tree. An additional grant
#* of patent rights can be found in the PATENTS file in the same directory.
#*/
## @generated

cdef extern from "GraphQLAstVisitor.h":

    struct GraphQLAstNode:
        pass



    struct GraphQLAstDocument:
        pass
    ctypedef int (*visit_document_func)(GraphQLAstDocument*, void*)
    ctypedef void (*end_visit_document_func)(GraphQLAstDocument*, void*)
    struct GraphQLAstOperationDefinition:
        pass
    ctypedef int (*visit_operation_definition_func)(GraphQLAstOperationDefinition*, void*)
    ctypedef void (*end_visit_operation_definition_func)(GraphQLAstOperationDefinition*, void*)
    struct GraphQLAstVariableDefinition:
        pass
    ctypedef int (*visit_variable_definition_func)(GraphQLAstVariableDefinition*, void*)
    ctypedef void (*end_visit_variable_definition_func)(GraphQLAstVariableDefinition*, void*)
    struct GraphQLAstSelectionSet:
        pass
    ctypedef int (*visit_selection_set_func)(GraphQLAstSelectionSet*, void*)
    ctypedef void (*end_visit_selection_set_func)(GraphQLAstSelectionSet*, void*)
    struct GraphQLAstField:
        pass
    ctypedef int (*visit_field_func)(GraphQLAstField*, void*)
    ctypedef void (*end_visit_field_func)(GraphQLAstField*, void*)
    struct GraphQLAstArgument:
        pass
    ctypedef int (*visit_argument_func)(GraphQLAstArgument*, void*)
    ctypedef void (*end_visit_argument_func)(GraphQLAstArgument*, void*)
    struct GraphQLAstFragmentSpread:
        pass
    ctypedef int (*visit_fragment_spread_func)(GraphQLAstFragmentSpread*, void*)
    ctypedef void (*end_visit_fragment_spread_func)(GraphQLAstFragmentSpread*, void*)
    struct GraphQLAstInlineFragment:
        pass
    ctypedef int (*visit_inline_fragment_func)(GraphQLAstInlineFragment*, void*)
    ctypedef void (*end_visit_inline_fragment_func)(GraphQLAstInlineFragment*, void*)
    struct GraphQLAstFragmentDefinition:
        pass
    ctypedef int (*visit_fragment_definition_func)(GraphQLAstFragmentDefinition*, void*)
    ctypedef void (*end_visit_fragment_definition_func)(GraphQLAstFragmentDefinition*, void*)
    struct GraphQLAstVariable:
        pass
    ctypedef int (*visit_variable_func)(GraphQLAstVariable*, void*)
    ctypedef void (*end_visit_variable_func)(GraphQLAstVariable*, void*)
    struct GraphQLAstIntValue:
        pass
    ctypedef int (*visit_int_value_func)(GraphQLAstIntValue*, void*)
    ctypedef void (*end_visit_int_value_func)(GraphQLAstIntValue*, void*)
    struct GraphQLAstFloatValue:
        pass
    ctypedef int (*visit_float_value_func)(GraphQLAstFloatValue*, void*)
    ctypedef void (*end_visit_float_value_func)(GraphQLAstFloatValue*, void*)
    struct GraphQLAstStringValue:
        pass
    ctypedef int (*visit_string_value_func)(GraphQLAstStringValue*, void*)
    ctypedef void (*end_visit_string_value_func)(GraphQLAstStringValue*, void*)
    struct GraphQLAstBooleanValue:
        pass
    ctypedef int (*visit_boolean_value_func)(GraphQLAstBooleanValue*, void*)
    ctypedef void (*end_visit_boolean_value_func)(GraphQLAstBooleanValue*, void*)
    struct GraphQLAstEnumValue:
        pass
    ctypedef int (*visit_enum_value_func)(GraphQLAstEnumValue*, void*)
    ctypedef void (*end_visit_enum_value_func)(GraphQLAstEnumValue*, void*)
    struct GraphQLAstArrayValue:
        pass
    ctypedef int (*visit_array_value_func)(GraphQLAstArrayValue*, void*)
    ctypedef void (*end_visit_array_value_func)(GraphQLAstArrayValue*, void*)
    struct GraphQLAstObjectValue:
        pass
    ctypedef int (*visit_object_value_func)(GraphQLAstObjectValue*, void*)
    ctypedef void (*end_visit_object_value_func)(GraphQLAstObjectValue*, void*)
    struct GraphQLAstObjectField:
        pass
    ctypedef int (*visit_object_field_func)(GraphQLAstObjectField*, void*)
    ctypedef void (*end_visit_object_field_func)(GraphQLAstObjectField*, void*)
    struct GraphQLAstDirective:
        pass
    ctypedef int (*visit_directive_func)(GraphQLAstDirective*, void*)
    ctypedef void (*end_visit_directive_func)(GraphQLAstDirective*, void*)
    struct GraphQLAstNamedType:
        pass
    ctypedef int (*visit_named_type_func)(GraphQLAstNamedType*, void*)
    ctypedef void (*end_visit_named_type_func)(GraphQLAstNamedType*, void*)
    struct GraphQLAstListType:
        pass
    ctypedef int (*visit_list_type_func)(GraphQLAstListType*, void*)
    ctypedef void (*end_visit_list_type_func)(GraphQLAstListType*, void*)
    struct GraphQLAstNonNullType:
        pass
    ctypedef int (*visit_non_null_type_func)(GraphQLAstNonNullType*, void*)
    ctypedef void (*end_visit_non_null_type_func)(GraphQLAstNonNullType*, void*)
    struct GraphQLAstName:
        pass
    ctypedef int (*visit_name_func)(GraphQLAstName*, void*)
    ctypedef void (*end_visit_name_func)(GraphQLAstName*, void*)
    struct GraphQLAstVisitorCallbacks:
        visit_document_func visit_document
        end_visit_document_func end_visit_document
        visit_operation_definition_func visit_operation_definition
        end_visit_operation_definition_func end_visit_operation_definition
        visit_variable_definition_func visit_variable_definition
        end_visit_variable_definition_func end_visit_variable_definition
        visit_selection_set_func visit_selection_set
        end_visit_selection_set_func end_visit_selection_set
        visit_field_func visit_field
        end_visit_field_func end_visit_field
        visit_argument_func visit_argument
        end_visit_argument_func end_visit_argument
        visit_fragment_spread_func visit_fragment_spread
        end_visit_fragment_spread_func end_visit_fragment_spread
        visit_inline_fragment_func visit_inline_fragment
        end_visit_inline_fragment_func end_visit_inline_fragment
        visit_fragment_definition_func visit_fragment_definition
        end_visit_fragment_definition_func end_visit_fragment_definition
        visit_variable_func visit_variable
        end_visit_variable_func end_visit_variable
        visit_int_value_func visit_int_value
        end_visit_int_value_func end_visit_int_value
        visit_float_value_func visit_float_value
        end_visit_float_value_func end_visit_float_value
        visit_string_value_func visit_string_value
        end_visit_string_value_func end_visit_string_value
        visit_boolean_value_func visit_boolean_value
        end_visit_boolean_value_func end_visit_boolean_value
        visit_enum_value_func visit_enum_value
        end_visit_enum_value_func end_visit_enum_value
        visit_array_value_func visit_array_value
        end_visit_array_value_func end_visit_array_value
        visit_object_value_func visit_object_value
        end_visit_object_value_func end_visit_object_value
        visit_object_field_func visit_object_field
        end_visit_object_field_func end_visit_object_field
        visit_directive_func visit_directive
        end_visit_directive_func end_visit_directive
        visit_named_type_func visit_named_type
        end_visit_named_type_func end_visit_named_type
        visit_list_type_func visit_list_type
        end_visit_list_type_func end_visit_list_type
        visit_non_null_type_func visit_non_null_type
        end_visit_non_null_type_func end_visit_non_null_type
        visit_name_func visit_name
        end_visit_name_func end_visit_name

    void graphql_node_visit(GraphQLAstNode *node,
                            GraphQLAstVisitorCallbacks *callbacks,
                            void *userData)

