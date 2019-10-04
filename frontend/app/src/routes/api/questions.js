import fetch from "node-fetch";

export async function get(req, res) {
    try {
        const url = `${process.env.API_URL}api/v1/questions?multichoice=6&dropdown=6`;

        const resp = await fetch(url);
        const json = await resp.json();

        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(json));

    } catch (error) {
        res.statusCode = 500;
        res.end({ error });
    }
}
