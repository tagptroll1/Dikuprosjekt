import fetch from "node-fetch";

export async function get(req, res) {
    try {
        const url = `${process.env.API_URL}/api/v1/questions?limit=10`;

        const resp = await fetch(url);
        const json = await resp.json();

        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(json));
    } catch (error) {
        res.status(500).end(JSON.stringify({ error }));
    }
}
