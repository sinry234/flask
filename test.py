﻿from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Thing(Base):
    __tablename__ = 'thing'
    id = Column(Integer, primary_key=True)
    Rate = Column(Integer)
    Code = Column(String)
    Name = Column(String)

rules = {
    "groupOp": "AND",
    "rules":[
        {
            "field":"Rate",
            "op":"eq",
            "data":"6"
        }
    ],
    "groups":[
        {"groupOp":"OR",
        "rules":[
            {"field":"Code", "op":"eq", "data":"abc"},
            {"field":"Name","op":"eq","data":"fd"}
        ],
        "groups":[]
    }
]}


from sqlalchemy import and_, or_
from operator import eq
lookup = {
    "AND": and_,
    "OR": or_,
    "eq": eq
}

def visit_rule(rules):
    fn = lookup[rules['groupOp']]
    return fn(
                *(
                    [visit_expr(expr) for expr in rules['rules']] +
                    [visit_rule(subrule) for subrule in rules['groups']]
                )
            )

def visit_expr(expr):
    return lookup[expr["op"]](
                getattr(Thing, expr["field"]),
                expr["data"]
            )

print (visit_rule(rules))