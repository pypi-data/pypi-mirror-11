#/**
#* Copyright (c) 2015, Facebook, Inc.
#* All rights reserved.
#*
#* This source code is licensed under the BSD-style license found in the
#* LICENSE file in the root directory of this source tree. An additional grant
#* of patent rights can be found in the PATENTS file in the same directory.
#*/
## @generated

cdef extern from "GraphQLAst.h":


    struct GraphQLAstDefinition:
        pass

    struct GraphQLAstDocument:
        pass
    int GraphQLAstDocument_get_definitions_size(const GraphQLAstDocument *node)


    struct GraphQLAstOperationDefinition:
        pass
    const char * GraphQLAstOperationDefinition_get_operation(const GraphQLAstOperationDefinition *node)
    const GraphQLAstName * GraphQLAstOperationDefinition_get_name(const GraphQLAstOperationDefinition *node)
    int GraphQLAstOperationDefinition_get_variable_definitions_size(const GraphQLAstOperationDefinition *node)
    int GraphQLAstOperationDefinition_get_directives_size(const GraphQLAstOperationDefinition *node)
    const GraphQLAstSelectionSet * GraphQLAstOperationDefinition_get_selection_set(const GraphQLAstOperationDefinition *node)


    struct GraphQLAstVariableDefinition:
        pass
    const GraphQLAstVariable * GraphQLAstVariableDefinition_get_variable(const GraphQLAstVariableDefinition *node)
    const GraphQLAstType * GraphQLAstVariableDefinition_get_type(const GraphQLAstVariableDefinition *node)
    const GraphQLAstValue * GraphQLAstVariableDefinition_get_default_value(const GraphQLAstVariableDefinition *node)


    struct GraphQLAstSelectionSet:
        pass
    int GraphQLAstSelectionSet_get_selections_size(const GraphQLAstSelectionSet *node)


    struct GraphQLAstSelection:
        pass

    struct GraphQLAstField:
        pass
    const GraphQLAstName * GraphQLAstField_get_alias(const GraphQLAstField *node)
    const GraphQLAstName * GraphQLAstField_get_name(const GraphQLAstField *node)
    int GraphQLAstField_get_arguments_size(const GraphQLAstField *node)
    int GraphQLAstField_get_directives_size(const GraphQLAstField *node)
    const GraphQLAstSelectionSet * GraphQLAstField_get_selection_set(const GraphQLAstField *node)


    struct GraphQLAstArgument:
        pass
    const GraphQLAstName * GraphQLAstArgument_get_name(const GraphQLAstArgument *node)
    const GraphQLAstValue * GraphQLAstArgument_get_value(const GraphQLAstArgument *node)


    struct GraphQLAstFragmentSpread:
        pass
    const GraphQLAstName * GraphQLAstFragmentSpread_get_name(const GraphQLAstFragmentSpread *node)
    int GraphQLAstFragmentSpread_get_directives_size(const GraphQLAstFragmentSpread *node)


    struct GraphQLAstInlineFragment:
        pass
    const GraphQLAstNamedType * GraphQLAstInlineFragment_get_type_condition(const GraphQLAstInlineFragment *node)
    int GraphQLAstInlineFragment_get_directives_size(const GraphQLAstInlineFragment *node)
    const GraphQLAstSelectionSet * GraphQLAstInlineFragment_get_selection_set(const GraphQLAstInlineFragment *node)


    struct GraphQLAstFragmentDefinition:
        pass
    const GraphQLAstName * GraphQLAstFragmentDefinition_get_name(const GraphQLAstFragmentDefinition *node)
    const GraphQLAstNamedType * GraphQLAstFragmentDefinition_get_type_condition(const GraphQLAstFragmentDefinition *node)
    int GraphQLAstFragmentDefinition_get_directives_size(const GraphQLAstFragmentDefinition *node)
    const GraphQLAstSelectionSet * GraphQLAstFragmentDefinition_get_selection_set(const GraphQLAstFragmentDefinition *node)


    struct GraphQLAstValue:
        pass

    struct GraphQLAstVariable:
        pass
    const GraphQLAstName * GraphQLAstVariable_get_name(const GraphQLAstVariable *node)


    struct GraphQLAstIntValue:
        pass
    const char * GraphQLAstIntValue_get_value(const GraphQLAstIntValue *node)


    struct GraphQLAstFloatValue:
        pass
    const char * GraphQLAstFloatValue_get_value(const GraphQLAstFloatValue *node)


    struct GraphQLAstStringValue:
        pass
    const char * GraphQLAstStringValue_get_value(const GraphQLAstStringValue *node)


    struct GraphQLAstBooleanValue:
        pass
    int GraphQLAstBooleanValue_get_value(const GraphQLAstBooleanValue *node)


    struct GraphQLAstEnumValue:
        pass
    const char * GraphQLAstEnumValue_get_value(const GraphQLAstEnumValue *node)


    struct GraphQLAstArrayValue:
        pass
    int GraphQLAstArrayValue_get_values_size(const GraphQLAstArrayValue *node)


    struct GraphQLAstObjectValue:
        pass
    int GraphQLAstObjectValue_get_fields_size(const GraphQLAstObjectValue *node)


    struct GraphQLAstObjectField:
        pass
    const GraphQLAstName * GraphQLAstObjectField_get_name(const GraphQLAstObjectField *node)
    const GraphQLAstValue * GraphQLAstObjectField_get_value(const GraphQLAstObjectField *node)


    struct GraphQLAstDirective:
        pass
    const GraphQLAstName * GraphQLAstDirective_get_name(const GraphQLAstDirective *node)
    int GraphQLAstDirective_get_arguments_size(const GraphQLAstDirective *node)


    struct GraphQLAstType:
        pass

    struct GraphQLAstNamedType:
        pass
    const GraphQLAstName * GraphQLAstNamedType_get_name(const GraphQLAstNamedType *node)


    struct GraphQLAstListType:
        pass
    const GraphQLAstType * GraphQLAstListType_get_type(const GraphQLAstListType *node)


    struct GraphQLAstNonNullType:
        pass
    const GraphQLAstType * GraphQLAstNonNullType_get_type(const GraphQLAstNonNullType *node)


    struct GraphQLAstName:
        pass
    const char * GraphQLAstName_get_value(const GraphQLAstName *node)


