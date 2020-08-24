import fetch from "node-fetch";

export async function post(req, res) {
    const body = req.body;

    try {
        const url = `${process.env.API_URL}/api/v1/userdata`;

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
};

export async function put(req, res) {
    const body = req.body;

    try {
        const url = `${process.env.API_URL}/api/v1/userdata`;

        await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `token ${process.env.API_KEY}`,
            },
            body: JSON.stringify(body),
        });
    } catch (error) {
        console.error(error);
    }
};

export async function get(req, res) {
    let url = new URL(`${process.env.API_URL}/api/v1/userdata`);

    try {
        const resp = await fetch(url);
        const json = await resp.json();

        res.json(json);
    } catch (error) {
        res.status(500).end(JSON.stringify({ error }));
    }
};


/*
export async function del(req, res) {
    try {
        let url = `${process.env.API_URL}/api/v1/userdata`;
        const query = queryString.stringify(req.query);
        url = url + "/" + query.slice(0, -1);
        console.log(url);
        
        await fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: `token ${process.env.API_KEY}`,
            },
        }); 
    } catch (error) {
        console.error(error);
    }
} */