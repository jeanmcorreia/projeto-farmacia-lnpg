from marshmallow import Schema, fields

class MovimentacaoSchema(Schema):
    id_medicamento = fields.Int(required=True, description="ID do medicamento a ser movimentado.")
    tipo = fields.Str(required=True, description="Tipo da movimentação (ex: 'entrada').")
    quantidade = fields.Int(required=True, gt=0, description="Quantidade movimentada (deve ser > 0).")
    id_funcionario = fields.Int(required=True, description="ID do funcionário que registrou a movimentação.")

class MovimentacaoResponseSchema(MovimentacaoSchema):
    id = fields.Int(dump_only=True, description="ID único da movimentação.")
    data = fields.DateTime(dump_only=True, description="Data e hora em que a movimentação foi registrada.")