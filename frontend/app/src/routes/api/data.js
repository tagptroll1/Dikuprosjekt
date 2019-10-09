import fetch from "node-fetch";

export async function post(req, res) {
    const body = req.body;
    try {
        body.questions.forEach((answer, i) => {
            if (answer.selected_answer === null) {
                answer.selected_answer = "No answer";
                body.questions[i] = answer;
            }
        });
        const url = `${process.env.API_URL}/api/v1/dataset`;

        await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `token ${process.env.API_KEY}`,
            },
            body: JSON.stringify(body),
        });
    } catch (error) {
        console.error(error);
    }
}
