import ast

from peval.tools import ast_transformer, replace_fields
from peval.core.scope import analyze_scope


def decompose_destructuring_assignments(node, constants):
    node = _decompose_destructuring_assignments(node)
    return node, constants


def _decompose_destructuring_assignments(node):
    remaining_nodes = list(node.body)
    new_nodes = []

    while len(remaining_nodes) > 0:
        cur_node = remaining_nodes.pop(0)
        if type(cur_node) == ast.Assign:
            if isinstance(target, (ast.List, ast.Tuple)):
                for i, el in enumerate(target.elts):
                    decomposedAssignment = ast.Assign(targets=[el], value=ast.Subscript(value=statement, slice=ast.Constant(value=i), ctx=Load()))
            remaining_nodes = replace_name(remaining_nodes, ctx=dict(dest_name=dest_name, src_name=src_name))
        else:
            new_nodes.append(cur_node)

    if len(new_nodes) == len(node.body):
        return node

    return replace_fields(node, body=new_nodes)


@ast_transformer
class replace_name:
    @staticmethod
    def handle_Name(node, ctx, **_):
        if type(node.ctx) == ast.Load and node.id == ctx.dest_name:
            return replace_fields(node, id=ctx.src_name)
        else:
            return node
