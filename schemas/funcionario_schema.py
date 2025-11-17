from marshmallow import Schema, fields

class FuncionarioSchema(Schema):
    nome = fields.Str(required=True, description="Nome completo do funcionário.")
    cpf = fields.Str(required=True, description="CPF do funcionário (formato: XXX.XXX.XXX-XX).")
    cargo = fields.Str(required=True, description="Cargo do funcionário.")
    email = fields.Email(required=True, description="Email do funcionário.")

class FuncionarioResponseSchema(FuncionarioSchema):
    id = fields.Int(dump_only=True, description="ID único do funcionário.")