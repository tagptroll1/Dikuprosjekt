import fetch from "node-fetch";

export async function get(req, res) {
    try {
        const url = `${process.env.API_URL}/api/v1/questions?limit=10`;
        console.log(url);
        
        const resp = await fetch(url);
        console.log(resp);
        
        const json = await resp.json();
        console.log(json);
        
        res.json(json);

    } catch (error) {
        console.log(error);
        
        res.statusCode = 500;
        res.end({ error });
    }
}
