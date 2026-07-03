import axios from 'axios'

export async function evaluateIdea(idea) {
    const response = await axios.post('/api/evaluate', { idea })
    return response.data
}