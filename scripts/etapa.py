import shutil
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
APP = RAIZ / "app"
ETAPAS = RAIZ / "etapas"
BACKUP = APP / ".backup"
ULTIMA_ETAPA = 4

USO = """Uso:
  python scripts/etapa.py preparar N   deixa o app no ponto de partida da etapa N
                                       (aplica as soluções das etapas 0 a N-1)
  python scripts/etapa.py solucao N    aplica a solução da etapa N
                                       (e das anteriores, se necessário)
N vai de 0 a 4."""


def aplicar_solucao(n: int, carimbo: str) -> list[str]:
    origem = ETAPAS / f"etapa-{n}" / "solucao"
    if not origem.is_dir():
        raise SystemExit(f"Não encontrei a solução da etapa {n} em {origem}.")
    copiados = []
    for arquivo in sorted(p for p in origem.rglob("*") if p.is_file()):
        relativo = arquivo.relative_to(origem)
        destino = APP / relativo
        if destino.exists() and destino.read_bytes() != arquivo.read_bytes():
            salvo = BACKUP / carimbo / relativo
            salvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destino, salvo)
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arquivo, destino)
        copiados.append(str(Path("app") / relativo))
    return copiados


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in {"preparar", "solucao"} or not argv[2].isdigit():
        print(USO)
        return 1
    comando, n = argv[1], int(argv[2])
    if n > ULTIMA_ETAPA:
        print(USO)
        return 1
    ate = n - 1 if comando == "preparar" else n
    carimbo = time.strftime("%Y%m%d-%H%M%S")
    copiados = []
    for etapa in range(ate + 1):
        copiados += aplicar_solucao(etapa, carimbo)
    if not copiados:
        print("Nada a aplicar: a etapa 0 parte do estado inicial do repositório.")
        return 0
    print(f"Arquivos atualizados ({comando} {n}):")
    for caminho in copiados:
        print(f"  {caminho}")
    if (BACKUP / carimbo).exists():
        print(f"Seu código anterior foi guardado em app/.backup/{carimbo}/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
