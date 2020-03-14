import fetch from "node-fetch";

export async function post(req, res) {
    const body = req.body;
    console.log(body)
    try {
        body.questions.forEach((answer, i) => {
            if (answer.selected_answer === null) {
                answer.selected_answer = "No answer";
                body.questions[i] = answer;
            }
        });
        //const url = `${process.env.API_URL}/api/v1/dataset`;
        const url = new URL("http://127.0.0.1:5000/api/v1/dataset");

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

export async function get(req, res) {
    try {
        //const response = await fetch(`${process.env.API_URL}/api/v1/data`);
        const response = new URL("http://127.0.0.1:5000/api/v1/data");
        const json = await response.json();
        res.json(json);
    } catch (error) {
        res.error(error);
    }
}
