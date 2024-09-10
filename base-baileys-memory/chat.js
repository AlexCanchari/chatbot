
const postCompletion = async (messages) => {
    try {
        const response = await fetch('http://127.0.0.1:1233/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "TheBloke/Mistral-7B-Instruct-v0.1-GGUF/mistral-7b-instruct-v0.1.Q4_0.gguf",
                messages: messages,
                temperature: 0.7,
                stream: false
            })
        });
        if (!response.ok) throw new Error('Failed to fetch');
        const completion = await response.json();
        const answer = completion.choices[0].message.content;
        return answer;
    }
    catch (error) {
        console.error("Error: ", error);
    }   
};

module.exports = {postCompletion} ;

