
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND LPARENT NOT OR RPARENT WORD\n        expression : expression OR term\n                   | expression AND term\n        \n        expression : term\n        \n        term : NOT factor\n        \n        term : factor\n        \n        factor : WORD\n        \n        factor : LPARENT expression RPARENT\n        '
    
_lr_action_items = {'NOT':([0,6,7,8,],[3,3,3,3,]),'WORD':([0,3,6,7,8,],[5,5,5,5,5,]),'LPARENT':([0,3,6,7,8,],[6,6,6,6,6,]),'$end':([1,2,4,5,9,11,12,13,],[0,-3,-5,-6,-4,-1,-2,-7,]),'OR':([1,2,4,5,9,10,11,12,13,],[7,-3,-5,-6,-4,7,-1,-2,-7,]),'AND':([1,2,4,5,9,10,11,12,13,],[8,-3,-5,-6,-4,8,-1,-2,-7,]),'RPARENT':([2,4,5,9,10,11,12,13,],[-3,-5,-6,-4,13,-1,-2,-7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,6,],[1,10,]),'term':([0,6,7,8,],[2,2,11,12,]),'factor':([0,3,6,7,8,],[4,9,4,4,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression OR term','expression',3,'p_expression_binop','check.py',27),
  ('expression -> expression AND term','expression',3,'p_expression_binop','check.py',28),
  ('expression -> term','expression',1,'p_expression_term','check.py',35),
  ('term -> NOT factor','term',2,'p_term_uop','check.py',42),
  ('term -> factor','term',1,'p_term','check.py',49),
  ('factor -> WORD','factor',1,'p_factor','check.py',56),
  ('factor -> LPARENT expression RPARENT','factor',3,'p_factor_group','check.py',63),
]
