import styles from './ResultCard.module.css'

function ScoreBar({ label, value }) {
    return (
        <div className={styles.scoreRow}>
            <span className={styles.scoreLabel}>{label}</span>
            <div className={styles.barTrack}>
                <div className={styles.barFill} style={{ width: `${value * 10}%` }} />
            </div>
            <span className={styles.scoreNum}>{value}/10</span>
        </div>
    )
}

export default function ResultCard({ result, onReset }) {
    const { interpretation, repos, scores, verdict, improvements } = result

    return (
        <div className={styles.card}>

            <section className={styles.section}>
                <div className={styles.tag}>WHAT WE HEARD</div>
                <p className={styles.interpretation}>{interpretation}</p>
            </section>

            <section className={styles.verdictSection}>
                <div className={styles.tag}>VERDICT</div>
                <p className={styles.verdict}>{verdict}</p>
            </section>

            <section className={styles.section}>
                <div className={styles.tag}>SCORES</div>
                <div className={styles.scores}>
                    <ScoreBar label="ORIGINALITY" value={scores.originality} />
                    <ScoreBar label="SATURATION" value={scores.saturation} />
                    <ScoreBar label="EXEC DIFFICULTY" value={scores.execution_difficulty} />
                </div>
            </section>

            <section className={styles.section}>
                <div className={styles.tag}>WHERE TO GO FROM HERE</div>
                <ol className={styles.improvements}>
                    {improvements.map((item, i) => (
                        <li key={i}>{item}</li>
                    ))}
                </ol>
            </section>

            {repos.length > 0 && (
                <section className={styles.section}>
                    <div className={styles.tag}>ALREADY EXISTS — GITHUB EVIDENCE</div>
                    <div className={styles.repos}>
                        {repos.map((r, i) => {
                            const year = r.created_at?.slice(0, 4)
                            return (
                                <a key={i} href={r.url} target="_blank" rel="noopener noreferrer" className={styles.repo}>
                                    {year && <span className={styles.timeContext}>Similar concept already implemented since {year}.</span>}
                                    <span className={styles.repoName}>{r.name}</span>
                                    <span className={styles.repoMeta}>⭐ {r.stars} · {r.created_at}</span>
                                    {r.description && <span className={styles.repoDesc}>{r.description}</span>}
                                </a>
                            )
                        })}
                    </div>
                </section>
            )}

            <section className={styles.resetSection}>
                <button className={styles.resetBtn} onClick={onReset}>
                    ← EVALUATE ANOTHER IDEA
                </button>
            </section>

        </div>
    )
}