import fetch from "node-fetch";

export async function post(req, res) {
    try {
        const body = JSON.stringify(req.body);
        const url = `${process.env.API_URL}/api/v1/question_feedback/set`;

        const resp = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body,
        });

        const json = await resp.json();
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(json));
    } catch (error) {
        res.statusCode = 500;
        res.end({ error });
    }
}
