from marshmallow import Schema, fields

class ItemVendaSchema(Schema):
    id_medicamento = fields.Int(required=True, description="ID do medicamento a ser vendido.")
    quantidade = fields.Int(required=True, ge=1, description="Quantidade a ser vendida (mínimo 1).")

class VendaSchema(Schema):
    id_cliente = fields.Int(required=True, description="ID do cliente que está comprando.")
    id_funcionario = fields.Int(required=True, description="ID do funcionário que realizou a venda.")
    itens = fields.List(
        fields.Nested(ItemVendaSchema()), 
        required=True,
        validate=lambda x: len(x) > 0,
        description="Lista de medicamentos e quantidades vendidas."
    )

class ItemVendaResponseSchema(ItemVendaSchema):
    id = fields.Int(dump_only=True)
    id_venda = fields.Int(dump_only=True)
    preco_unitario_momento = fields.Float(dump_only=True, description="Preço do item no momento da compra.")

class VendaResponseSchema(VendaSchema):
    id = fields.Int(dump_only=True, description="ID único da venda gerado.")
    valor_total = fields.Float(dump_only=True, description="Valor total calculado da venda.")
    data_venda = fields.DateTime(dump_only=True, description="Data/hora em que a venda foi registrada.")
    itens = fields.List(fields.Nested(ItemVendaResponseSchema()), dump_only=True)