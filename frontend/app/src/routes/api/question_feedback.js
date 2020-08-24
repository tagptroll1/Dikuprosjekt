import fetch from "node-fetch";

export async function get(req, res) {
    const url = new URL(`${process.env.API_URL}/api/v1/question_feedback`);

    try {
        const resp = await fetch(url);
        const json = await resp.json();
        res.json(json);
    } catch (error) {
        res.status(500).end(JSON.stringify({ error }));
    }
}
