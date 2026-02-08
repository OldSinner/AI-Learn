# AI-Learn

Projekt do tworzenia małych aplikacji pokazujących proces nauki sztucznej inteligencji.

## Struktura projektu

```
AI-Learn/
├── projects/                   # Podprojekty AI
│   └── snake_ai/              # Projekt gry Snake z Q-learningiem
│       ├── src/               # Kod źródłowy projektu
│       │   ├── __init__.py
│       │   ├── main.py        # Główny plik uruchamiający
│       │   ├── basesnake.py   # Bazowa klasa gry
│       │   ├── snakenotail.py # Implementacja AI (bez ogona)
│       │   ├── model.py       # Modele i definicje
│       │   └── utils.py       # Funkcje pomocnicze
│       ├── notebooks/         # Eksperymenty i testy
│       │   ├── snakeai-notail.ipynb
│       │   └── snakeai-tail.ipynb
│       ├── models/            # Wytrenowane modele
│       └── data/              # Dane do eksperymentów
├── lib/                       # Biblioteki wspólne dla projektów
├── utils/                     # Narzędzia i funkcje utility
├── apps/                      # Gotowe aplikacje
├── requirements.txt           # Zależności Python
├── .gitignore                # Ignorowane pliki Git
└── README.md                 # Dokumentacja
```

## Kluczowe elementy

- **projects/**: Każdy podprojekt ma własną strukturę z `src/`, `notebooks/`, `models/`, `data/`
- **lib/**: Wspólne biblioteki i klasy używane w wielu projektach
- **utils/**: Funkcje pomocnicze i narzędzia

## Uruchamianie

Aby uruchomić projekt snake_ai:

```bash
cd projects/snake_ai/src
python main.py
```

## Instalacja

```bash
pip install -r requirements.txt
```
