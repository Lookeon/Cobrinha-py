
# Snake OOP
<p align="center">
  <img width="331" height="533" alt="image" src="https://github.com/user-attachments/assets/bd982edf-99c5-4af5-8b1f-7e695c8dd554" />
</p>
Jogo da cobrinha (Snake) feito em Python com Tkinter, usando Programação Orientada a Objetos. Projeto de estudo para praticar classes, lógica de jogo e interface gráfica.

## Funcionalidades

- Controle da cobra com as setas ou com as teclas **W, A, S, D**
- A cobra cresce e o jogador ganha 10 pontos a cada comida
- Fim de jogo ao bater na parede ou no próprio corpo
- Placar atualizado na tela
- Botão **Jogar novamente** para reiniciar a partida

## Estrutura do código

- `Snake`: movimento, crescimento, direção e colisões da cobra
- `Food`: posição aleatória da comida, sem aparecer em cima da cobra
- `SnakeGame`: janela, loop do jogo, placar e controles

## Tecnologias

- Python 3
- Tkinter (já vem instalado com o Python na maioria dos sistemas)

## Como executar

1. Instale o [Python 3](https://www.python.org/downloads/)
2. Clone o repositório:
   ```bash
   git clone https://github.com/USUARIO/NOME-DO-REPO.git
   ```
3. Entre na pasta e execute o arquivo:
   ```bash
   cd NOME-DO-REPO
   python snake.py
   ```

## Como jogar

| Ação | Teclas |
|------|--------|
| Cima | ↑ ou W |
| Baixo | ↓ ou S |
| Esquerda | ← ou A |
| Direita | → ou D |

Coma os quadrados vermelhos para crescer e evite as paredes e o próprio corpo.

## Status

Projeto de estudo.
