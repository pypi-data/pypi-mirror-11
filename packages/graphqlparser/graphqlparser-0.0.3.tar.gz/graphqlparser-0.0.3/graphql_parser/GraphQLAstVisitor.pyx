#/**
#* Copyright (c) 2015, Facebook, Inc.
#* All rights reserved.
#*
#* This source code is licensed under the BSD-style license found in the
#* LICENSE file in the root directory of this source tree. An additional grant
#* of patent rights can be found in the PATENTS file in the same directory.
#*/
## @generated

from libc.string cimport memset
cimport cGraphQLAstVisitor
cimport GraphQLAstNode
cimport cGraphQLAstNode
cimport cGraphQLAst
cimport GraphQLAst

cdef class GraphQLAstVisitor:

    def visit_node(self, node):
      cdef cGraphQLAstVisitor.GraphQLAstVisitorCallbacks callbacks_c
      memset(&callbacks_c, 0, sizeof(callbacks_c))
      set_callbacks(&callbacks_c)
      cdef void* userData = <void *>self
      cdef cGraphQLAstNode.GraphQLAstNode *node_c;
      node_c = (<GraphQLAstNode.GraphQLAstNode?>node)._node
      cGraphQLAstVisitor.graphql_node_visit(node_c, &callbacks_c, userData)




