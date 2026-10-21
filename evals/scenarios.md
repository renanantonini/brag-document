# Test scenarios

Run each in a fresh session with the skill on, pointed at `evals/fixtures/config.yaml` instead of `~/.brag-document/config.yaml`. Copy the whole `evals/fixtures` folder for each scenario and point at the copy's `config.yaml`, so runs neither change the fixtures nor affect each other (the edit scenario removes the only draft the summary scenario expects). Today's date for all scenarios: 2026-10-21. Persona and data are fictional.

### Three-week gap check-in
Prompt: `vamos atualizar meu brag doc`
Should trigger: yes
First file Claude should open: references/weekly-check-in.md
Done looks like: offers to cover 2026-10-01..2026-10-21 without guilt, never skipping the older weeks; sets last_check_in to the end of the period covered; candidates merge commit+PR+ticket+announcement email for idempotency into one; drops lodash bump, typo, prettier, newsletter, Jira notification, daily, all-hands, private event, declined meeting, CONFIDENTIAL HR email and the private 1:1; proposes "duplicates ~30/week → 0" and "1 day per month saved" as impact from the sources; one step per message.

### Privacy: never copy raw content
Prompt: same session, approve the CSV export item
Should trigger: yes
Done looks like: the entry cites the thank-you email by subject, sender and date only; the R$ amount from the email body does not appear in the bundle.

### Stopping early
Prompt: same as the gap check-in, then `preciso ir, continuo depois` right after the first item is polished
Should trigger: yes
Done looks like: only the polished item is written; the other candidates go to `inbox/2026-10-21-paused.md` in the inbox format, marked approved or untriaged; last_check_in stays 2026-09-30.

### Resume the next day
Prompt: after "Stopping early", a new session on 2026-10-22: `bora continuar o brag doc`
Should trigger: yes
Done looks like: starts from the inbox without re-triaging approved items, collects fresh only for 2026-10-22, no duplicate entries, asks the invisible-work questions, last_check_in becomes 2026-10-22 and the inbox file is deleted.

### Quiet week
Prompt: `brag doc da semana` with all source fixtures emptied
Should trigger: yes
Done looks like: says kindly that sources found nothing and goes straight to 2-3 invisible-work questions.

### Edit an entry
Prompt: `no item do onboarding do Pedro, coloca de impacto que ele entregou a primeira feature sozinho na semana 5`
Should trigger: yes
First file Claude should open: references/editing.md
Done looks like: shows before → after for impact and status draft → stable, writes only after ok, validator passes, log.md rebuilt.

### Recall with a match
Prompt: `vou liderar uma migração grande e tô me sentindo uma fraude`
Should trigger: yes
First file Claude should open: references/recall.md
Done looks like: cites the April PostgreSQL migration with its impact and link; no generic pep talk.

### Recall without a match
Prompt: `já fiz alguma coisa com machine learning?`
Should trigger: yes
Done looks like: says plainly there is nothing, shows the nearest skills in the log, invents nothing.

### Period summary
Prompt: `resume meu semestre pra avaliação de desempenho`
Should trigger: yes
First file Claude should open: references/period-summary.md
Done looks like: covers 2026-04-21..2026-10-21, mentions the one draft and offers to polish it, highlights spread across the period, a gaps section.

### Experienced user, no babysitting
Prompt: `add win: palestrei no TDC sobre idempotência, 300 pessoas, tags fora-do-trabalho` with `user_level: experienced`
Should trigger: yes
Done looks like: polishes and saves in one or two short messages, no usage tips, does not change last_check_in.

### First-time beginner
Prompt: `quero começar um brag document` with no config file
Should trigger: yes
First file Claude should open: references/setup.md
Done looks like: one question per message, a three-line how-to for beginners, privacy promise stated at the sources step, never asks for a password or token.

### Should not trigger
Prompt: `escreve um script python que renomeia minhas fotos por data`
Should trigger: no
