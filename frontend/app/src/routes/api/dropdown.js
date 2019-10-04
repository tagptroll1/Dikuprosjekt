export async function get(req, res) {
    try {
        const fetch = process.browser
            ? window.fetch
            : require("node-fetch").default;

        const url = process.env.API_URL;

        const resp = await fetch(`${url}/api/v1/dropdown/set/2`);
        const json = await resp.json();

        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(json));
    } catch (error) {
        res.statusCode = 500;
        res.end({ error });
    }
}
