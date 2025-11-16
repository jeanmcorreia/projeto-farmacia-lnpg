from marshmallow import Schema, fields

class MedicamentoSchema(Schema):
    nome = fields.Str(required=True, description="Nome comercial do medicamento.")
    fabricante = fields.Str(required=True, description="Laboratório fabricante.")
    preco_unitario = fields.Float(required=True, description="Preço unitário do medicamento.")
    quantidade_estoque = fields.Int(required=True, description="Quantidade em estoque.")
    validade = fields.Date(required=True, description="Data de validade (formato: AAAA-MM-DD).")

class MedicamentoResponseSchema(MedicamentoSchema):
    id = fields.Int(dump_only=True, description="ID único do medicamento.")