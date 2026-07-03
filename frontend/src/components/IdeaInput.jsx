import { useState } from 'react'
import styles from './IdeaInput.module.css'

export default function IdeaInput({ onSubmit, loading }) {
    const [idea, setIdea] = useState('')

    const handleSubmit = () => {
        if (idea.trim().length >= 10 && !loading) onSubmit(idea.trim())
    }

    const handleKey = (e) => {
        if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmit()
    }

    return (
        <div className={styles.wrapper}>
            <div className={styles.label}>DROP YOUR IDEA.</div>
            <textarea
                className={styles.textarea}
                placeholder="Describe your idea. No pitch deck language. Just what it is."
                value={idea}
                onChange={e => setIdea(e.target.value)}
                onKeyDown={handleKey}
                rows={5}
                disabled={loading}
            />
            <div className={styles.footer}>
                <span className={styles.hint}>⌘ + ENTER TO SUBMIT</span>
                <button
                    className={styles.btn}
                    onClick={handleSubmit}
                    disabled={loading || idea.trim().length < 10}
                >
                    {loading ? 'EVALUATING...' : 'EVALUATE →'}
                </button>
            </div>
        </div>
    )
}