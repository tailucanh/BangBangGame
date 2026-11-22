"""Startup housekeeping for the local SQLite store.

Runs once, before any game socket is open, so it never competes with a battle
writer. Only rows that nothing reads any more are removed:

* sessions             - web/flash sessions whose expiry has passed.
* multiplayer_matches  - finished/abandoned/interrupted room snapshots older
                         than MATCH_KEEP_DAYS (live phases are never touched;
                         ranked results live in rank_entries/match_history).
* world_boss_*         - rounds older than BOSS_KEEP_DAYS, always keeping the
                         two newest rounds and every round that still has an
                         undelivered reward.

Then the WAL is truncated, a VACUUM runs only when enough pages are free, and
PRAGMA optimize refreshes query-planner statistics. Any failure is logged and
skipped: housekeeping must never stop the game from starting.
"""
from __future__ import annotations

import time

import storage
from server_logging import get_logger

log = get_logger('maintenance')

MATCH_KEEP_DAYS = 7
BOSS_KEEP_DAYS = 30
VACUUM_FREE_RATIO = 0.25   # VACUUM only when >= 25% of pages are free...
VACUUM_MIN_FREE_PAGES = 256  # ...and at least ~1 MB can be reclaimed.

_DAY_MS = 86_400_000


def _has_table(db, name: str) -> bool:
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone() is not None


def _prune(db, now_ms: int) -> dict:
    removed = {}
    if _has_table(db, 'sessions'):
        removed['sessions'] = db.execute('DELETE FROM sessions WHERE exp < ?', (now_ms / 1000,)).rowcount
    if _has_table(db, 'multiplayer_matches'):
        removed['multiplayer_matches'] = db.execute(
            "DELETE FROM multiplayer_matches WHERE phase NOT IN ('loading','battle') AND updated_ms < ?",
            (now_ms - MATCH_KEEP_DAYS * _DAY_MS,)).rowcount
    if all(_has_table(db, t) for t in ('world_boss_rounds', 'world_boss_runs',
                                       'world_boss_scores', 'world_boss_rewards')):
        old = [r[0] for r in db.execute(
            'SELECT id FROM world_boss_rounds '
            'WHERE closed_ms IS NOT NULL AND closed_ms < ? '
            'AND id < (SELECT MAX(id) - 1 FROM world_boss_rounds) '
            'AND id NOT IN (SELECT round_id FROM world_boss_rewards WHERE delivered = 0)',
            (now_ms - BOSS_KEEP_DAYS * _DAY_MS,))]
        if old:
            marks = ','.join('?' * len(old))
            for table in ('world_boss_rewards', 'world_boss_scores', 'world_boss_runs'):
                db.execute(f'DELETE FROM {table} WHERE round_id IN ({marks})', old)
            db.execute(f'DELETE FROM world_boss_rounds WHERE id IN ({marks})', old)
        removed['world_boss_rounds'] = len(old)
    return removed


def run_startup(path=None) -> dict:
    started = time.perf_counter()
    report: dict = {}
    try:
        with storage.connection(path, write=True) as db:
            report['removed'] = _prune(db, time.time_ns() // 1_000_000)
        with storage.connection(path) as db:
            db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            pages = db.execute('PRAGMA page_count').fetchone()[0]
            free = db.execute('PRAGMA freelist_count').fetchone()[0]
            if free >= VACUUM_MIN_FREE_PAGES and free >= pages * VACUUM_FREE_RATIO:
                db.execute('VACUUM')
                report['vacuum_pages'] = free
            db.execute('PRAGMA optimize')
    except Exception:
        log.exception('[maintenance] startup housekeeping skipped')
        report['error'] = True
    report['ms'] = round((time.perf_counter() - started) * 1000)
    log.info('[maintenance] %s', report)
    return report
