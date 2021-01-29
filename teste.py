from aluno.models import Aluno
from avaliacao.views import CalcPontuacaoDia, CalcWonWeekRewards, CalcGeneralRankByQuantSubj, CalcGeneralRank, \
    CalcRankTurma
from turma.models import Turma

aluno = Aluno.objects.get(id=1)
turma = Turma.objects.get(id=2)
CalcGeneralRankByQuantSubj(aluno)
