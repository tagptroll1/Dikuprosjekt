import fetch from "node-fetch";
import queryString from "query-string";

export async function get(req, res) {
    const url = new URL(process.env.API_URL);
    const query = queryString.stringify(req.query);
    url.search = query;

    try {
        const resp = await fetch(url);
        const json = await resp.json();

        res.json(json);
    } catch (error) {
        res.status(500).end(JSON.stringify({ error }));
    }
}
