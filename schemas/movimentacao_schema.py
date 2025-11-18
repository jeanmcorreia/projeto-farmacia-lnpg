from marshmallow import Schema, fields, validate

class MovimentacaoSchema(Schema):
    id_medicamento = fields.Int(
        required=True, 
        metadata={
            'description':'ID do medicamento a ser movimentado.'
        }
    )
    tipo = fields.Str(
        required=True, 
        metadata={
            'description':'Tipo da movimentação (ex: "entrada").'
        }
    )
    quantidade = fields.Int(
        required=True, 
        validate=validate.Range(min=1, min_inclusive=False), 
        metadata={
            'description':'Quantidade movimentada (deve ser > 0).'
        }
    )
    id_funcionario = fields.Int(
        required=True, 
        metadata={
            'description':'ID do funcionário que registrou a movimentação.'
        }
    )

class MovimentacaoResponseSchema(MovimentacaoSchema):
    id = fields.Int(
        dump_only=True, 
        metadata={
            'description':'ID único da movimentação.'
        }
    )
    data = fields.DateTime(
        dump_only=True, 
        metadata={
            'description':'Data e hora em que a movimentação foi registrada.'
        }
    )