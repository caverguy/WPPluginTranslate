# Python Script til Oversættelse af Stings i PHP og JS Filer

## Introduktion
Dette Python script er designet til at automatisere oversættelsen af strenge i PHP- og JavaScript-filer. Det bruger Google Cloud Translation API til at oversætte tekst, mens den centrale kode forbliver uændret. Dette værktøj er især nyttigt for udviklere, der arbejder på flersprogede projekter, eller for enhver, der har brug for effektivt at oversætte mange strenge i kodefiler.

## Funktioner
- Oversætter strenge i PHP- og JS-filer ved hjælp af Google Cloud Translation API.
- Understøtter inkrementelle oversættelser for at undgå at genoversætte uændrede strings.
- Giver mulighed for brugerdefinerede regulære udtryk til strengmatching.
- Indeholder muligheder for at udelukke bestemte filer eller mapper.
- Tilbyder en dry run-tilstand til test uden at foretage faktiske ændringer.
- Leverer detaljeret logging for detaljeret output.

## Krav
- Python 3
- Google Cloud Platform konto med aktiveret Translation API
- Nødvendige Python pakker: `google-cloud-translate`

## Installation

Før du kører scriptet, skal du sikre dig, at du har Python installeret på dit system. Opsæt derefter Google Cloud Translation API og installer den nødvendige Python-pakke:

```bash
pip install google-cloud-translate
```
## Brug

Brug
For at bruge scriptet, kør det fra kommandolinjen med de nødvendige argumenter.
```bash
 python translate_script.py <mappe> <målsprogs_kode> [valgmuligheder]

```
# Argumenter
<mappe>: Mappen, der indeholder de filer, der skal oversættes
<målsprogs_kode>: Målsprogskoden (f.eks. 'da' for dansk).

# Valgmuligheder:
- --min_length: Minimumslængde af strenge, der skal oversættes (standard er 5).
- --dry_run: Kør scriptet i dry run-tilstand uden faktisk at skrive til filerne.
- --regex: Regulært udtryk til strengmatching.
- --exclude: Liste over filstier, der skal udelukkes fra oversættelse.
- --verbose: Aktiver detaljeret output.
# Eksempel:
```bash 
python translate_script.py /sti/til/din/mappe da
```