cdef int _visit_document(cGraphQLAstVisitor.GraphQLAstDocument* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstDocument.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_document' if end else 'visit_document'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_document(cGraphQLAstVisitor.GraphQLAstDocument* node, void* userData):
    return _visit_document(node, userData, 0)

cdef void end_visit_document(cGraphQLAstVisitor.GraphQLAstDocument* node, void* userData):
    _visit_document(node, userData, 1)



cdef int _visit_operation_definition(cGraphQLAstVisitor.GraphQLAstOperationDefinition* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstOperationDefinition.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_operation_definition' if end else 'visit_operation_definition'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_operation_definition(cGraphQLAstVisitor.GraphQLAstOperationDefinition* node, void* userData):
    return _visit_operation_definition(node, userData, 0)

cdef void end_visit_operation_definition(cGraphQLAstVisitor.GraphQLAstOperationDefinition* node, void* userData):
    _visit_operation_definition(node, userData, 1)



cdef int _visit_variable_definition(cGraphQLAstVisitor.GraphQLAstVariableDefinition* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstVariableDefinition.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_variable_definition' if end else 'visit_variable_definition'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_variable_definition(cGraphQLAstVisitor.GraphQLAstVariableDefinition* node, void* userData):
    return _visit_variable_definition(node, userData, 0)

cdef void end_visit_variable_definition(cGraphQLAstVisitor.GraphQLAstVariableDefinition* node, void* userData):
    _visit_variable_definition(node, userData, 1)



cdef int _visit_selection_set(cGraphQLAstVisitor.GraphQLAstSelectionSet* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstSelectionSet.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_selection_set' if end else 'visit_selection_set'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_selection_set(cGraphQLAstVisitor.GraphQLAstSelectionSet* node, void* userData):
    return _visit_selection_set(node, userData, 0)

cdef void end_visit_selection_set(cGraphQLAstVisitor.GraphQLAstSelectionSet* node, void* userData):
    _visit_selection_set(node, userData, 1)



cdef int _visit_field(cGraphQLAstVisitor.GraphQLAstField* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstField.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_field' if end else 'visit_field'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_field(cGraphQLAstVisitor.GraphQLAstField* node, void* userData):
    return _visit_field(node, userData, 0)

cdef void end_visit_field(cGraphQLAstVisitor.GraphQLAstField* node, void* userData):
    _visit_field(node, userData, 1)



cdef int _visit_argument(cGraphQLAstVisitor.GraphQLAstArgument* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstArgument.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_argument' if end else 'visit_argument'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_argument(cGraphQLAstVisitor.GraphQLAstArgument* node, void* userData):
    return _visit_argument(node, userData, 0)

cdef void end_visit_argument(cGraphQLAstVisitor.GraphQLAstArgument* node, void* userData):
    _visit_argument(node, userData, 1)



cdef int _visit_fragment_spread(cGraphQLAstVisitor.GraphQLAstFragmentSpread* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstFragmentSpread.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_fragment_spread' if end else 'visit_fragment_spread'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_fragment_spread(cGraphQLAstVisitor.GraphQLAstFragmentSpread* node, void* userData):
    return _visit_fragment_spread(node, userData, 0)

cdef void end_visit_fragment_spread(cGraphQLAstVisitor.GraphQLAstFragmentSpread* node, void* userData):
    _visit_fragment_spread(node, userData, 1)



cdef int _visit_inline_fragment(cGraphQLAstVisitor.GraphQLAstInlineFragment* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstInlineFragment.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_inline_fragment' if end else 'visit_inline_fragment'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_inline_fragment(cGraphQLAstVisitor.GraphQLAstInlineFragment* node, void* userData):
    return _visit_inline_fragment(node, userData, 0)

cdef void end_visit_inline_fragment(cGraphQLAstVisitor.GraphQLAstInlineFragment* node, void* userData):
    _visit_inline_fragment(node, userData, 1)



cdef int _visit_fragment_definition(cGraphQLAstVisitor.GraphQLAstFragmentDefinition* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstFragmentDefinition.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_fragment_definition' if end else 'visit_fragment_definition'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_fragment_definition(cGraphQLAstVisitor.GraphQLAstFragmentDefinition* node, void* userData):
    return _visit_fragment_definition(node, userData, 0)

cdef void end_visit_fragment_definition(cGraphQLAstVisitor.GraphQLAstFragmentDefinition* node, void* userData):
    _visit_fragment_definition(node, userData, 1)



cdef int _visit_variable(cGraphQLAstVisitor.GraphQLAstVariable* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstVariable.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_variable' if end else 'visit_variable'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_variable(cGraphQLAstVisitor.GraphQLAstVariable* node, void* userData):
    return _visit_variable(node, userData, 0)

cdef void end_visit_variable(cGraphQLAstVisitor.GraphQLAstVariable* node, void* userData):
    _visit_variable(node, userData, 1)



cdef int _visit_int_value(cGraphQLAstVisitor.GraphQLAstIntValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstIntValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_int_value' if end else 'visit_int_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_int_value(cGraphQLAstVisitor.GraphQLAstIntValue* node, void* userData):
    return _visit_int_value(node, userData, 0)

cdef void end_visit_int_value(cGraphQLAstVisitor.GraphQLAstIntValue* node, void* userData):
    _visit_int_value(node, userData, 1)



cdef int _visit_float_value(cGraphQLAstVisitor.GraphQLAstFloatValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstFloatValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_float_value' if end else 'visit_float_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_float_value(cGraphQLAstVisitor.GraphQLAstFloatValue* node, void* userData):
    return _visit_float_value(node, userData, 0)

cdef void end_visit_float_value(cGraphQLAstVisitor.GraphQLAstFloatValue* node, void* userData):
    _visit_float_value(node, userData, 1)



cdef int _visit_string_value(cGraphQLAstVisitor.GraphQLAstStringValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstStringValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_string_value' if end else 'visit_string_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_string_value(cGraphQLAstVisitor.GraphQLAstStringValue* node, void* userData):
    return _visit_string_value(node, userData, 0)

cdef void end_visit_string_value(cGraphQLAstVisitor.GraphQLAstStringValue* node, void* userData):
    _visit_string_value(node, userData, 1)



cdef int _visit_boolean_value(cGraphQLAstVisitor.GraphQLAstBooleanValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstBooleanValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_boolean_value' if end else 'visit_boolean_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_boolean_value(cGraphQLAstVisitor.GraphQLAstBooleanValue* node, void* userData):
    return _visit_boolean_value(node, userData, 0)

cdef void end_visit_boolean_value(cGraphQLAstVisitor.GraphQLAstBooleanValue* node, void* userData):
    _visit_boolean_value(node, userData, 1)



cdef int _visit_enum_value(cGraphQLAstVisitor.GraphQLAstEnumValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstEnumValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_enum_value' if end else 'visit_enum_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_enum_value(cGraphQLAstVisitor.GraphQLAstEnumValue* node, void* userData):
    return _visit_enum_value(node, userData, 0)

cdef void end_visit_enum_value(cGraphQLAstVisitor.GraphQLAstEnumValue* node, void* userData):
    _visit_enum_value(node, userData, 1)



cdef int _visit_array_value(cGraphQLAstVisitor.GraphQLAstArrayValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstArrayValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_array_value' if end else 'visit_array_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_array_value(cGraphQLAstVisitor.GraphQLAstArrayValue* node, void* userData):
    return _visit_array_value(node, userData, 0)

cdef void end_visit_array_value(cGraphQLAstVisitor.GraphQLAstArrayValue* node, void* userData):
    _visit_array_value(node, userData, 1)



cdef int _visit_object_value(cGraphQLAstVisitor.GraphQLAstObjectValue* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstObjectValue.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_object_value' if end else 'visit_object_value'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_object_value(cGraphQLAstVisitor.GraphQLAstObjectValue* node, void* userData):
    return _visit_object_value(node, userData, 0)

cdef void end_visit_object_value(cGraphQLAstVisitor.GraphQLAstObjectValue* node, void* userData):
    _visit_object_value(node, userData, 1)



cdef int _visit_object_field(cGraphQLAstVisitor.GraphQLAstObjectField* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstObjectField.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_object_field' if end else 'visit_object_field'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_object_field(cGraphQLAstVisitor.GraphQLAstObjectField* node, void* userData):
    return _visit_object_field(node, userData, 0)

cdef void end_visit_object_field(cGraphQLAstVisitor.GraphQLAstObjectField* node, void* userData):
    _visit_object_field(node, userData, 1)



cdef int _visit_directive(cGraphQLAstVisitor.GraphQLAstDirective* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstDirective.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_directive' if end else 'visit_directive'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_directive(cGraphQLAstVisitor.GraphQLAstDirective* node, void* userData):
    return _visit_directive(node, userData, 0)

cdef void end_visit_directive(cGraphQLAstVisitor.GraphQLAstDirective* node, void* userData):
    _visit_directive(node, userData, 1)



cdef int _visit_named_type(cGraphQLAstVisitor.GraphQLAstNamedType* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstNamedType.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_named_type' if end else 'visit_named_type'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_named_type(cGraphQLAstVisitor.GraphQLAstNamedType* node, void* userData):
    return _visit_named_type(node, userData, 0)

cdef void end_visit_named_type(cGraphQLAstVisitor.GraphQLAstNamedType* node, void* userData):
    _visit_named_type(node, userData, 1)



cdef int _visit_list_type(cGraphQLAstVisitor.GraphQLAstListType* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstListType.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_list_type' if end else 'visit_list_type'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_list_type(cGraphQLAstVisitor.GraphQLAstListType* node, void* userData):
    return _visit_list_type(node, userData, 0)

cdef void end_visit_list_type(cGraphQLAstVisitor.GraphQLAstListType* node, void* userData):
    _visit_list_type(node, userData, 1)



cdef int _visit_non_null_type(cGraphQLAstVisitor.GraphQLAstNonNullType* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstNonNullType.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_non_null_type' if end else 'visit_non_null_type'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_non_null_type(cGraphQLAstVisitor.GraphQLAstNonNullType* node, void* userData):
    return _visit_non_null_type(node, userData, 0)

cdef void end_visit_non_null_type(cGraphQLAstVisitor.GraphQLAstNonNullType* node, void* userData):
    _visit_non_null_type(node, userData, 1)



cdef int _visit_name(cGraphQLAstVisitor.GraphQLAstName* node, void* userData, int end):
    cdef GraphQLAstVisitor visitor
    ast = GraphQLAst.GraphQLAstName.create(node)
    if userData is not NULL:
      visitor = <GraphQLAstVisitor>userData
      attname = 'end_visit_name' if end else 'visit_name'
      fun = getattr(visitor, attname, None)
      if fun is not None:
        retval = fun(ast)
        return 0 if retval is None else retval

cdef int visit_name(cGraphQLAstVisitor.GraphQLAstName* node, void* userData):
    return _visit_name(node, userData, 0)

cdef void end_visit_name(cGraphQLAstVisitor.GraphQLAstName* node, void* userData):
    _visit_name(node, userData, 1)



cdef set_callbacks(cGraphQLAstVisitor.GraphQLAstVisitorCallbacks *callbacks):


    callbacks.visit_document = &visit_document
    callbacks.end_visit_document = &end_visit_document


    callbacks.visit_operation_definition = &visit_operation_definition
    callbacks.end_visit_operation_definition = &end_visit_operation_definition


    callbacks.visit_variable_definition = &visit_variable_definition
    callbacks.end_visit_variable_definition = &end_visit_variable_definition


    callbacks.visit_selection_set = &visit_selection_set
    callbacks.end_visit_selection_set = &end_visit_selection_set


    callbacks.visit_field = &visit_field
    callbacks.end_visit_field = &end_visit_field


    callbacks.visit_argument = &visit_argument
    callbacks.end_visit_argument = &end_visit_argument


    callbacks.visit_fragment_spread = &visit_fragment_spread
    callbacks.end_visit_fragment_spread = &end_visit_fragment_spread


    callbacks.visit_inline_fragment = &visit_inline_fragment
    callbacks.end_visit_inline_fragment = &end_visit_inline_fragment


    callbacks.visit_fragment_definition = &visit_fragment_definition
    callbacks.end_visit_fragment_definition = &end_visit_fragment_definition


    callbacks.visit_variable = &visit_variable
    callbacks.end_visit_variable = &end_visit_variable


    callbacks.visit_int_value = &visit_int_value
    callbacks.end_visit_int_value = &end_visit_int_value


    callbacks.visit_float_value = &visit_float_value
    callbacks.end_visit_float_value = &end_visit_float_value


    callbacks.visit_string_value = &visit_string_value
    callbacks.end_visit_string_value = &end_visit_string_value


    callbacks.visit_boolean_value = &visit_boolean_value
    callbacks.end_visit_boolean_value = &end_visit_boolean_value


    callbacks.visit_enum_value = &visit_enum_value
    callbacks.end_visit_enum_value = &end_visit_enum_value


    callbacks.visit_array_value = &visit_array_value
    callbacks.end_visit_array_value = &end_visit_array_value


    callbacks.visit_object_value = &visit_object_value
    callbacks.end_visit_object_value = &end_visit_object_value


    callbacks.visit_object_field = &visit_object_field
    callbacks.end_visit_object_field = &end_visit_object_field


    callbacks.visit_directive = &visit_directive
    callbacks.end_visit_directive = &end_visit_directive


    callbacks.visit_named_type = &visit_named_type
    callbacks.end_visit_named_type = &end_visit_named_type


    callbacks.visit_list_type = &visit_list_type
    callbacks.end_visit_list_type = &end_visit_list_type


    callbacks.visit_non_null_type = &visit_non_null_type
    callbacks.end_visit_non_null_type = &end_visit_non_null_type


    callbacks.visit_name = &visit_name
    callbacks.end_visit_name = &end_visit_name

