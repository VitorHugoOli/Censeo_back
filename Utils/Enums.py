from Utils.Pontos import PONTOS_AVALIACAO

tipo_aula = (
    ('teorica', 'teorica'),
    ('prova', 'prova'),
    ('trabalho', 'trabalho'),
    ('excursao', 'excursao')
)

tipo_dias = (
    ('SEG', 'SEG'),
    ('TER', 'TER'),
    ('QUA', 'QUA'),
    ('QUI', 'QUI'),
    ('SEX', 'SEX'),
    ('SAB', 'SAB'),
    ('DOM', 'DOM'),
)

tipo_questao_enum = (
    ('aberta', 'aberta'),
    ('qualificativa', 'qualificativa'),
    ('binario', 'binario'),
)

tipo_relevancia = (
    ('baixa', 'baixa'),
    ('media', 'media'),
    ('alta', 'alta')
)

relevancia_points = {
    'baixa': PONTOS_AVALIACAO * 0.2,
    'media': PONTOS_AVALIACAO * 0.5,
    'alta': PONTOS_AVALIACAO
}

tipo_qualificativo = (
    ('perfeita', 'perfeita'),
    ('boa', 'boa'),
    ('regular', 'regular'),
    ('ruim', 'ruim'),
    ('pessima', 'pessima')
)

tipo_resposta = (
    ('binario', 'binario'),
    ('qualificativa', 'qualificativa'),
    ('aberta', 'aberta')
)

tipo_strike = (
    ('fire', 'fire'),
    ('cold_fire', 'cold_fire'),
    ('snow', 'snow')
)
