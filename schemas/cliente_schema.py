from marshmallow import Schema, fields

class ClienteSchema(Schema):
    nome = fields.Str(  
        required=True,  
        metadata={
            'description':'Nome completo do cliente.'
        }
    )
    cpf = fields.Str(
        required=True, 
        metadata= {
            'description':'CPF do cliente (formato: XXX.XXX.XXX-XX).'
        }
    )
    telefone = fields.Str(
        required=True, 
        metadata={
            'description':'Telefone de contato.'
        }
    )
    email = fields.Email(
        required=True, 
        metadata={
            'description':'Email do cliente.'
        }
    )

class ClienteResponseSchema(ClienteSchema):
    id = fields.Int(
        dump_only=True, 
        metadata={
            'description':'ID único do cliente.'
        }
    )