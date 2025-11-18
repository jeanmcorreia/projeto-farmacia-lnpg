from marshmallow import Schema, fields

class MedicamentoSchema(Schema):
    nome = fields.Str(
        required=True, 
        metadata={
            'description':'Nome comercial do medicamento.'
        }
    )
    fabricante = fields.Str(
        required=True, 
        metadata={
            'description':'Laboratório fabricante.'
        }
    )
    preco_unitario = fields.Float(
        required=True, 
        metadata={
            'description':'Preço unitário do medicamento.'
        }
    )
    quantidade_estoque = fields.Int(
        required=True, 
        metadata={
            'description':'Quantidade em estoque.'
        }
    )
    validade = fields.Date(
        required=True, 
        metadata={
            'description':'Data de validade (formato: AAAA-MM-DD).'
        }
    )

class MedicamentoResponseSchema(MedicamentoSchema):
    id = fields.Int(
        dump_only=True, 
        metadata={
            'description':'ID único do medicamento.'
        }
    )