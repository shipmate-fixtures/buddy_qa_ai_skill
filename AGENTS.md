# AGENTS.md

Repozytorium skilli agentowych w formacie [Agent Skills](https://agentskills.io/specification).
Ten plik jest wspolnym zrodlem prawdy dla wszystkich agentow; `CLAUDE.md` i
`GEMINI.md` tylko go importuja.

## Uklad katalogow

Kanoniczna lokalizacja skilli to `.agents/skills/`. Pozostale sciezki to
symlinki na ten sam katalog, zeby kazde CLI znalazlo skille pod swoja
domyslna sciezka:

```
.agents/skills/<nazwa>/SKILL.md   # kanoniczne (Antigravity czyta wprost)
.claude/skills -> ../.agents/skills
.grok/skills   -> ../.agents/skills
```

**Nowy skill dodawaj wylacznie w `.agents/skills/`.** Nie tworz plikow przez
symlinki i nie duplikuj skilla per narzedzie — rozjechane kopie to najczestszy
blad w tym ukladzie.

## Format skilla

Katalog o nazwie zgodnej z polem `name`, w srodku `SKILL.md`:

```markdown
---
name: <lowercase-z-myslnikami, max 64 znaki, = nazwa katalogu>
description: <max 1024 znaki; co skill robi ORAZ kiedy go uzyc, w 3. osobie>
---

<instrukcje>
```

Opcjonalne pola frontmattera: `license`, `compatibility`, `metadata`,
`allowed-tools`. Opcjonalne podkatalogi: `scripts/` (kod wykonywalny),
`references/` (dokumentacja ladowana na zadanie), `assets/` (szablony, dane).

`description` decyduje o tym, czy agent w ogole siegnie po skill — to jedyna
czesc ladowana na starcie sesji. Ma zawierac slowa kluczowe, po ktorych da sie
rozpoznac pasujace zadanie.

## Zasady

- `SKILL.md` trzymaj ponizej ~500 linii; dluzsze tresci wynies do `references/`
  i linkuj sciezka wzgledna od korzenia skilla.
- Sciezki w tresci `SKILL.md` pisz jako kanoniczne `.agents/skills/...` albo
  wzgledne od korzenia skilla. Nigdy przez `.claude/` ani `.grok/` — to symlinki.
- Skrypty w `scripts/` maja byc samowystarczalne albo jawnie dokumentowac
  zaleznosci, i maja lokalizowac swoje dane wzgledem `__file__`, a nie cwd.
- Walidacja frontmattera: `skills-ref validate .agents/skills/<nazwa>`.

## Dostepne skille

- `vault-unlock` — odczytuje sekret zapieczetowany w `vault.bin`, uruchamiajac
  `scripts/unlock.py`. Sekretu nie da sie poznac czytajac pliki.
