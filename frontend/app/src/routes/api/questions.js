import fetch from "node-fetch";
import queryString from "querystring";

export async function get(req, res) {
    const url_str = `${process.env.API_URL}/api/v1/questions`;
    const url = new URL(url_str);
    const query = queryString.stringify(req.query);
    url.search = query;

    try {
        const resp = await fetch(url.href);
        const json = await resp.json();

        res.json(json);
    } catch (error) {
        res.status(500).end(JSON.stringify({ error }));
    }
}

export async function post(req, res) {
    const { body } = req;

    const url = `${process.env.API_URL}/api/v1/questions`;

    try {
        const resp = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `token ${process.env.API_KEY}`,
            },
            body: JSON.stringify(body),
        });

        const text = await resp.text();

        try {
            const json = JSON.parse(text);

            if (resp.ok) {
                res.status(201).json(json)
            } else {
                res.status(resp.status).json(json);
            }
        } catch (error) {
            res.status(500).end("Json parsing failed, text: " + text);
        }
    } catch (error) {
        res.status(500).end("Request failed")
    }
}
