---
type: brag-entry
title: Migração do banco de pedidos para PostgreSQL 16
date: 2026-04-15
description: Planejei e conduzi a migração do banco de pedidos do PostgreSQL 11 para o 16, com replicação lógica e virada em janela de 10 minutos.
impact: Zero perda de dados; consultas de relatório 3x mais rápidas; fim do suporte estendido pago (economia de R$ 4 mil/mês).
tags: [projeto, lideranca]
status: stable
sources:
  - resource: https://example.atlassian.net/browse/ORD-210
    title: ORD-210 Migrar banco de pedidos para PG16
---

Envolveu o time de dados e o SRE. Escrevi o runbook de rollback, que não precisou ser usado.
