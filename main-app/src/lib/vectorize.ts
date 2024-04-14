
export const vectorize = async (input: string): Promise<number[]> => {
    const url = `http://localhost:5000/search?term=${encodeURIComponent(input)}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch');
        }

        const result = await response.json();

        return result[0];
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}