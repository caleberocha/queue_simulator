# Simulador de filas
Simulador de filas desenvolvido para a disciplina de Simulação e Métodos Analíticos. Até o momento, são suportadas filas simples e filas em *tandem*. 

## Requisitos
Python 3.7

## Uso

    # Com arquivo de entrada
    python3 -m queue_simulator arquivo [--debug]
    
    # Com string json de entrada
    python3 -m queue_simulator string_json [--debug]
    
## Formato de entrada
O arquivo ou string de entrada deve estar no formato JSON.

Os números aleatórios podem ser fornecidos em uma lista predefinida, ou podem ser fornecidos seeds e uma quantidade de números para gerar. A simulação rodará uma vez para cada seed especificado.

Formato do arquivo:


    {
      "seeds": [
          123,
          562,
          53,
          453,
          567
      ],
      "random_count": 100000,
      # Especificando seeds e random_count, o parâmetro rndNumbers não será utilizado
      "rndNumbers": [
          0.3276,
          0.8851,
          0.1643,
          0.5542,
          0.6813,
          0.7221,
          0.9881
      ],
      "initialEvent": {
          "queue": "F1",
          "time": 3.0
      },
      "queues": [
        {
          "name": "F1",
          "servers": 1,
          "capacity": 5,
          "arrival": [
              2.0,
              4.0
          ],
          "service": [
              3.0,
              5.0
          ]
        },
        {
          "name": "F2",
          "servers": 1,
          "capacity": 3,
          "arrival": [
              2.0,
              5.0
          ],
          "service": [
              3.0,
              5.0
          ]
        }
      ]
    }
