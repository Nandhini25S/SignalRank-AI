import { useState } from 'react'
import IdeaInput from './components/IdeaInput'
import ResultCard from './components/ResultCard'
import { evaluateIdea } from './api/evaluate'
import styles from './App.module.css'

export default function App() {
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleSubmit = async (idea) => {
        setLoading(true)
        setError(null)
        setResult(null)
        try {
            const data = await evaluateIdea(idea)
            setResult(data)
        } catch (err) {
            const msg = err.response?.data?.detail || 'Something broke. Try again.'
            setError(msg)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className={styles.page}>
            {/* Header */}
            <header className={styles.header}>
                <span className={styles.logo}>BRUTAL</span>
                <span className={styles.sub}>NO VALIDATION. JUST REALITY.</span>
            </header>

            <main className={styles.main}>
                {/* Hero text */}
                <div className={styles.hero}>
                    <h1 className={styles.headline}>PUT YOUR IDEA HERE.<br />GET A REALITY CHECK.</h1>
                    <p className={styles.tagline}>We search GitHub. We check saturation. We tell you the truth.</p>
                </div>

                {/* Input */}
                <IdeaInput onSubmit={handleSubmit} loading={loading} />

                {/* Loading */}
                {loading && (
                    <div className={styles.loading}>
                        <span className={styles.dot} />
                        <span>SEARCHING GITHUB · EVALUATING · FORMING VERDICT</span>
                    </div>
                )}

                {/* Error */}
                {error && (
                    <div className={styles.error}>⚠ {error}</div>
                )}

                {/* Result */}
                {result && <ResultCard result={result} onReset={() => setResult(null)} />}
            </main>

            <footer className={styles.footer}>
                IF YOU'RE OFFENDED, YOUR IDEA NEEDED THIS.
            </footer>
        </div>
    )
}